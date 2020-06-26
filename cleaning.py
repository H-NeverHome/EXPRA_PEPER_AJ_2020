# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:58:39 2020

@author: de_hauk
"""


import pandas as pd

import numpy as np
import os
data_raw_exp = []
data_raw_bl = []
column_names = ['del1','group','del2','block','del3', 'trial_nr','del4', 'type', 'del5','RT','del6','R_type']
 
total_dat_BL = pd.DataFrame()
total_dat_EXP = pd.DataFrame()
miss_error = pd.DataFrame()
### Load, name columns, drop irrelevant, split into baseline & experiment  
for file in os.listdir(r"C:\Users\de_hauk\Desktop\New folder"):
    if file.endswith(".txt"):
        path = os.path.join(r"C:\Users\de_hauk\Desktop\New folder", file)
        if 'block' in path:
            vpn_id = file.split('b')[0]
            dat_raw = pd.read_csv(path,header=None, names = column_names)
            data_proc = dat_raw.drop(axis=1,labels = [i for i in dat_raw if 'del' in i])
            sample = data_proc.copy()
            block = []
            block_cond = []
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

### Get missed answers
vpn_all = []
for vpn in data_raw_exp:
    curr_df = vpn[2] 
    curr_id = vpn[0] 
    miss = curr_df.loc[(curr_df['R_type'] == ' miss')].drop(axis = 1, labels = ['R_type', 'RT'])
    miss_proto = pd.DataFrame(index = ['1','2','3','4'])
    missed_answ = []
    
    for block_cond in range(0,2):
        check = miss.loc[miss['block_cond'] == block_cond]
        miss_proto = pd.DataFrame(index = ['1','2','3','4'])    
        for i in range(1,11):
            if i in check['block_nr'].values:
                curr_block = check.loc[(check['block_nr'] == i)]
                unq_val, unq_count = np.unique(curr_block['type'],return_counts = True)
                errors = np.ones(4)
                for tt in [1,2,3,4]:
                    if tt in unq_val:
                        ind = np.where(unq_val==tt)
                        errors[tt-1] = unq_count[ind[0]]
                    elif tt not in unq_val:
                        errors[tt-1] = 0
                miss_proto['B_'+str(i)] = errors
            else:
                miss_proto['B_'+str(i)] = np.zeros(4)
        missed_answ.append(('block_condition'+str(block_cond),miss_proto))
    fin = missed_answ[0][1].append(missed_answ[1][1])
    fin['block_cond'] = np.append(np.zeros(4),np.ones(4))
    vpn_all.append((curr_id,missed_answ,fin))
            
    # no_miss = ddddd.loc[(ddddd['R_type'] != ' miss')]

# for dat_exp,dat_bl in zip(data_raw_exp,data_raw_bl):
    
# for file in os.listdir(r"C:\Users\de_hauk\Desktop\New folder"):
#     if file.endswith(".txt"):
#         path = os.path.join(r"C:\Users\de_hauk\Desktop\New folder", file)
#         if 'block' in path:
#             print(file.split('b')[0])
       

### Get error rates


### Get reaction time
