#Extracting daily data using minmaxmean and meanhourly approach

#install required packages
#install.packages(c("raster","matrixStats","data.table"))
library(raster)
library(matrixStats)
library(data.table)

#load in the hourly ERA5 data, process, and save csv files
df = brick('data.nc')

z = length(df@z[["Date/time"]])
for (i in seq(1,z,24)){
  df1 = as.data.frame(df[[i]],xy=T)
  df2 = na.omit(df1)
  for (j in (i+1):(i+23)){
    df1 = as.data.frame(df[[j]])
    df2 = cbind(df2,na.omit(df1))
  }
  
  df3 = as.data.frame(rowMeans(df2[3:26]))
  df4 = cbind(df2[1:2],df3)
  filename = paste(substr(names(df1),2,11),'_meanhourly_data.csv',sep="")
  fwrite(df4,filename,row.names=F)
  
  df3$Mins = rowMins(as.matrix(df2[3:26]))
  df3$Maxs = rowMaxs(as.matrix(df2[3:26]))
  df3$mean = (df3$Mins+df3$Maxs)/2
  df4 = cbind(df2[1:2],df3$mean)
  filename = paste(substr(names(df1),2,11),'_minmaxmean_data.csv',sep="")
  fwrite(df4,filename,row.names=F)
}  
