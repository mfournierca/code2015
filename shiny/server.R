library(shiny)
library(dplyr)

cip <- read.csv("../data/cip_mapping.csv")
df <- read.csv("../data/dump.csv")

# Define a server for the Shiny app
function(input, output) {
  
  output$nocPlot <- renderPlot({
    
    cip <- input$cip
    cip_key <- cip[cip$category_name==s, "category_key"]
    
    print(cip_key)
    
  })
}




