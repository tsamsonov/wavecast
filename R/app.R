## app.R ##
library(sf)
library(tmap)
library(tidyverse)
library(shiny)
library(shinydashboard)
library(shinyWidgets)

drawMap = function(){
  d = 10000
  
  filled = st_read('Wavetin.gdb', 'filledcont_attr')
  black = st_read('Wavetin.gdb', 'black')
  
  cont = st_read('Wavetin.gdb', 'cont') %>% 
    mutate(len = st_length(.),
           Contour = round(Contour, 1)) %>% 
    filter(len > units::set_units(30000, m))
  
  filled = filled %>%
    mutate(м = MEAN_v1)
  
  tm_shape(black) +
    tm_borders(col = 'grey', lwd = 4) +
    tm_shape(filled) +
    tm_polygons('м', 
                breaks = 0.5 * 0:10, border.col = NULL,
                legend.format = list(text.separator = '—'),
                legend.reverse = TRUE,
                showNA = FALSE) +
    tm_shape(cont) +
    tm_iso(col = 'black',
           lwd = 1,
           text = 'Contour', 
           size = 0.8) +
    tm_layout(frame = FALSE,
              title.fontfamily = 'Open Sans',
              title.position = c('center', 'top'),
              title = 'Прогноз высоты волны на 2011-01-04 12:00',
              inner.margins = c(0.02, 0.02, 0.15, 0.02),
              legend.title.size = 1.2,
              legend.text.size = 0.9,
              legend.bg.color = 'white')
}

dashboardPage(
  dashboardHeader(),
  dashboardSidebar(),
  dashboardBody()
)

ui <- dashboardPage(
  dashboardHeader(
    title = "Прогноз волнения",
    titleWidth = 200
  ),
  dashboardSidebar(
    width = 200,
    dateInput("date1", "Дата: ", value = "2011-01-04"),
    radioGroupButtons(
      inputId = "times",
      label = "Срок:", 
      choices = c("00", "03", "06", "09", "12", "15", "18", "21"),
      status = "primary"
    )
  ),
  dashboardBody(
    fluidRow(
      column(width = 12,
             style = "width:700px",
        tabBox(
          title = "Параметры", width = NULL,
          # The id lets us use input$tabset1 on the server to find the current tab
          id = "tabset1", height = "250px",
          tabPanel("Высота", plotOutput("map1")),
          tabPanel("Период", plotOutput("map2")),
          tabPanel("Длина", plotOutput("map3")),
          tabPanel("Энергия", plotOutput("map4"))
        )
      )
    )
  )
)

server <- function(input, output) {
  output$map1 <- renderPlot(drawMap())
  output$map2 <- renderPlot(drawMap())
  output$map3 <- renderPlot(drawMap())
  output$map4 <- renderPlot(drawMap())
}

shinyApp(ui, server)
