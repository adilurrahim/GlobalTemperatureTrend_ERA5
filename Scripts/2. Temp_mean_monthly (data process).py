import pandas as pd
import os
import numpy as np

attributes = ['minmaxmean','meanhourly']
years = [i for i in range(1981,2021)]
path = "Processed_Data/"

for attr in attributes:
    for year in years:
        dates = os.listdir(path+str(year))       
        dates_avg = [i for i in dates if attr in i]
        if len(dates_avg)==365:
            months = [dates_avg[0:31],dates_avg[31:59],dates_avg[59:90],dates_avg[90:120],dates_avg[120:151],dates_avg[151:181],dates_avg[181:212],dates_avg[212:243],dates_avg[243:273],dates_avg[273:304],dates_avg[304:334],dates_avg[334:]]
        if len(dates_avg)==366:
            months = [dates_avg[0:31],dates_avg[31:60],dates_avg[60:91],dates_avg[91:121],dates_avg[121:152],dates_avg[152:182],dates_avg[182:213],dates_avg[213:244],dates_avg[244:274],dates_avg[274:305],dates_avg[305:335],dates_avg[335:]]
        
        for month in months:
            df = pd.read_csv(path+str(year)+'/'+month[0])
            df2 = df[['x','y']]
            df = df.drop(['x','y'],axis=1)
            for mnt in month[1:]:
                df1 = pd.read_csv(path+str(year)+'/'+mnt)
                df = pd.concat([df,df1[df1.columns[2]]],axis=1)
            df2['MeanTemp'] = df.mean(axis=1)
            df2.to_csv(attr+'/'+mnt[5:7]+'/'+str(year)+'.csv',index=False)        
    
##Difference between two approach 
years = [i for i in range(1981,2021)]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

for mnt in months:
    year = years[0]
    df_avg = pd.read_csv('meanhourly/'+mnt+'/'+str(year)+'.csv')
    df2 = df_avg[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv('meanhourly/'+mnt+'/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    df_avg = df_avg.drop(['MeanTemp'],axis=1)   
    df_avg['MeanTemp'] = df2.mean(axis=1)
    
    year = years[0]
    df_mean = pd.read_csv('minmaxmean/'+mnt+'/'+str(year)+'.csv')
    df2 = df_mean[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv('minmaxmean/'+mnt+'/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    df_mean = df_mean.drop(['MeanTemp'],axis=1)   
    df_mean['MeanTemp'] = df2.mean(axis=1)
       
    df3 = df_mean[['x','y']]
    df3['TempDiff'] = df_mean['MeanTemp'] - df_avg['MeanTemp']
    df3.to_csv('Difference_1981_2020_'+mnt+'.csv',index=False)
    
#####################################
#latitude wise mean calculation
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

list1 = []
for mnt in months:
    df = pd.read_csv(path+'/differences/Difference_1981_2020_'+mnt+'.csv')
    list1.append([max(df['TempDiff']), min(df['TempDiff']), latitude_mean(df)])
        
df1 = pd.DataFrame(list1)
df1.columns = ['Max','Min','Average']
df1.to_csv(path+'/Table3.csv',index=False)
#####################################
#Temperature change to 2011-2020 over 1981-1990
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
attributes = ['minmaxmean','meanhourly']

for attr in attributes:
    for mnt in months:
        years = [i for i in range(2011,2021)]
        year = years[0]
        df_avg = pd.read_csv(attr+'/'+mnt+'/'+str(year)+'.csv')
        df2 = df_avg[['MeanTemp']]
        for year in years[1:]:
            df1 = pd.read_csv(attr+'/'+mnt+'/'+str(year)+'.csv')
            df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
        df_avg = df_avg.drop(['MeanTemp'],axis=1)   
        df_avg['MeanTemp'] = df2.mean(axis=1)
        df_2011_2020 = df_avg
        
        years = [i for i in range(1981,1991)]
        year = years[0]
        df_avg = pd.read_csv(attr+'/'+mnt+'/'+str(year)+'.csv')
        df2 = df_avg[['MeanTemp']]
        for year in years[1:]:
            df1 = pd.read_csv(attr+'/'+mnt+'/'+str(year)+'.csv')
            df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
        df_avg = df_avg.drop(['MeanTemp'],axis=1)   
        df_avg['MeanTemp'] = df2.mean(axis=1)
        df_1981_1990 = df_avg
        
        df3 = df_1981_1990[['x','y']]
        df3['TempDiff'] = df_2011_2020['MeanTemp'] - df_1981_1990['MeanTemp']      
        df3.to_csv(attr+'/'+mnt+'/TempVariation'+'.csv')

#added code
df1 = pd.DataFrame(list1)
df1.columns = ['Max','Min','Average']
df1.to_csv(path+'/Table3.csv',index=False)
#####################################
