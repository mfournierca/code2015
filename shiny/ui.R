library(shiny)

cip <- read.csv("/usr/local/code2015/data/cip_mapping.csv")
cip <- cip[order(cip$category_name), ]
cip <- cip[grep("^[1234567890]", cip$category_name), ]

# Define the overall UI
fluidPage(      
    
    # Give the page a title
    titlePanel("Employment Categories by Education"),
    fluidRow( 
        # Generate a row with a sidebar
        sidebarLayout(      
          
            # Define the sidebar with one input
            sidebarPanel(
                 selectInput(
                    "cip", 
                    "Select Field of Education: ", 
                    choices=as.vector(cip$category_name),
                    width="100%",
                ), 
                helpText("This tool generates a graph of where people with a given education are employed. The graph is ranked by number of people in each job, so the most popular / likely occupations are first."),
                # caveats / notes
                HTML("
                    <p>Notes:</p>
                    <ul>
                        <li>Data taken from the 2011 Canadian national census.</li>
                        <li>Values are estimates for the total population based on the census.</li>
                        <li>Data is aggregated across all age groups, provinces and census divisions.</li>
                        <li>Some data is excluded due to quality issues, privacy rules imposed on Statistics Canada, or non-response on the census.</li>
                    </ul>"
                )
            ),

            # Create a spot for the barplot
            mainPanel(
                plotOutput("nocPlot")  
            ),

            fluid=TRUE
        )
    ), 
    hr()
)


