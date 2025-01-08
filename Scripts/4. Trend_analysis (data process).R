#Trend analysis

#install required packages
#install.packages(c("wql","data.table"))

library(data.table)
library(wql)

rowwise_estimate = function(row){
  year = seq(1981,2020)
  trend = cor.test(row,year,method = "spearman",exact=FALSE)
  trend1 = mannKen(row)
  V = c(trend$estimate,trend$p.value,trend1$sen.slope,trend1$p.value)
  return (V)
}

months =c('01','02','03','04','05','06','07','08','09','10','11','12','overall')
attributes = c('minmaxmean','meanhourly')
years = seq(1981,2020,1)

for (attr in attirbutes){
  for (mnt in months){
    df = fread(paste(attr,'/',mnt,'/',as.character(years[1]),'.csv',sep=""))
    
    for (yr in years[2:40]){
      df1 = fread(paste(attr,'/',mnt,'/',as.character(yr),'.csv',sep=""))
      df = cbind(df,df1[,3])
    }

    df1 = df[,1:2]
    df2 = df[,3:length(df)]
    df3 =  apply(df2, 1, FUN = rowwise_estimate)
    df4 = as.data.frame(t(df3))
    df1 = cbind(df1,df4)
    colnames(df1) = c('x','y','Spearman rho', 'Spearman p-val', 'Theil-sen slope', 'Mannkendall p-val')
    
    fwrite(df1,paste(attr,'/',mnt,'_trend.csv',sep=""))
  }
}

#sample code edited


