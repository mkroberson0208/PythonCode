# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 09:12:11 2021

@author: Michael
"""
import os
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "arial"
plt.style.use('seaborn-whitegrid')
plt.rcParams["legend.frameon"] = True

def read_multiple(l: list):
    my_api = '499659ea0d975475c7302585ae1c6d7a'
    tmp = pd.DataFrame()
    tmp['date'] = None
    for series_id in l:
        args_url = {'series_id':series_id,'api_key':my_api,'file_type':'json'}
        req = requests.get('https://api.stlouisfed.org/fred/series/observations',params=args_url)
        data = req.json()
        df = pd.DataFrame.from_dict(data['observations'])
        df['value'] = df['value'].replace({'.':'0'}).astype(float)
        df['value'] = df['value'].replace(0,np.nan)
        df = df.rename(columns={'value':series_id})
        tmp = tmp.merge(df[['date',series_id]],on='date',how='outer')
    return tmp

test = ['MSPUS','MORTGAGE30US','MEHOINUSA646N']
df = read_multiple(test)
df.index = pd.to_datetime(df['date'])
df = df.sort_index()
df = df.fillna(method='ffill')

os.chdir('C:\\Users\\Michael\\Desktop')
for c in df.columns[1:]:
    print(c)
    df_plot = df[c].dropna()
    fig,ax=plt.subplots(1,1)
    ax.plot(df_plot.index,df_plot)
    plt.savefig(str(c)+'_plot.png')
    
price = 0.8*df['MSPUS']
rate = df['MORTGAGE30US']/100
i = rate/12
term = 30
n = term*12

df['monthly_pmt'] = (price*(((i)*(1+i)**n)/(((1+i)**n)-(1))))
df['annual_pmt'] = df['monthly_pmt']*12
df['all_in_cost'] = (price*(((i)*(1+i)**n)/(((1+i)**n)-(1))))*n + 0.2*df['MSPUS']
df['pct_housing_costs'] = df['annual_pmt']/df['MEFAINUSA646N']

