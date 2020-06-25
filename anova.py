# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:07:23 2020

@author: hauke
"""
from scipy.stats import f
import pingouin as pg
import pandas as pd
import numpy as np
import seaborn as sns
np.random.seed(1993)
def cohens_d(mean1,mean2,sd1,sd2,n1,n2):
    mean_diff = mean2 -mean1
    denom1 = (((n1-1)*sd1) + ((n2-1)*sd2)) / (n1+n2-2)
    fin = mean_diff / denom1
    return fin

### 3 treatment groups

one = np.random.normal(12,9,35)
two = np.random.normal(15,9,35)
three = np.random.normal(17.5,9,35)
group = np.append(np.full(len(one),1), [np.full(len(one),2), np.full(len(one),3)])
dict_dat = {'data': np.append(one, [two, three]),
            'group' : group}

data = pd.DataFrame(data = dict_dat)

### Store data as csv
data.to_csv(r'data.csv')

### Plot_Data

sns.kdeplot(data = one)
sns.kdeplot(data = two)
sns.kdeplot(data = three)
sns.kdeplot(data = np.append(one, [two, three]))

res = pg.anova(data=data, dv='data', between='group', ss_type=2, detailed=True, effsize='np2')

### ANOVA
m_1 , var_1, sd_1 = np.mean(one), np.var(one), np.std(one)
m_2 , var_2, sd_2 = np.mean(two), np.var(two), np.std(two)
m_3 , var_3, sd_3 = np.mean(three), np.var(three), np.std(three)
m_tot , var_tot = data['data'].mean(), data['data'].var()

n_obs = len(one)
sq_tot = ((dict_dat['data'] - dict_dat['data'].mean())**2).sum()
var_dep = sq_tot / (len(dict_dat['data']))
sqa = 35*np.sum((m_tot - m_1)**2)+35*np.sum((m_tot - m_2)**2)+35*np.sum((m_tot - m_3)**2)
sqr = (n_obs-1) * var_1 + (n_obs-1) * var_2 + (n_obs-1) * var_3

mqa = (1/2) * sqa
mqr = (1/(35*3-3)) * sqr
f_val = mqa/mqr
pval = 1-f.cdf(f_val,2,102)

### Eta-Squared
eta_sq_uncorr = sqa/sq_tot

### Omega Squared

omg_sq = (f_val-1) / (f_val+ (((35*3)-3)) / (3-1))
### Cohens D
cohens_d_12 = cohens_d(m_1,m_2,sd_1,sd_2,n_obs,n_obs)
cohens_d_23 = cohens_d(m_2,m_3,sd_1,sd_3,n_obs,n_obs)
cohens_d_31 = cohens_d(m_3,m_1,sd_3,sd_1,n_obs,n_obs)

#Hedges G
