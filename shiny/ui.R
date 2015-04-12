library(shiny)

cip <- read.csv("data/cip_mapping.csv")
cip <- cip[order(cip$category_name), ]
cip <- cip[grep("^[1234567890]", cip$category_name), ]

# Define the overall UI
fluidPage(      
    
    # Give the page a title
    titlePanel("Occupation by Education Category"),
    
    # Generate a row with a sidebar
    sidebarLayout(      
      
        # Define the sidebar with one input
        sidebarPanel(
            selectInput(
                "cip", 
                "Field of Education: ", 
                choices=as.vector(cip$category_name),
                width="100%"
            ),
            hr(),
            helpText("Select a field of education.")
        ),

        # Create a spot for the barplot
        mainPanel(
            plotOutput("nocPlot")  
        ),

        fluid=TRUE
    )
)


