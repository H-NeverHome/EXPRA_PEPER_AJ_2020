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
            unique_IDs.append(vpn_id)
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
            if len(sample['block_nr']) > 100+300:
                print('shit')


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



### Get error rates
def data_proc_incorr(data_bl,data_exp):
    tot_dat = []
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
        tot_dat.append((data_type,fin_dat))
    return tot_dat




### Get reaction time (only hits)
def data_proc_RT(data_bl,data_exp):
    Fin_dat_RT = []
    for data,data_type in zip([data_raw_bl,data_raw_exp],['baseline','experiment']):
        fin_dat_experi = []
        fin_dat_111 = pd.DataFrame(columns = ['RT_0_mean','RT_0_std','RT_1_mean','RT_1_std'])
        fin_dat_bl = pd.DataFrame(columns = ['RT_mean','RT_std'])
        for vpn in data:
            curr_df = vpn[2].copy() 
            curr_id = vpn[0]
            hit = curr_df.loc[(curr_df['R_type'] == ' hit')]

            check = hit.copy()
            if data_type == 'baseline':
                rng = 6 # 5 Blocks a 20 in baseline
            elif data_type == 'experiment':
                rng = 11 # 10 Blocks a 30 in baseline
            rt_DF = pd.DataFrame(index = ['B_' + str(i) for i in range(1,rng)])
            rt_mean, rt_std,block_cond = [],[],[]
            hhhh = pd.DataFrame(columns = ['mean','std','block','block_cond'])
            # for every block
            for i in range(1,rng):
                curr_block = check.loc[(check['block_nr'] == i)]
                corr_block_proc = pd.DataFrame(columns = ['mean','std','hits','misses','incorrect'], index= ['trial_t_1','trial_t_2','trial_t_3' ,'trial_t_4' ])
                #print(curr_block)
                block_c = np.unique(np.array(curr_block['block_cond']))[0]
                mean_list = []
                std_list = []
                hits_L = []
                missed_L = []
                error_L = []
                
                # for every trialtype
                for trial_type in range(1,5):
                    RT_mean = curr_block['RT'].loc[(curr_block['type'] == trial_type) & (curr_block['R_type'] == ' hit')].mean()
                    RT_std = curr_block['RT'].loc[(curr_block['type'] == trial_type) & (curr_block['R_type'] == ' hit')].std()
                    #hit,miss,error
                    hits = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' hit']
                    doesnt work
                    missed = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' miss']
                    error = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' incorrect']
                    mean_list.append(RT_mean)
                    std_list.append(RT_std)
                    hits_L.append(len(hits))
                    missed_L.append(len(missed))
                    error_L.append(len(error))
                #print(missed_L)   
                # RT_mean_1, RT_std_1 = curr_block['RT'].loc[curr_block['type'] == 1].mean(), curr_block['RT'].loc[curr_block['type'] == 1].std()
                # RT_mean_2, RT_std_2 = curr_block['RT'].loc[curr_block['type'] == 2].mean(), curr_block['RT'].loc[curr_block['type'] == 2].std()
                # RT_mean_3, RT_std_3 = curr_block['RT'].loc[curr_block['type'] == 3].mean(), curr_block['RT'].loc[curr_block['type'] == 3].std()
                # RT_mean_4, RT_std_4 = curr_block['RT'].loc[curr_block['type'] == 4].mean(), curr_block['RT'].loc[curr_block['type'] == 4].std()
                # sum_hits,sum_error, sum_miss = 
                # rt_mean.append([RT_mean_1,RT_mean_2,RT_mean_3,RT_mean_4])
                # rt_std.append([RT_std_1, RT_std_2, RT_std_3, RT_std_4])
                corr_block_proc['mean'] = mean_list
                corr_block_proc['std'] = std_list
                corr_block_proc['hits'] = hits_L
                corr_block_proc['incorrect'] = error_L
                corr_block_proc['misses'] = missed_L
                # corr_block_proc['mean'] = [RT_mean_1,RT_mean_2,RT_mean_3,RT_mean_4]
                # corr_block_proc['std'] = [RT_std_1, RT_std_2, RT_std_3, RT_std_4]
                corr_block_proc['block'] = [i,i,i,i]
                corr_block_proc['block_cond'] = [block_c,block_c,block_c,block_c]
                #print(i,corr_block_proc)
                hhhh = pd.concat([hhhh,corr_block_proc])
                # if pd.Series([RT_mean_1,RT_mean_2,RT_mean_3,RT_mean_4]).isnull().values.any() == True:
                #     print(curr_block)
                # rt_mean.append(RT_mean)
                # rt_std.append(RT_std)
                #block_cond.append(block_c)
            fin_dat_experi.append((curr_id,hhhh))
        Fin_dat_RT.append((data_type,fin_dat_experi))
           
            # rt_DF['rt_mean'],rt_DF['rt_std'] = rt_mean,rt_std
            # rt_DF['block_cond'] = block_cond
    return Fin_dat_RT
        #     # Compute Mean of Means,Std,MEdian
        #     block_dat = pd.DataFrame(index = [curr_id])
            
        #     if data_type == 'baseline': # ignore block condition in BL
        #         RT_mean_BL = rt_DF['rt_mean'].mean()
        #         RT_std_BL = rt_DF['rt_mean'].std()
        #         block_dat['RT_mean'], block_dat['RT_std'] = RT_mean_BL,RT_std_BL
        #         fin_dat_bl = pd.concat([fin_dat_bl,block_dat],axis = 0)
                
        #     elif data_type == 'experiment':
        #         block_c_0_mean = rt_DF.loc[rt_DF['block_cond'] == 0]['rt_mean'].mean()
        #         block_c_0_std = rt_DF.loc[rt_DF['block_cond'] == 0]['rt_mean'].std()
        #         block_c_1_mean = rt_DF.loc[rt_DF['block_cond'] == 1]['rt_mean'].mean()
        #         block_c_1_std = rt_DF.loc[rt_DF['block_cond'] == 1]['rt_mean'].std()
        #         block_c_0 = [block_c_0_mean, block_c_0_std]
        #         block_c_1 = [block_c_1_mean,block_c_1_std]
        #         block_dat['RT_0_mean'],block_dat['RT_0_std'] = block_c_0[0],block_c_0[1]
        #         block_dat['RT_1_mean'],block_dat['RT_1_std'] = block_c_1[0],block_c_1[1]
        #         fin_dat_111 = pd.concat([fin_dat_111,block_dat],axis = 0)
    
        # if data_type == 'baseline':
            
        #     Fin_dat_RT.append((data_type,fin_dat_bl))
        # elif data_type == 'experiment':
        #     Fin_dat_RT.append((data_type,fin_dat_111))
    #return rt_DF
        

DATA_incorrect_answers = data_proc_incorr(data_raw_bl,data_raw_exp)
DATA_missed_answers = data_proc_missed(data_raw_bl,data_raw_exp)
DATA_rt = data_proc_RT(data_raw_bl,data_raw_exp)

lfnjalkn = len([i for i in data_raw_exp[0][2]['R_type'] if i == ' incorrect'])      
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





