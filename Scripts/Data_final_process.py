import pandas as pd
#from dask import dataframe as dd
import os
import numpy as np
from scipy import stats
from tqdm import tqdm
import time
import pymannkendall as mk

def latitude_mean(dataframe):
    latitudes = [i for i in dataframe['y'].unique()]
    list1=[]
    for latitude in latitudes:
        df1 = dataframe.loc[dataframe['y']==latitude].copy()
        avg_temp = np.mean(df1[df1.columns[2]])
        avg_above = np.mean(df1[df1.columns[3]])
        avg_below = np.mean(df1[df1.columns[5]])
        list1.append([latitude,avg_temp,avg_above,avg_below])       
    sample_df = pd.DataFrame(list1)    
    sample_df.columns = ['Latitude', 'Avg. Temperature','Above','Below'] 
    sample_df['Scaling'] = np.cos(sample_df['Latitude']*(np.pi/180))
    sample_df['Scaled Temperature'] = sample_df['Scaling'] * sample_df['Avg. Temperature']   
    sample_df['Scaled Above'] = sample_df['Scaling'] * sample_df['Above'] 
    sample_df['Scaled Below'] = sample_df['Scaling'] * sample_df['Below'] 
    final_temp = sum(sample_df['Scaled Temperature'])/ sum(sample_df['Scaling'])
    final_above = sum(sample_df['Scaled Above'])/ sum(sample_df['Scaling'])
    final_below = sum(sample_df['Scaled Below'])/ sum(sample_df['Scaling'])
    return [final_temp,final_above,final_below]

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

path = "D:/Processed_Data/"
year_data = os.listdir(path)
year = year_data[5]
for year in year_data: 
    global_avg = []
    dates = os.listdir(path+year)
    dates_avg = [i for i in dates if 'mean' in i]
    #dates_mean = [i for i in dates if 'mean' in i]
    for data in dates_avg:
        df = pd.read_csv(path+year+'/'+data)
        temp = latitude_mean(df)
        global_avg.append([data[:-4],temp])        
    sample = pd.DataFrame(global_avg) 
    sample.columns = ['Date','Temp']   
    sample.to_csv(path1 +'/'+str(year)+'.csv',index=False)
path1 = r"C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\World_Avg_Mean\ERA 5 data process"    


# dates = os.listdir('D:/Analysis/Second Paper/World_Avg_MeanHourly/YearlyAverage/')
# avg = []
# for date in dates:
#     df = pd.read_csv('D:/Analysis/Second Paper/World_Avg_MeanHourly/YearlyAverage/'+date)
#     avg_temp = round(np.mean(df[df.columns[1]]),4)
#     avg_above = round(np.mean(df[df.columns[2]]),4)
#     avg_below = round(np.mean(df[df.columns[3]]),4)
#     avg.append([date[:-4],avg_temp,avg_above,avg_below])
    
# df = pd.DataFrame(avg)    
# df.columns = ['Year','Average','Above','Below']  
# df.to_csv('D:/Analysis/Second Paper/World_Avg_MeanHourly/Annual_avg.csv',index=False)


# rho, pval = stats.spearmanr(df['Average'],df['Year'])
# rho, pval = stats.spearmanr(df['Above'],df['Year'])
# rho, pval = stats.spearmanr(df['Below'],df['Year'])


df = pd.read_csv (r"C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\World_Avg_Mean"+"/Annual_mean.csv")

df1 = df.set_index('Year')
#df1.drop(['Year'], axis=1, inplace=True)
trend = mk.original_test(df1)
pval,slope = trend[2],trend[7]


######Monthly 
#define function
year = [i for i in range(1981,2021)]
# def spearman_rowwise(x):
#     rho,pval = stats.spearmanr(x,year)
#     return rho,pval
def mannkendall_rowwise(x):
    trend = mk.original_test(x)
    pval,slope = trend.p,trend.slope
    return slope,pval

def run_rowwise_loop(df):
    Cs, Ds = [],[]
    for _,row in df.iterrows():
        c,d, = mannkendall_rowwise(row)
        Cs.append(c)
        Ds.append(d)
    return pd.Series({'C':Cs,'D':Ds})

mnt = ['01','02','03','04','05','06','07','08','09','10','11','12']
mnt = ['10','11']

