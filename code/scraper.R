## Script to scrape data from ORS / ROWCA / OCHA. 
library(XML)
library(RCurl)
source('code/write_tables.R')
source('code/chd_coder.R')

# collecting data
base_url <- 'http://ors.ocharowca.info/Anonymous/AllDataFeed.ashx'
doc <- xmlTreeParse(getURL(base_url), useInternalNodes = TRUE)
data <- xmlToDataFrame(nodes = getNodeSet(doc,"//Table"))

# storing raw data in db
writeTables(df = data, table_name = '_raw_data', db = 'scraperwiki')

# dataset table
dataset <- data.frame(dsID = 'ocha-ors',
                      last_updated = NA,
                      last_scraped = as.character(Sys.time()),
                      name = "OCHA ROWCA's Online Reporting System")
# value table
value <- data

# cleaning columns that will not be added
value$Cluster <- NULL
value$Organization <- NULL
value$ProjectCode <- NULL
value$Year <- NULL
value$MONTH <- NULL
value$Objective <- NULL
value$Priority <- NULL
value$AnnualTarget <- NULL
value$Activity <- NULL
value$LocationPCode <- NULL
value$RunningSum <- NULL
value$Country <- NULL

# handling accumulative
value$Indicator <- ifelse(value$Accumulative == 'YES', paste(value$Indicator, "(Accumulative)"), value$Indicator)
value$Accumulative <- NULL

# adding names
names(value) <- c('indID', 'region', 'value', 'period')
value$dsID <- 'ocha-ors'
value$source <- 'http://ors.ocharowca.info/Anonymous/AllDataFeed.ashx'
value$is_number <- 1

# indicator table
indicator <- data.frame(indID = NA, name = unique(value$indID), units = NA)
indicator <- chdCoder(iso3 = "REG", gen = "O")

# storing raw data in db
writeTables(df = indicator, table_name = 'indicator', db = 'scraperwiki')
writeTables(df = dataset, table_name = 'dataset', db = 'scraperwiki')
writeTables(df = value, table_name = 'value', db = 'scraperwiki')