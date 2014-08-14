### Script to create the CHD coding scheme. 
# The script takes the name of the indicator in its
# original language, sends to Google Translate for a
# machine English translation and compares the result to a
# list of topics for a unambiguous coding scheme using regex.

# This is to be used at the collector level. When the indicator table has
# been generated. 
# library(translate)

chdCoder <- function(df = indicator, iso3 = NULL, foreign = F, from = "es", gen = NULL, top = NULL) {
    # Sanity checks.
    
    # Key-word lists.
    health_list <- c('health', 'malaria', 'cholera', 'hospital', 
                     'patient')
    demographic_list <- c('population', 'communit', 'territory', 'area')
    humanitarian_list <- c('displace', 'refugee', 'violence', 'mine')
    
    # Creating an English list using Google Translate.
    if (foreign == TRUE) {
        source('code/auth.R')
        eng <- list()
        message('Translating names.')
        pb <- txtProgressBar(min = 0, max = nrow(df), style = 3)
        for (j in 1:nrow(df)) {
            setTxtProgressBar(pb, j)  # Updates progress bar.
            eng[j] <- translate(indicator$name[j], source = "es", 
                                target = "en", key = gtrans_auth)
        }
    }
    
    # The code generator.
    message('Creating codes.')
    # Overral progress bar.0
    pb <- txtProgressBar(min = 0, max = nrow(df), style = 3)
    for (i in 1:nrow(df)) {
        setTxtProgressBar(pb, i)  # Updates progress bar.
        
        # Adding the 0s to the code.
        if (nchar(i) == 1) ind_index <- paste('00', i, sep = "")
        if (nchar(i) == 2) ind_index <- paste('0', i, sep = "")
        if (nchar(i) == 3) ind_index <- i
            
        # Regex of the English translations.
        hth <- grepl(paste(health_list, collapse = "|"), as.character(indicator$name[i]), 
                     ignore.case = T)
        pop <- grepl(paste(demographic_list, sep = "|"), as.character(indicator$name[i]), 
                     ignore.case = T)
        hum <- grepl(paste(humanitarian_list, sep = "|"), as.character(indicator$name[i]), 
                     ignore.case = T)
            
        # Adding CHD-specific codes.
        if (hth == TRUE) {
            general <- 'B'
            topic <- 'HTH'
        }
        if (pop == TRUE) {
            general <- 'B'
            topic <- 'POP'
        }
        if (hum == TRUE) {
            general <- 'O'
            topic <- 'HUM'
        }
        
        if (any(hth, pop, hum) == FALSE) {
            if (!is.null(gen)) general <- gen
             else general <- 'UNK'
            if (!is.null(top)) topic <- top
             else topic <- 'UNK'
        }
        
        # Assembling the code.
        code <- paste(iso3, general, topic, ind_index, sep = ".")
        
        indicator$indID[i] <- code
    }
    indicator
}