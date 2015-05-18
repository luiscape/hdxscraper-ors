# plotting script #
library(ggplot2)

# loading + preparing
data <- read.csv('data/data.csv')
data$MONTH <- factor(data$MONTH, levels = month.name)

# plotting
country_plot <- ggplot(data) + theme_bw() +
    geom_bar(aes(Country), stat = 'bin') +
    ylab('Number of Data Points')

ggsave('plots/country_plot.png', country_plot, width = 100, height = 70, units = 'mm')

ggplot(data) + theme_bw() +
    geom_bar(aes(Organization, fill = Country), stat = 'bin') +
    ylab('Number of Data Points') +
    theme(axis.text.x = element_text(angle = 90))


# simple time plot
ggplot(data) + theme_bw() +
    geom_bar(aes(MONTH, fill = Country), stat = 'bin') +
    ylab('Number of Data Points')



## prototyping ##
# plotting a single indicator #
x <- data[data$Indicator == 'number of households receiving assistance in agriculture for off season vegetable gardening and season recession crops', ]

ggplot(x) + theme_bw() +
    geom_bar(aes(MONTH, AnnualTarget, group = Admin1), stat = 'identity', position = 'dodge', fill = "#cccccc") +
#     geom_bar(aes(MONTH, AnnualTarget, group = Admin1), stat = 'identity', position = 'dodge') +
    facet_wrap(~ Admin1) +
    theme(axis.text.x = element_text(angle = 90))


