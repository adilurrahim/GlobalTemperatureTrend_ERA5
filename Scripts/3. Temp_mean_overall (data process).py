import pandas as pd

attributes = ['minmaxmean','meanhourly']


years = [i for i in range(1981,2021)]
for attr in attributes:
    for year in years:
        df_1 = pd.read_csv(attr+'/01/'+str(year)+'.csv')
        df_2 = pd.read_csv(attr+'/02/'+str(year)+'.csv')
        df_3 = pd.read_csv(attr+'/03/'+str(year)+'.csv')
        df_4 = pd.read_csv(attr+'/04/'+str(year)+'.csv')
        df_5 = pd.read_csv(attr+'/05/'+str(year)+'.csv')
        df_6 = pd.read_csv(attr+'/06/'+str(year)+'.csv')
        df_7 = pd.read_csv(attr+'/07/'+str(year)+'.csv')
        df_8 = pd.read_csv(attr+'/08/'+str(year)+'.csv')
        df_9 = pd.read_csv(attr+'/09/'+str(year)+'.csv')
        df_10 = pd.read_csv(attr+'/10/'+str(year)+'.csv')
        df_11 = pd.read_csv(attr+'/11/'+str(year)+'.csv')
        df_12 = pd.read_csv(attr+'/12/'+str(year)+'.csv')
        
        df = df_1[['x','y']]
        df['MeanTemp'] = (df_1[['MeanTemp']]+df_2[['MeanTemp']]+df_3[['MeanTemp']]+df_4[['MeanTemp']]+df_5[['MeanTemp']]+df_6[['MeanTemp']]+
              df_7[['MeanTemp']]+df_8[['MeanTemp']]+df_9[['MeanTemp']]+df_10[['MeanTemp']]+df_11[['MeanTemp']]+df_12[['MeanTemp']])/12
        df.to_csv(attr+'/overall/'+str(year)+'.csv',index=False)
############################################

##Difference between two approach 
years = [i for i in range(1981,2021)]

year = years[0]
df_avg = pd.read_csv('meanhourly/overall/'+str(year)+'.csv')
df2 = df_avg[['MeanTemp']]
for year in years[1:]:
    df1 = pd.read_csv('meanhourly/overall/'+str(year)+'.csv')
    df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
df_avg = df_avg.drop(['MeanTemp'],axis=1)   
df_avg['MeanTemp'] = df2.mean(axis=1)

year = years[0]
df_mean = pd.read_csv('minmaxmean/overall/'+str(year)+'.csv')
df2 = df_mean[['MeanTemp']]
for year in years[1:]:
    df1 = pd.read_csv('minmaxmean/overall/'+str(year)+'.csv')
    df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
df_mean = df_mean.drop(['MeanTemp'],axis=1)   
df_mean['MeanTemp'] = df2.mean(axis=1)
   
df3 = df_mean[['x','y']]
df3['TempDiff'] = df_mean['MeanTemp'] - df_avg['MeanTemp']
df3.to_csv('Difference_1981_2020_overall.csv',index=False)
#############################################

#Temperature change to 2011-2020 over 1981-1990
for attr in attributes:
    years = [i for i in range(2011,2021)]
    year = years[0]
    df_avg = pd.read_csv(attr+'/overall/'+str(year)+'.csv')
    df2 = df_avg[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv(attr+'/overall/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    df_avg = df_avg.drop(['MeanTemp'],axis=1)   
    df_avg['MeanTemp'] = df2.mean(axis=1)
    df_2011_2020 = df_avg
    
    years = [i for i in range(1981,1991)]
    year = years[0]
    df_avg = pd.read_csv(attr+'/overall/'+str(year)+'.csv')
    df2 = df_avg[['MeanTemp']]
    for year in years[1:]:
        df1 = pd.read_csv(attr+'/overall/'+str(year)+'.csv')
        df2 = pd.concat([df2,df1[df1.columns[2]]],axis=1)
    df_avg = df_avg.drop(['MeanTemp'],axis=1)   
    df_avg['MeanTemp'] = df2.mean(axis=1)
    df_1981_1990 = df_avg
    
    df3 = df_1981_1990[['x','y']]
    df3['TempDiff'] = df_2011_2020['MeanTemp'] - df_1981_1990['MeanTemp']      
    df3.to_csv(attr+'/overall/TempVariation'+'.csv')

