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
### 3 treatment groups

one = np.random.normal(12,9,35)
two = np.random.normal(15,9,35)
three = np.random.normal(17.5,9,35)
group = np.append(np.full(len(one),1), [np.full(len(one),2), np.full(len(one),3)])
dict_dat = {'data': np.append(one, [two, three]),
            'group' : group}

data = pd.DataFrame(data = dict_dat)

sns.kdeplot(data = one)
sns.kdeplot(data = two)
sns.kdeplot(data = three)
sns.kdeplot(data = np.append(one, [two, three]))

res = pg.anova(data=data, dv='data', between='group', ss_type=2, detailed=True, effsize='np2')

### ANOVA
m_1 , var_1 = np.mean(one), np.var(one)
m_2 , var_2 = np.mean(two), np.var(two)
m_3 , var_3 = np.mean(three), np.var(three)
m_tot , var_tot = data['data'].mean(), data['data'].var()

n_obs = len(one)
sqa = 35*np.sum((m_tot - m_1)**2)+35*np.sum((m_tot - m_2)**2)+35*np.sum((m_tot - m_3)**2)
sqr = (n_obs-1) * var_1 + (n_obs-1) * var_2 + (n_obs-1) * var_3

mqa = (1/2) * sqa
mqr = (1/(35*3-3)) * sqr
f_val = mqa/mqr
pval = 1-f.cdf(f_val,2,102)

