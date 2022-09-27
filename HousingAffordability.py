
import os
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib import ticker

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

plt.rcParams["font.family"] = "arial"
plt.style.use('seaborn-whitegrid')

os.chdir('C:\\Users\\Michael\\Desktop')
fig,axes=plt.subplots(2,2)
i = 0 
while i < 3:
    ax = axes.flat[i]
    ax.plot(df.iloc[:,i+1])
    ax.set_title(df.columns[i+1])
    i += 1
ax = axes.flat[i]
ax.axis('off')
plt.tight_layout()
plt.savefig('test_plot.png')

price = 0.8*df['MSPUS']
rate = df['MORTGAGE30US']/100
i = rate/12
term = 30
n = term*12
df['monthly_pmt'] = (price*(((i)*(1+i)**n)/(((1+i)**n)-(1))))
df['annual_pmt'] = df['monthly_pmt']*12
df['all_in_cost'] = (price*(((i)*(1+i)**n)/(((1+i)**n)-(1))))*n + 0.2*df['MSPUS']
df['pct_housing_costs'] = df['annual_pmt']/df['MEHOINUSA646N']

fig,ax = plt.subplots(1,1,dpi=500)
fig.set_size_inches(6, 4)
fig.suptitle('Mortgage Payment as % Income')
ax.plot(df.pct_housing_costs,c='navy')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=0))
plt.savefig('test.png')