path = "D:/Processed_Data/"
for mn in mnt:
    dates = os.listdir(path+'1981')
    dates_avg = [i for i in dates if 'mean' in i]
    months = [i for i in dates_avg if mn in i[5:7]]
    month_df = []
    for month in months:
        df = pd.read_csv(path+'1981/'+month)
        month_df.append(df[df.columns[2]])
    df1 = sum(month_df) / len(month_df)
    for yr in year[1:]:
        dates = os.listdir(path+str(yr))
        dates_avg = [i for i in dates if 'mean' in i]
        months = [i for i in dates_avg if mn in i[5:7]]
        month_df = []
        for month in months:
            df = pd.read_csv(path+str(yr)+'/'+month)
            month_df.append(df[df.columns[2]])
        df2 = sum(month_df) / len(month_df)
        df1 = pd.concat([df1,df2],axis=1)    
    df3 = df[['x','y']]
    df3[['slope','pval']] = run_rowwise_loop(df1)
    df3.to_csv(r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\Monthly_Mean'+'/'+mn+'.csv',index=False)        
 
    

######Julian days 
path = "E:/Processed_Data/"
year_data = os.listdir(path)
year_data = year_data[1:]     


dates = os.listdir(path+'1981')
dates_avg = [i for i in dates if 'average' in i]

#define function
year = [i for i in range(1981,2021)]
def spearman_rowwise(x):
    rho,pval = stats.spearmanr(x,year)
    return rho,pval
def run_rowwise_loop(df):
    Cs, Ds = [],[]
    for _,row in df.iterrows():
        c,d, = spearman_rowwise(row)
        Cs.append(c)
        Ds.append(d)
    return pd.Series({'C':Cs,'D':Ds})

dat = 172
for dat in tqdm(range(172,len(dates_avg))):
    data = dates_avg[dat]
    dt = data[5:10]
    df = pd.read_csv(path+'1981/'+data)
    #df = df.drop(['Above','Equal','Below'],axis=1)
    df1 = df[[df.columns[3]]]
    df2 = df[[df.columns[5]]]
    for years in year_data:
       dates_ = os.listdir(path+years)
       dates_avg_ = [i for i in dates_ if 'average' in i]
       dt_ = [i for i in dates_avg_ if dt==i[5:10]][0]
       df3 = pd.read_csv(path+years+'/'+dt_)
       df1 = pd.concat([df1,df3[df3.columns[3]]],axis=1)
       df2 = pd.concat([df2,df3[df3.columns[5]]],axis=1)
    #df2 = df.drop(['x','y'],axis=1)
    df6 = df[['x','y']]
    df6[['rho','pval']] = run_rowwise_loop(df1)
    df7 = df[['x','y']]
    df7[['rho','pval']] = run_rowwise_loop(df2)
     
    df6.to_csv('E:/Analysis/Second Paper/Julian_Day_Avg/Above/'+data[5:],index=False)        
    df7.to_csv('E:/Analysis/Second Paper/Julian_Day_Avg/Below/'+data[5:],index=False)     
   
######################Monthly overall
#path = "D:/Analysis/Second Paper/World_Avg_MeanHourly/YearlyAverage/"
path = r"C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\World_Avg_Average\ERA 5 data process"    

years = os.listdir(path)

jan = []
feb= []
mar = []
apr = []
may = []
june = []
july = []
aug = []
sep = []
octo = []
nov = []
dec = []


for year in years:
    if year[:-4]== '1986':
        parameter = 'Temp'
    else:
        parameter = 'Average'
    df = pd.read_csv(path+'/'+year)
    jan.append(np.mean(df[0:31][parameter]))
    
    if len(df)==365:
        feb.append(np.mean(df[31:59][parameter]))
        mar.append(np.mean(df[59:90][parameter]))
        apr.append(np.mean(df[90:120][parameter]))
        may.append(np.mean(df[120:151][parameter]))
        june.append(np.mean(df[151:181][parameter]))
        july.append(np.mean(df[181:212][parameter]))
        aug.append(np.mean(df[212:243][parameter]))
        sep.append(np.mean(df[243:273][parameter]))
        octo.append(np.mean(df[273:304][parameter]))
        nov.append(np.mean(df[304:334][parameter]))
        dec.append(np.mean(df[334:][parameter]))
    if len(df)==366:
        feb.append(np.mean(df[31:60][parameter]))
        mar.append(np.mean(df[60:91][parameter]))
        apr.append(np.mean(df[91:121][parameter]))
        may.append(np.mean(df[121:152][parameter]))
        june.append(np.mean(df[152:182][parameter]))
        july.append(np.mean(df[182:213][parameter]))
        aug.append(np.mean(df[213:244][parameter]))
        sep.append(np.mean(df[244:274][parameter]))
        octo.append(np.mean(df[274:305][parameter]))
        nov.append(np.mean(df[305:335][parameter]))
        dec.append(np.mean(df[335:][parameter]))



df = pd.DataFrame()

df['Dates'] = [i for i in range(1981,2021)]

df['January'] = jan
df['February'] = feb
df['March'] = mar
df['April'] = apr
df['May'] = may
df['June'] = june
df['July'] = july
df['August'] = aug
df['September'] = sep
df['October'] = octo
df['November'] = nov
df['December'] = dec

df.to_csv(path[:-18]+"/Monthly/months_data.csv",index=False)

list1 = []
for i in range(1,13):
    rho, pval = stats.spearmanr(df[df.columns[i]],df['Dates'])
    trend = mk.original_test(df[df.columns[i]])
    pval1,slope = trend[2],trend[7]
    list1.append([rho, pval, slope, pval1])
    
df1 = pd.DataFrame(list1)
df1.columns = ['Spearman rho', 'Spearman p-value', 'Thei-Sen Slope', 'MK p-value']
df1.to_csv(path[:-18]+"/Monthly/months_trend.csv",index=False)


