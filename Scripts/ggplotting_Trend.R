#install.packages('tidyverse')
#install.packages("scattermore") 
library(tidyverse)
library(dplyr)
require(scattermore)
library(data.table)

path ="C:/Users/mrahim6/OneDrive - Louisiana State University/Papers/Temperature trend/Paper 1/Mann-Kendall"
attr = "Monthly_Average/"
setwd(paste(path,"/Analysis/",attr,sep=""))
files = list.files(".")
file= files[1]

for (file in files){
  df <- fread(file)
  colnames(df) = c('x','y','rho','pval','Slope','MK')
  df$quality <- with(df, ifelse((pval < 0.05 & rho < 0), "Significantly Descreasing (p-value= 0.05)",
                                                  ifelse(pval > 0.05 & pval < 0.1 & rho < 0, "Significantly Descreasing (p-value= 0.10)",
                                                         ifelse(pval < 0.05 & rho > 0, "Significantly Increasing (p-value= 0.05)",
                                                                ifelse(pval > 0.05 & pval < 0.1  & rho > 0, "Significantly Increasing (p-value= 0.10)", "Insignificant")))))
  
  ggplot(df, aes(x=x, y=y, color = factor(quality))) +
    geom_scattermore(pointsize=0) +
    scale_color_manual(values=c('grey','#02476e','#bdd2fd','#720000','#e1972e')) +
    theme_bw()  +
    theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
    theme(axis.title.x = element_blank()) +
    theme(axis.title.y = element_blank()) +
    theme(axis.text.x=element_blank(), #remove x axis labels
          axis.ticks.x=element_blank(), #remove x axis ticks
          axis.text.y=element_blank(),  #remove y axis labels
          axis.ticks.y=element_blank()  #remove y axis ticks
    )+
    labs(color = "") +
    theme(legend.text = element_text(size=9)) + 
    theme(legend.position="bottom") +
    guides(color = guide_legend(nrow = 2, byrow = TRUE))
  
  ggsave(paste(path,"/Maps/",attr,"Trend/",substr(file,1,2),".png",sep=""),
         width = 9, height =6)
 
  
  ggplot(df, aes(x=x, y=y, color = Slope)) +
    geom_scattermore() +
    scale_color_viridis_c(option = "turbo") +
    
    theme_bw()  +
    theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
    theme(axis.title.x = element_blank()) +
    theme(axis.title.y = element_blank()) +
    theme(axis.text.x=element_blank(), #remove x axis labels
          axis.ticks.x=element_blank(), #remove x axis ticks
          axis.text.y=element_blank(),  #remove y axis labels
          axis.ticks.y=element_blank()  #remove y axis ticks
    ) +
    labs(color = "")
  
  ggsave(paste(path,"/Maps/",attr,"Slope/",substr(file,1,2),".png",sep=""),
           width = 9, height =6)
  
}

#Overall
path ="C:/Users/mrahim6/OneDrive - Louisiana State University/Papers/Temperature trend/Paper 1/Mann-Kendall"
attr = "TempDifferenceAverage"
setwd(paste(path,"/Analysis/",attr,sep=""))

df <- fread("OverallTrendAnalysis.csv")
colnames(df) = c('x','y','rho','pval','Slope','MK')
df$quality <- with(df, ifelse((pval < 0.05 & rho < 0), "Significantly Descreasing (p-value= 0.05)",
                              ifelse(pval > 0.05 & pval < 0.1 & rho < 0, "Significantly Descreasing (p-value= 0.10)",
                                     ifelse(pval < 0.05 & rho > 0, "Significantly Increasing (p-value= 0.05)",
                                            ifelse(pval > 0.05 & pval < 0.1  & rho > 0, "Significantly Increasing (p-value= 0.10)", "Insignificant")))))


ggplot(df, aes(x=x, y=y, color = factor(quality))) +
  geom_scattermore(pointsize=0) +
  scale_color_manual(values=c('grey','#02476e','#bdd2fd','#720000','#e1972e')) +
  theme_bw()  +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(axis.text.x=element_blank(), #remove x axis labels
        axis.ticks.x=element_blank(), #remove x axis ticks
        axis.text.y=element_blank(),  #remove y axis labels
        axis.ticks.y=element_blank()  #remove y axis ticks
  )+
  labs(color = "") +
  theme(legend.text = element_text(size=9)) + 
  theme(legend.position="bottom") +
  guides(color = guide_legend(nrow = 2, byrow = TRUE))
        
ggsave(paste(path,"/Maps/",attr,"/Overall Trend.png",sep=""),
       width = 9, height =6)

#title = 'Overall Slope (1981-2020)'
ggplot(df, aes(x=x, y=y, color = Slope)) +
  geom_scattermore() +
  scale_color_viridis_c(option = "turbo") +

  theme_bw()  +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(axis.text.x=element_blank(), #remove x axis labels
        axis.ticks.x=element_blank(), #remove x axis ticks
        axis.text.y=element_blank(),  #remove y axis labels
        axis.ticks.y=element_blank()  #remove y axis ticks
  ) +
  labs(color = "")
  #theme(plot.margin = unit(c(1,1,1,1), "cm")) +

ggsave(paste(path,"/Maps/",attr,"/Overall Slope.png",sep=""),
       width = 9, height =6)
