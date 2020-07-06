# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:51:37 2020

@author: de_hauk
"""

import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import scipy
from scipy import stats

np.random.seed(1993)

n_groups=3
size_group = 40
size_sample = n_groups * size_group
group1 = np.random.normal(450,25,size_group)
group1_id = np.full(size_group,1)
group2 = np.random.normal(445,25,size_group)
group2_id = np.full(size_group,2)
group3 = np.random.normal(460,25,size_group)
group3_id = np.full(size_group,3)


data_var = np.append(group1,[group2,group3])
group_var = np.append(group1_id,[group2_id,group3_id])
DATA_anova = pd.DataFrame()
DATA_anova['data'] = data_var
DATA_anova['group'] = group_var
sns_plot = sns.catplot(x="group", y="data", data=DATA_anova)

eq_var = pg.homoscedasticity(DATA_anova, dv='data', group='group', method='levene', alpha=0.05)
aov = pg.anova(dv='data', between='group', data=DATA_anova,
               detailed=True)

DATA_anova.to_csv(r'DATA_1F_anova.csv', sep= ',')
sns_plot.savefig("1F_anova_dat.png")


