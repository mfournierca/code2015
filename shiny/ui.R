library(shiny)

cip <- read.csv("../data/cip_mapping.csv")

# Define the overall UI

fluidPage(    
  
  # Give the page a title
  titlePanel("Occupation by Education Category"),
  
  # Generate a row with a sidebar
  sidebarLayout(      
    
    # Define the sidebar with one input
    sidebarPanel(
      selectInput("cip", "Field of Education: ", 
                  choices=as.vector(cip$category_name)),
      hr(),
      helpText("Select a field of education.")
    ),
    
    # Create a spot for the barplot
    mainPanel(
      plotOutput("nocPlot")  
    )
  )
)


