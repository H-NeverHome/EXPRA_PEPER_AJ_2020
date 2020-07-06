# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:27:55 2020

@author: de_hauk
"""

import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import scipy
from scipy import stats

np.random.seed(1993)

n_times = 2

#### F1
n_groups=3
size_group = 40
size_sample = n_groups * size_group
group1 = np.random.normal(450,25,size_group)
group1_id = np.full(size_group,1)
group2 = np.random.normal(445,25,size_group)
group2_id = np.full(size_group,2)
group3 = np.random.normal(460,25,size_group)
group3_id = np.full(size_group,3)

#### F2
gender = np.random.binomial(1,0.44,size_sample)

# #### F3
# educ = np.random.randint(1, high=5, size=size_sample)

#### DATA
data_var = np.append(group1,[group2,group3])
group_var = np.append(group1_id,[group2_id,group3_id])
DATA_anova = pd.DataFrame()
DATA_anova['data'] = data_var
DATA_anova['group'] = group_var
DATA_anova['gender'] = gender
#DATA_anova['educ'] = educ
sns_plot = sns.catplot(x="group", y="data", hue='gender', data=DATA_anova)

aov_2F = pg.anova(dv='data', between=['group','gender'], data=DATA_anova,
               detailed=True)

DATA_anova.to_csv(r'DATA_2F_anova.csv', sep= ',')