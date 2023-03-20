#install.packages('tidyverse')
#install.packages("scattermore") 
library(tidyverse)
library(dplyr)
require(scattermore)
library(data.table)

path ="C:/Users/mrahim6/OneDrive - Louisiana State University/Papers/Temperature trend/Paper 1/Mann-Kendall"
attr = "TempDifferenceMean/"
setwd(paste(path,"/Analysis/",attr,sep=""))
#files = list.files(".")
#file= files[1]
file = "Difference.csv" 
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

    ggsave(paste(path,"/Maps/",attr,"/",substr(file,1,nchar(file)-4),".png",sep=""),
           width = 9, height =6)
}
setwd(paste(path,"/Analysis/",sep=""))
df <- fread('Difference_mean_avg.csv')

title = paste('Temperature Variation between MinMaxMean and MeanHourly Methods', sep=" ")
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


###2011-2020 over 1981-1990

path ="C:/Users/mrahim6/OneDrive - Louisiana State University/Papers/Temperature trend/Paper 1/Mann-Kendall"
attr = "Temperatures/mean/"
setwd(paste(path,"/Analysis/",attr,sep=""))
files = list.files(".")
#file= files[1]
for (file in files){
  df <- fread(paste(file,'/TempVariation.csv',sep=""))
  ggplot(df, aes(x=x, y=y, color = TempDiff)) +
    geom_scattermore() +
    scale_color_viridis_c(option = "turbo") +
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
  
  ggsave(paste(path,"/Maps/TempDifferenceMean/Monthly","/",file,".png",sep=""),
         width = 9, height =6)
}



