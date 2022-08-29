
import os
import pandas as pd
import numpy as np
import openpyxl
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm

os.chdir('Q:\\')
df = pd.read_csv('synthetic_data.csv')
df = df.sort_values('Default_ind')
df.reset_index(inplace=True,drop=True)
df.index = df.index + 1
print(df)

# Default rate = event incidence (0/1 indicator)
# Loss or charge-off rate = balance lost (0/1 multiplied by $ balance)
d = {}
d['Default Rate'] = df['Default_ind'].sum()/df['Default_ind'].count()
d['Charge-off Rate'] = (df['Face_amt']*df['Default_ind']).sum()/df['Face_amt'].sum()
print(d)

# weight = % of portfolio balance per row
df['weight'] = df['Face_amt']/df['Face_amt'].sum()

# Logistic model 
iv = ['x1']
X = np.asarray(sm.add_constant(df[iv]))
y = np.asarray(df['Default_ind'])
model = sm.GLM(endog=y, exog=X, family=sm.families.Binomial())
result = model.fit()
print(result.summary())

y_hat = result.predict(X)
predProb = np.vstack((y_hat,1-y_hat)).T
V = np.diagflat(np.product(predProb,axis=1))
covLogit = np.linalg.inv(X.T @ V @ X)
print("Standard errors: ", np.sqrt(np.diag(covLogit)))

df['LL'] = ((df['Default_ind']*np.log(df['y_hat'])) + ((1-df['Default_ind'])*np.log(1-df['y_hat'])))
df['LL'].sum()
result.llf

# Balance-weighted logistic model
#   - Estimated on default event indicator re-weighted by % balance to output loss rate
iv = ['x1']
X = np.asarray(sm.add_constant(df[iv]))
y = np.asarray(df['Default_ind'])
w = np.asarray(df['weight'])
model = sm.GLM(endog=y, exog=sm.add_constant(x), family=sm.families.Binomial(),freq_weights=w)
result = model.fit()
print(result.summary())

y_hat = result.predict(X)
predProb = np.vstack((y_hat,1-y_hat,w)).T
V = np.diagflat(np.product(predProb,axis=1))
covLogit = np.linalg.inv(X.T @ V @ X)
print("Weighted standard errors: ", np.sqrt(np.diag(covLogit)))