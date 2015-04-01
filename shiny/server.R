library(shiny)
library(dplyr)
library(ggplot2)

cipdf <- read.csv("../data/cip_mapping.csv")
nocdf <- read.csv("../data/noc_mapping.csv")
datadf <- read.csv("../data/dump.csv")

colnames(nocdf)[which(names(nocdf) == "category_key")] <- "NOC2011"

head(datadf)

# Define a server for the Shiny app
function(input, output) {
  
  output$nocPlot <- renderPlot({
    
    cip <- input$cip
    cip_key <- cipdf[cipdf$category_name==cip, "category_key"]

    p <- datadf %>% 
      filter(CIP2011_4 == cip_key, !is.na(occupation_cat4)) %>% 
      arrange(desc(observation_value)) %>% 
      slice(1:25) %>%
      inner_join(nocdf, by="NOC2011") %>%
      select(observation_value, category_name) %>%
      ggplot(aes(x=category_name, y=observation_value)) + 
        geom_bar(stat="identity") +
        theme(axis.text.x = element_text(angle = 30, hjust = 1))
    
    print(p)
  })
}





