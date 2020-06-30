# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:53:52 2020

@author: de_hauk
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools as it
fig, axs = plt.subplots(2,2,sharey = True)

groups = {1:'naive, neutral',
          2:'instruiert, neutral',
          3:'naive, negativ',
          4:'instruiert, negativ'}
block_cond = {0:'no malingering',
              1:'malingering'}
trial_type = {1:'AX',
              2:'BX',
              3:'AY',
              4:'BY'}
data_plot = pd.read_csv(r'C:\Users\de_hauk\Desktop\data.csv', sep=',' )
indxs = [i for i in it.product([0,1],repeat = 2)]

for group,index in zip(range(1,5),indxs):
    a_ind, b_ind = index[0],index[1]
    dat_curr = data_plot.loc[data_plot['BS_group'] == group]
    dat_curr['block_cond'] = dat_curr['block_cond'].replace(block_cond).copy()
    #sns.catplot(data = dat_curr, x = 'block_cond',y = 'mean', hue = 'trial_type',kind = 'box', ax = axs[a_ind,b_ind], palette="Blues_d")
    aaa = sns.pointplot(data = dat_curr, x = 'trial_type' ,y = 'mean', hue = 'block_cond',ci = 95,n_boot=5000, ax = axs[a_ind,b_ind],)
    #bbb = sns.swarmplot(data = dat_curr, x = 'block_cond',y = 'mean', hue = 'trial_type',dodge = True, ax = aaa.ax, palette="Blues_d")
    title = groups[group]
    axs[a_ind,b_ind].set_title(title)
    axs[a_ind,b_ind].set_xticklabels([trial_type[1],trial_type[2],trial_type[3],trial_type[4]])
    #axs[a_ind,b_ind].legend([block_cond[1],block_cond[2]])

#sns.violinplot(data= data_plot,order =data_plot['trial_type'],  palette="Set3", bw=.2, cut=1, linewidth=1)
