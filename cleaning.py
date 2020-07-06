# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:58:39 2020

@author: de_hauk
"""


import pandas as pd
import pingouin as pg
import numpy as np
import os


########## Import Data
data_raw_exp = []
data_raw_bl = []
column_names = ['del1','group','del2','block','del3', 'trial_nr','del4', 'type', 'del5','RT','del6','R_type']
data_raw_total = []
unique_IDs = []
total_dat_BL = pd.DataFrame()
total_dat_EXP = pd.DataFrame()
miss_error = pd.DataFrame()
### Load, name columns, drop irrelevant, split into baseline & experiment  
for file in os.listdir(r"C:\Users\de_hauk\Desktop\New folder"):
    if file.endswith(".txt"):
        path = os.path.join(r"C:\Users\de_hauk\Desktop\New folder", file)
        if 'block' in path:
            vpn_id = file.split('b')[0]
            unique_IDs.append(int(vpn_id))
            dat_raw = pd.read_csv(path,header=None, names = column_names)
            data_proc = dat_raw.drop(axis=1,labels = [i for i in dat_raw if 'del' in i])
            sample = data_proc.copy()
            block = []
            block_cond = []
            # Split Block Info into Block & Block condition 
            for i in sample['block']:
                if len(str(i)) ==2:
                    block.append(int(str(i)[0]))
                    block_cond.append(int(str(i)[1]))
                elif len(str(i)) ==3:
                    block.append(int(str(i)[0:2]))
                    block_cond.append(int(str(i)[-1]))
            sample['block_nr'] = pd.Series(block)
            sample['block_cond'] = pd.Series(block_cond)
            sample = sample.drop(axis=1, labels = ['block']).copy()
            data_raw_bl.append((vpn_id,sample.iloc[0,0],sample.loc[0:99]))
            data_raw_exp.append((vpn_id,sample.iloc[0,0],sample.loc[100::]))
            sample['bl_exp'] = pd.Series(np.append(np.zeros(100), np.ones(300)))
            data_raw_total.append((vpn_id,sample))
            # check if data exactly 400 trials long
            if len(sample['block_nr']) > 100+300:
                print('shit')
########## get additional info

groups = {1:'naive, neutral',
          2:'instruiert, neutral',
          3:'naive, negativ',
          4:'instruiert, negativ'}
block_cond = {0:'no malingering',
              1:'malingering'}
trial_types_dict = {1:'AX',
              2:'BX',
              3:'AY',
              4:'BY'}

########## get group data

groups_raw = pd.read_csv(r'C:\Users\de_hauk\Desktop\VP_Zuordnung.txt',sep ='\t').sort_values('id').drop('ID', axis =1)
groups = groups_raw.loc[groups_raw['id'].isin(unique_IDs)].copy()

########## Get proc data
PERF_bl= []
PERF_bl_DF = pd.DataFrame(columns= ['id','RT_M_bl','RT_STD_bl', 'hits_bl','misses_bl','incorrect_bl'] )
PERF_exp_DF_1 =  pd.DataFrame()
PERF_exp_DF_0 = pd.DataFrame()
#### New Func
for vpn_dat in data_raw_total:
    ### get id
    curr_id = int(vpn_dat[0])
    
    ### get BS group
    BS_group = groups['group'].loc[groups['id'] == curr_id]
    #print(curr_id,int(BS_group))
    bl_data_raw = vpn_dat[1].loc[0:99]
    exp_data_raw = vpn_dat[1].loc[100::]
    if 30 in bl_data_raw['trial_nr'].unique():
        print('irregular block length')
    bl_data = bl_data_raw.drop(labels = ['group','trial_nr','bl_exp'],axis=1)
    exp_data = exp_data_raw.drop(labels = ['group','trial_nr','bl_exp'],axis=1)

    ### get trial_type
    trial_types = bl_data['type'].sort_values(ascending = True).unique()
    ### data storage
    Data_long = pd.DataFrame()
    Data_long_clmns = ['ID','block_cond','BS_cond','trial_type','mean','std','hits','misses','incorrect']
    Data_wide = pd.DataFrame()
    Data_wide_clmns = ['ID','BS_cond','trial_type','mean_0','std_0','hits_0','misses_0','incorrect_0','mean_1','std_1','hits_1','misses_1','incorrect_1']
    
    ########## get BL data
    n_blocks_bl = bl_data['block_nr'].unique()
    BL_dat_id = pd.DataFrame(columns= ['id','RT_M','RT_STD', 'hits','misses','incorrect'])
    if len(n_blocks_bl) != 5:
        print('error block length exp')     
    # for block_bl in n_blocks_bl:
    #     curr_block_DF_bl = bl_data.loc[bl_data['block_nr'] == block_bl]
    bl_tt_res = pd.DataFrame(index= ['id','RT_M_bl','RT_STD_bl', 'hits_bl','misses_bl','incorrect_bl'] )
    for trial_type in trial_types:
        curr_tt_bl_hits = bl_data.loc[(bl_data['type'] == trial_type) & (bl_data['R_type'] == ' hit')]
        curr_tt_bl_all = bl_data.loc[(bl_data['type'] == trial_type)]
        res_block_bl = [curr_id,                                                        
                        curr_tt_bl_hits['RT'].mean(),
                        curr_tt_bl_hits['RT'].std(),
                        len([i for i in curr_tt_bl_all['R_type'] if i == ' hit']),
                        len([i for i in curr_tt_bl_all['R_type'] if i == ' miss']),
                        len([i for i in curr_tt_bl_all['R_type'] if i == ' incorrect'])]
        bl_tt_res[trial_types_dict[trial_type]] = res_block_bl
    bl_tt_res = bl_tt_res.copy().T
    bl_tt_res['trial_type'] = [trial_types_dict[1],
                                  trial_types_dict[2],
                                  trial_types_dict[3],
                                  trial_types_dict[4]]
    PERF_bl_DF = PERF_bl_DF.append(bl_tt_res).copy()

    ############ get exp data
    n_blocks_exp = exp_data['block_nr'].unique()
    if len(n_blocks_exp) != 10:
        print('error block length exp')
    for block_cond in exp_data['block_cond'].unique():
        exp_tt_res = pd.DataFrame(index= ['id','RT_M_exp_'+str(block_cond),
                                          'RT_STD_exp_'+str(block_cond),
                                          'hits_exp_'+str(block_cond),
                                          'misses_exp_'+str(block_cond),
                                          'incorrect_exp_'+str(block_cond)])
        
        curr_cond_DF_exp = exp_data.loc[exp_data['block_cond'] == block_cond]
        for trial_type in trial_types:
            curr_tt_exp_hits = exp_data.loc[(exp_data['type'] == trial_type) & (exp_data['R_type'] == ' hit')]
            curr_tt_exp_all = exp_data.loc[(exp_data['type'] == trial_type)]
            res_tt_exp = [curr_id,
                            curr_tt_exp_hits['RT'].mean(),
                            curr_tt_exp_hits['RT'].std(),
                            len([i for i in curr_tt_exp_all['R_type'] if i == ' hit']),
                            len([i for i in curr_tt_exp_all['R_type'] if i == ' miss']),
                            len([i for i in curr_tt_exp_all['R_type'] if i == ' incorrect'])]
            exp_tt_res[trial_types_dict[trial_type]] = res_tt_exp
        exp_tt_res = exp_tt_res.copy().T
        exp_tt_res['trial_type'] = [trial_types_dict[1],
                              trial_types_dict[2],
                              trial_types_dict[3],
                              trial_types_dict[4]]
        if block_cond == 0:
            PERF_exp_DF_0 = PERF_exp_DF_0.copy().append(exp_tt_res)
        elif block_cond ==1:
            PERF_exp_DF_1 = PERF_exp_DF_1.copy().append(exp_tt_res)


###Merge all DF to wide format 
total_dat = pd.DataFrame()
AAA_dat = pd.concat([PERF_bl_DF.sort_values('id'),
                     PERF_exp_DF_0.sort_values('id').drop(['id','trial_type'], axis = 1),
                     PERF_exp_DF_1.sort_values('id').drop(['id','trial_type'], axis = 1)]
                    ,axis=1)


###Merge all DF to long format 
BBB_dat = pd.concat([PERF_bl_DF.sort_values('id'),
                     PERF_exp_DF_0.sort_values('id'),
                     PERF_exp_DF_1.sort_values('id')]
                    ,axis=0)



group_aaa = []
for i in AAA_dat['id'].unique():
    group_aaa = group_aaa +list(groups['group'].loc[groups['id'] == i])*4
AAA_dat['group'] = group_aaa
AAA_dat.to_csv(r'C:\Users\de_hauk\Desktop\data_JASP_2.csv', sep=',' )

anova_2f_bs = AAA_dat.copy()[['id','RT_M_bl','trial_type','group']]
anova_2f_bs.to_csv(r'C:\Users\de_hauk\Desktop\anova_2f_bs.csv', sep=',' )

aaaBBB = pd.melt(AAA_dat, id_vars=['group','id','trial_type'], value_vars=['RT_M_bl','RT_M_exp_0','RT_M_exp_1'])
blck_cond = []
for i in aaaBBB['variable']:
    if i == 'RT_M_bl':
        blck_cond.append(0)
    elif i == 'RT_M_exp_0':
        blck_cond.append(1)
    elif i == 'RT_M_exp_1':
        blck_cond.append(2)
aaaBBB['block_cond'] = blck_cond
BS_cond = []
for i,j in zip(aaaBBB['trial_type'],aaaBBB['block_cond']):
    BS_cond.append(str(i)+str(j))
aaaBBB['total_cond'] = BS_cond      

res = pg.mixed_anova(data=aaaBBB, dv='value', subject ='id', between='group', within ='total_cond', effsize='np2')
res_ttest = pg.pairwise_ttests(data=aaaBBB, dv='value', subject ='id', between='group', within ='total_cond')

