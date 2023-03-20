import pandas as pd
#from dask import dataframe as dd
import os
import numpy as np


path = r'C:\Users\mrahim6\OneDrive - Louisiana State University\Papers\Temperature trend\Paper 1\Mann-Kendall\Analysis\Temperatures'

months = ['01','02','03','04','05','06','07','08','09','10','11','12']
years = [i for i in range(1981,2021)]

for year in years:
    df_1 = pd.read_csv(path+'/mean/01/'+str(year)+'.csv')
    df_2 = pd.read_csv(path+'/mean/02/'+str(year)+'.csv')
    df_3 = pd.read_csv(path+'/mean/03/'+str(year)+'.csv')
    df_4 = pd.read_csv(path+'/mean/04/'+str(year)+'.csv')
    df_5 = pd.read_csv(path+'/mean/05/'+str(year)+'.csv')
    df_6 = pd.read_csv(path+'/mean/06/'+str(year)+'.csv')
    df_7 = pd.read_csv(path+'/mean/07/'+str(year)+'.csv')
    df_8 = pd.read_csv(path+'/mean/08/'+str(year)+'.csv')
    df_9 = pd.read_csv(path+'/mean/09/'+str(year)+'.csv')
    df_10 = pd.read_csv(path+'/mean/10/'+str(year)+'.csv')
    df_11 = pd.read_csv(path+'/mean/11/'+str(year)+'.csv')
    df_12 = pd.read_csv(path+'/mean/12/'+str(year)+'.csv')
    
    df = df_1[['x','y']]
    df['MeanTemp'] = (df_1[['MeanTemp']]+df_2[['MeanTemp']]+df_3[['MeanTemp']]+df_4[['MeanTemp']]+df_5[['MeanTemp']]+df_6[['MeanTemp']]+
          df_7[['MeanTemp']]+df_8[['MeanTemp']]+df_9[['MeanTemp']]+df_10[['MeanTemp']]+df_11[['MeanTemp']]+df_12[['MeanTemp']])/12
    df.to_csv(path+'/mean/overall/'+str(year)+'.csv',index=False)


months = ['01','02','03','04','05','06','07','08','09','10','11','12']

list1 = []
for mnt in months:
    years = [i for i in range(1981,2021)]
    year = years[0]
    df = pd.read_csv(path+'/average/'+mnt+'/'+str(year)+'.csv')
    df2 = df[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv(path+'/average/'+mnt+'/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    
    df = df.drop(['MeanTemp'],axis=1)
    df['MeanTemp'] = df2.mean(axis=1)
    df_1981_2020_average = df
    
    years = [i for i in range(1981,2021)]
    year = years[0]
    df0 = pd.read_csv(path+'/mean/'+mnt+'/'+str(year)+'.csv')
    df2 = df0[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv(path+'/mean/'+mnt+'/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    
    df0 = df0.drop(['MeanTemp'],axis=1)
    df0['MeanTemp'] = df2.mean(axis=1)
    df_1981_2020_mean = df0
    
    df1 = df_1981_2020_average[['x','y']]
    df1['TempDiff'] = df_1981_2020_mean['MeanTemp'] - df_1981_2020_average['MeanTemp']
    df1.to_csv(path+'/differences/Difference_1981_2020_'+mnt+'.csv',index=False)


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

    list1.append([mnt,min(df1['TempDiff']),max(df1['TempDiff']),latitude_mean(df1)])


df1 = pd.read_csv(path+'/differences/Difference_1981_2020.csv')













