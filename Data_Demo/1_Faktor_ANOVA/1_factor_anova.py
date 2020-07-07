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
import matplotlib.pyplot as plt

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

### Plot Sample Data
measurement =sns.kdeplot(DATA_anova['data'].loc[DATA_anova['group']==1])
measurement =sns.kdeplot(DATA_anova['data'].loc[DATA_anova['group']==2])
measurement =sns.kdeplot(DATA_anova['data'].loc[DATA_anova['group']==3])
figure_measure = measurement.get_figure() 
figure_measure.savefig(r"C:\Users\de_hauk\PowerFolders\EXPRA_Peper_SS_2020\Daten\measurement.png")
plt.clf()
#Plot H0

h_0 = sns.kdeplot(np.random.normal(((460+445+450)/3),25,size_group*3))
figure_h0 = h_0.get_figure() 
figure_h0.savefig(r"C:\Users\de_hauk\PowerFolders\EXPRA_Peper_SS_2020\Daten\h_0.png")
plt.clf()
#Plot H1
h_1 =sns.kdeplot(np.random.normal(450,5,size_group))
h_1 =sns.kdeplot(np.random.normal(445,5,size_group))
h_1 =sns.kdeplot(np.random.normal(460,5,size_group))
figure_h1 = h_1.get_figure() 
figure_h1.savefig(r"C:\Users\de_hauk\PowerFolders\EXPRA_Peper_SS_2020\Daten\h_1.png")
plt.clf()

sns_plot = sns.catplot(x="group", y="data", data=DATA_anova)

eq_var = pg.homoscedasticity(DATA_anova, dv='data', group='group', method='levene', alpha=0.05)
aov = pg.anova(dv='data', between='group', data=DATA_anova,
               detailed=True)

ss_total = ((DATA_anova['data'] - DATA_anova['data'].mean())**2).sum()
eta_2 = 5248 / ss_total
# DATA_anova.to_csv(r'DATA_1F_anova.csv', sep= ',')
# sns_plot.savefig("1F_anova_dat.png")


