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


# vpn_all = []
# #for data in [data_raw_exp,data_raw_bl]

# for data,data_type in zip([data_raw_bl,data_raw_exp],['baseline','experiment']):
#     fin_dat= []
#     for vpn in data:
#         curr_df = vpn[2] 
#         curr_id = vpn[0] 
#         miss = curr_df.loc[(curr_df['R_type'] == ' miss')].drop(axis = 1, labels = ['R_type', 'RT'])
#         miss_proto = pd.DataFrame(index = ['1','2','3','4'])
#         missed_answ = []
        
#         for block_cond in range(0,2):
#             check = miss.loc[miss['block_cond'] == block_cond]
#             miss_proto = pd.DataFrame(index = ['1','2','3','4'])    
#             for i in range(1,11):
#                 if i in check['block_nr'].values:
#                     curr_block = check.loc[(check['block_nr'] == i)]
#                     unq_val, unq_count = np.unique(curr_block['type'],return_counts = True)
#                     errors = np.ones(4)
#                     for tt in [1,2,3,4]:
#                         if tt in unq_val:
#                             ind = np.where(unq_val==tt)
#                             errors[tt-1] = unq_count[ind[0]]
#                         elif tt not in unq_val:
#                             errors[tt-1] = 0
#                     miss_proto['B_'+str(i)] = errors
#                 else:
#                     miss_proto['B_'+str(i)] = np.zeros(4)
#             missed_answ.append(('block_condition'+str(block_cond),miss_proto))
#         fin = missed_answ[0][1].append(missed_answ[1][1])
#         fin['block_cond'] = np.append(np.zeros(4),np.ones(4))
#         fin_dat.append((int(curr_id),fin))
#     vpn_all.append((data_type,fin_dat))

# ### Get missed answers
def data_proc_missed(data_bl,data_exp):
    tot_dat = []
    for data,data_type in zip([data_bl,data_exp],['baseline','experiment']):
        proc_dat= []
        for vpn in data:
            curr_df = vpn[2] 
            curr_id = vpn[0] 
            miss = curr_df.loc[(curr_df['R_type'] == ' miss')].drop(axis = 1, labels = ['R_type', 'RT'])
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
            proc_dat.append((int(curr_id),fin))
        tot_dat.append((data_type,proc_dat))
    return tot_dat

missed_answers = data_proc_missed(data_raw_bl,data_raw_exp)

### Get error rates
def data_proc_incorr(data_bl,data_exp):
    tot_dat = []
    hhhh = []
    for data,data_type in zip([data_bl,data_exp],['baseline','experiment']):
        fin_dat= []
        for vpn in data:
            curr_df = vpn[2].copy() 
            curr_id = vpn[0]
            miss = curr_df.loc[(curr_df['R_type'] == ' incorrect')].drop(axis = 1, labels = ['R_type', 'RT'])
            #hhhh.append((curr_id,miss))
            missed_answ = []
            for block_cond in range(0,2):
                check = miss.loc[miss['block_cond'] == block_cond]
                miss_proto = pd.DataFrame(index = ['1','2','3','4'])    
                if data_type == 'baseline':
                    rng = 6
                elif data_type == 'experiment':
                    rng = 11
                for i in range(1,rng):
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
            fin_dat.append((int(curr_id),fin))
        hhhh.append((data_type,fin_dat))
    return hhhh

incorrect_answers = data_proc_incorr(data_raw_bl,data_raw_exp)


### Get reaction time (only hits)
aaaa = []
for data,data_type in zip([data_raw_bl,data_raw_exp],['baseline','experiment']):
    fin_dat= []
    for vpn in data:
        curr_df = vpn[2].copy() 
        curr_id = vpn[0]
        hit = curr_df.loc[(curr_df['R_type'] == ' hit')]
        ffff = []
        #for block_cond in range(0,2):
        check = hit.copy()
        if data_type == 'baseline':
            rng = 6
        elif data_type == 'experiment':
            rng = 11
        rt_DF = pd.DataFrame(index = ['B_' + str(i) for i in range(1,rng)])
        rt_mean, rt_median,rt_std,block_cond = [],[],[],[]
        for i in range(1,rng):
            curr_block = check.loc[(check['block_nr'] == i)]
            block_c = np.unique(np.array(curr_block['block_cond']))
            if len(block_c)<1:
                print(curr_id,curr_block,block_c,data_type)
            RT_mean, RT_median, RT_std = curr_block['RT'].mean(), curr_block['RT'].median(), curr_block['RT'].std()
            rt_mean.append(RT_mean)
            rt_median.append(RT_median)
            rt_std.append(RT_std)
            block_cond.append(block_c)
        rt_DF['rt_mean'],rt_DF['rt_median'],rt_DF['rt_std'] = rt_mean,rt_median,rt_std
        rt_DF['block_cond'] = block_cond
        #    ffff.append((block_cond,rt_DF))
        fin_dat.append((curr_id,rt_DF))
    aaaa.append((data_type,fin_dat))

#Check ID 14 BL & 22 EXP
       
    #             if i in check['block_nr'].values:
    #                 curr_block = check.loc[(check['block_nr'] == i)]
    #                 unq_val, unq_count = np.unique(curr_block['type'],return_counts = True)
    #                 errors = np.ones(4)
    #                 for tt in [1,2,3,4]:
    #                     if tt in unq_val:
    #                         ind = np.where(unq_val==tt)
    #                         errors[tt-1] = unq_count[ind[0]]
    #                     elif tt not in unq_val:
    #                         errors[tt-1] = 0
    #                 hit_proto['B_'+str(i)] = errors
    #             else:
    #                 hit_proto['B_'+str(i)] = np.zeros(4)
                    
    #     fin_dat.append((curr_id,data_type,ffff))
    # aaaa.append(fin_dat)   
    #     # #missed_answ = []
        # 
        #     
        #     if data_type == 'baseline':
        #         rng = 6
        #     elif data_type == 'experiment':
        #         rng = 11  
        #     for i in range(1,rng):
        #         curr_block = check.loc[(check['block_nr'] == i)]
        #         aaaa.append((curr_id,block_cond,curr_block))
                # if i in check['block_nr'].values:
                #     curr_block = check.loc[(check['block_nr'] == i)]
                #     unq_val, unq_count = np.unique(curr_block['type'],return_counts = True)
                #     errors = np.ones(4)
                #     for tt in [1,2,3,4]:
                #         if tt in unq_val:
                #             ind = np.where(unq_val==tt)
                #             errors[tt-1] = unq_count[ind[0]]
                #         elif tt not in unq_val:
                #             errors[tt-1] = 0
                #     hit_proto['B_'+str(i)] = errors
                # else:
                #     hit_proto['B_'+str(i)] = np.zeros(4)
    #         missed_answ.append(('block_condition'+str(block_cond),hit_proto))
    #     fin = missed_answ[0][1].append(missed_answ[1][1])
    #     fin['block_cond'] = np.append(np.zeros(4),np.ones(4))
    #     fin_dat.append((int(curr_id),fin))
    # hhhh.append((data_type,fin_dat))





