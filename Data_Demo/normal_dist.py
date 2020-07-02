# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:17:26 2020

@author: de_hauk
"""

import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import scipy
from scipy import stats

np.random.seed(1993)

data = np.random.normal(455,10,25) + np.random.normal(400,100)
data_norm = np.random.normal(455,10,100)

res_norm = pg.anderson(data, dist='norm')
res_norm_1 = stats.anderson(data, dist='norm')
res_norm_2 = stats.shapiro(data)

#sns.kdeplot(data_norm)
data_norm_M,data_norm_SD,data_norm_VAR = data_norm.mean(),data_norm.std(),data_norm.var()
data_nrom_res = pg.anderson(data_norm, dist='norm')
pdf_res = stats.norm.pdf(421,455,10) #.pdf(421)
pdf_res1 = stats.norm.pdf(454,455,10)

sum_prob = []

for i in np.linspace(420,490,1000):
    sum_prob.append(((i, np.around((1/10)*stats.norm.pdf(i,455,10),decimals = 5))))

data_plot = pd.DataFrame(sum_prob, columns = ['a','b'])
hhhh = np.sum(data_plot['b'])
sns.lineplot(x = data_plot['a'],y = data_plot['b'])



# ffff = np.sum(sum_prob)
sum_1 = np.sum(np.array(sum_prob)/np.sum(sum_prob))

example = [1,2,2,3,5,7,9]
sum_sq = np.sum([(i-np.mean(example))**2 for i in example])
var_ = pd.Series(example).std()





