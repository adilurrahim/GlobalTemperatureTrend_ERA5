import pandas as pd
#from dask import dataframe as dd
import os
import numpy as np


years = [i for i in range(2015,2021)]
path = "D:/Processed_Data/"
for year in years:
    dates = os.listdir(path+str(year))
    dates_avg = [i for i in dates if 'average' in i]
    df = pd.read_csv(path+str(year)+'/'+dates_avg[0])
    df2 = df[['x','y']]
    
    if year == 1986:
        df = df.drop(['x','y'],axis=1)
    else:
        df = df.drop(['x','y','Above','Below','Equal'],axis=1)
    
    for date in dates_avg[1:]:
        df1 = pd.read_csv(path+str(year)+'/'+date)
        df = pd.concat([df,df1[df1.columns[2]]],axis=1)
    
    df2['MeanTemp'] = df.mean(axis=1)
    df2.to_csv(r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceAverage'+'/'+str(year)+'.csv',index=False)        



# years = [i for i in range(1991,2011)]
# path = "D:/Processed_Data/"
# for year in years:
#     dates = os.listdir(path+str(year))
#     dates_avg = [i for i in dates if 'average' in i]
#     df = pd.read_csv(path+str(year)+'/'+dates_avg[0])
#     df2 = df[['x','y']]
#     df = df.drop(['x','y','Above','Below','Equal'],axis=1)
#     for date in dates_avg[1:]:
#         df1 = pd.read_csv(path+str(year)+'/'+date)
#         df = pd.concat([df,df1[df1.columns[2]]],axis=1)
    
#     df2[['MeanTemp']] = run_rowwise_loop(df)
#     df2.to_csv(r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifference'+'/'+str(year)+'.csv',index=False)        



##average 1981-1990, 2011-2020
path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceAverage'
years = [i for i in range(1981,1991)]
year = years[0]
df = pd.read_csv(path+'/'+str(year)+'.csv')
df2 = df[['MeanTemp']]
for year in years[1:]:
    df1 = pd.read_csv(path+'/'+str(year)+'.csv')
    df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)

df = df.drop(['MeanTemp'],axis=1)
df['MeanTemp'] = df2.mean(axis=1)
df.to_csv(path+'/'+str(years[0])+'-'+str(years[-1])+'.csv',index=False)
    


path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceMean'

df_1981_1990 = pd.read_csv(path+'/'+'1981-1990.csv')
df_2011_2020 = pd.read_csv(path+'/'+'2011-2020.csv')


df1 = df_1981_1990[['x','y']]

df1['TempDiff'] = df_2011_2020['MeanTemp'] - df_1981_1990['MeanTemp']

min(df1['TempDiff'])
max(df1['TempDiff'])

def latitude_mean(dataframe):
    latitudes = [i for i in dataframe['y'].unique()]
    list1=[]
    for latitude in latitudes:
        df1 = dataframe.loc[dataframe['y']==latitude].copy()
        avg_temp = np.mean(df1[df1.columns[2]])
        list1.append([latitude,avg_temp])       
    sample_df = pd.DataFrame(list1)    
    sample_df.columns = ['Latitude', 'Avg. Temperature'] 
    sample_df['Scaling'] = np.cos(sample_df['Latitude']*(np.pi/180))
    sample_df['Scaled Temperature'] = sample_df['Scaling'] * sample_df['Avg. Temperature']   
    final_temp = sum(sample_df['Scaled Temperature'])/ sum(sample_df['Scaling'])
    return final_temp

latitude_mean(df1)

df1.to_csv(path+'/Difference.csv',index=False)

###################################################################

path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceMean'

years = [i for i in range(1981,2021)]

df = pd.read_csv(path+'/'+str(years[0])+'.csv')
df = df[df.columns[2]]
for year in years[1:]:
    df1 = pd.read_csv(path+'/'+str(year)+'.csv')
    df = pd.concat([df,df1[df1.columns[2]]],axis=1)

    
from scipy import stats
import pymannkendall as mk
year = [i for i in range(1981,2021)]
def run_rowwise_loop(row):
    rho,pval = stats.spearmanr(row,year)
    trend = mk.original_test(row)
    #return ([rho,pval,trend.slope,trend.p])
    return pd.Series({'C':rho,'D':pval,'E':trend.slope,'F':trend.p})

df2 = pd.DataFrame()
df2[['Spearman rho','Spearman pval','Slope','MK pval']] = df.apply(run_rowwise_loop, axis=1)
#df2 = df.apply(lambda x: run_rowwise_loop(x),axis=1)


df3 = pd.concat([df1[['x','y']],df2],axis=1)
df3.to_csv(path+'/OverallTrendAnalysis.csv',index=False)



##################################################################
path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceMean'
df_mean = pd.read_csv(path+'/'+'Difference.csv')

path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\TempDifferenceAverage'
df_average = pd.read_csv(path+'/'+'Difference.csv')

df = df_mean[['x','y']]
df['TempDiff'] = df_mean['TempDiff'] - df_average['TempDiff']

path = r"C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis"
df.to_csv(path+'/Difference_mean_avg.csv',index=False)











