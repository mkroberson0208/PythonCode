
import os
import pandas as pd
import numpy as np
import openpyxl
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
from scipy import stats

os.chdir('H:\\')
df = pd.read_csv('synthetic_data.csv')
df = df.sort_values('Default_ind')
df.reset_index(inplace=True,drop=True)
df.index = df.index + 1
print(df)

d = {}
d['Default Rate'] = df['Default_ind'].sum()/df['Default_ind'].count()
d['Charge-off Rate'] = (df['Face_amt']*df['Default_ind']).sum()/df['Face_amt'].sum()
print(d)

# weight = % of portfolio balance per row
df['weight'] = df['Face_amt']/df['Face_amt'].sum()

# Unweighted logistic regression 
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
std_error = np.sqrt(np.diag(covLogit))
print("Standard errors: ", std_error)

z_score = result.params/std_error
p_values = 2*stats.norm.cdf(-abs(z_score), loc=0, scale=1)

var = ['Intercept'] + iv
list_of_dict = []
for v in var:
    d = {}
    i = var.index(v)
    d['var'] = v
    d['estimate'] = result.params[i]
    d['std_error'] = std_error[i]
    d['z_score'] = z_score[i]
    d['p_value'] = p_values[i]
    list_of_dict += [d]
print(list_of_dict)

chargeoff = ((y*df['Face_amt']).sum())
pred_chargeoff = (y_hat*df['Face_amt']).sum()
pct_error = pred_chargeoff/chargeoff - 1
print(pct_error)

# Balance-weighted logistic regression
iv = ['x1']
X = np.asarray(sm.add_constant(df[iv]))
y = np.asarray(df['Default_ind'])
w = np.asarray(df['weight'])
model = sm.GLM(endog=y, exog=X, family=sm.families.Binomial(),freq_weights=w)
result = model.fit()
print(result.summary())

# Weight vector increases variance of estimate / std. error leading to inaccurate p-values
y_hat = result.predict(X)
predProb = np.vstack((y_hat,1-y_hat,w)).T
V = np.diagflat(np.product(predProb,axis=1))
covLogit = np.linalg.inv(X.T @ V @ X)
std_error = np.sqrt(np.diag(covLogit))
print("Weighted standard errors: ", std_error)

predProb = np.vstack((y_hat,1-y_hat)).T
V = np.diagflat(np.product(predProb,axis=1))
covLogit = np.linalg.inv(X.T @ V @ X)
std_error = np.sqrt(np.diag(covLogit))
print("Unweighted standard errors: ", std_error)

z_score = result.params/std_error
p_values = 2*stats.norm.cdf(-abs(z_score), loc=0, scale=1)

var = ['Intercept'] + iv
list_of_dict = []
for v in var:
    d = {}
    i = var.index(v)
    d['var'] = v
    d['estimate'] = result.params[i]
    d['std_error'] = std_error[i]
    d['z_score'] = z_score[i]
    d['p_value'] = p_values[i]
    list_of_dict += [d]
print(list_of_dict)

chargeoff = ((y*df['Face_amt']).sum())
pred_chargeoff = (y_hat*df['Face_amt']).sum()
pct_error = pred_chargeoff/chargeoff - 1
print(pct_error)
