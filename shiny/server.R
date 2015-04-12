library(shiny)
library(dplyr)
library(ggplot2)
library(grid)
library(ggthemes)

# read data
cipdf <- read.csv("data/cip_mapping.csv")
nocdf <- read.csv("data/noc_mapping.csv")
datadf <- read.csv("data/dump.csv")

# set column name
colnames(nocdf)[which(names(nocdf) == "category_key")] <- "NOC2011"

# wrap x axis labels

label_wrap <- function(s) {
    s <- strwrap(s, width=20)
    paste(s, collapse="\n") 
}
nocdf$category_name <- lapply(nocdf$category_name, label_wrap)

# Define a server for the Shiny app
function(input, output) {

    output$nocPlot <- renderPlot({

        cip <- input$cip
        cip_key <- cipdf[cipdf$category_name==cip, "category_key"]

        p <- datadf %>% 
            # to avoid selecting top level categories, filter on cat4 
            filter(CIP2011_4 == cip_key, !is.na(occupation_cat4)) %>%
            
            # sort by observation value descending 
            arrange(desc(observation_value)) %>% 
            
            # take the top 
            slice(1:10) %>%
            
            # inner join to pick up the occupation name
            inner_join(nocdf, by="NOC2011") %>%

            # discard unused columns
            select(observation_value, category_name) 
       
        # prevent ggplot from ordering the x axis alphabetically
        p$category_name <- factor(
            p$category_name, 
            levels=p$category_name, ordered=TRUE
        )

        # plot
        p %>% ggplot(aes(x=category_name, y=observation_value)) + 
        geom_bar(stat="identity") +
        xlab("") + 
        ylab("") + 
        theme_economist() + 
        theme(
            axis.text.x=element_text(angle=45, hjust=1), 
            plot.margin=unit(c(0, 0, 0, 0), "cm")
        )

    })
}





