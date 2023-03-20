#Plot trend analysis maps

#install.packages(c("dplyr","tidyverse","scattermore","data.table")) 
library(tidyverse)
library(dplyr)
require(scattermore)
library(data.table)

attributes = c('minmaxmean','meanhourly')

for (attr in attributes){
  for (file in files){
    df <- fread(file)
    #title = paste('Temperature variation of 2011-2020 over 1981-1990', sep=" ")
    ggplot(df, aes(x=x, y=y, color = TempDiff)) +
      geom_scattermore() +
      scale_color_viridis_c(option = "turbo") +
      #ggtitle(title)+ 
      #labs(y = "Latitude", x = "Longitude") +
      theme_bw()  +
      theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
      #theme(plot.margin = unit(c(1,1,1,1), "cm")) +
      #theme(plot.title = element_text(hjust = 0.5)) +
      theme(axis.title.x = element_blank()) +
      theme(axis.title.y = element_blank()) +
      theme(axis.text.x=element_blank(), #remove x axis labels
            axis.ticks.x=element_blank(), #remove x axis ticks
            axis.text.y=element_blank(),  #remove y axis labels
            axis.ticks.y=element_blank()  #remove y axis ticks
      )+
      labs(color = "")
  
      ggsave(paste("Maps/",attr,"/",substr(file,1,nchar(file)-4),".png",sep=""),
             width = 9, height =6)
  }
}

###########################################
# Temperature Variation between minmaxmean and meanhourly Methods
for (attr in attributes){
  df <- fread(paste('Difference_1981_2020_',attr ,'.csv',sep=""))
  
  ggplot(df, aes(x=x, y=y, color = TempDiff)) +
    geom_scattermore() +
    scale_color_viridis_c(option = "turbo") +
    ggtitle(title)+ 
    labs(y = "Latitude", x = "Longitude") +
    theme_bw()  +
    #theme(plot.margin = unit(c(1,1,1,1), "cm")) +
    theme(plot.title = element_text(hjust = 0.5))
  
  ggsave(paste(path,"/Maps/","/","difference.png",sep=""),
         width = 9, height =6)
}
