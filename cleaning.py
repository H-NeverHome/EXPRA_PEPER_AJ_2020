# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:58:39 2020

@author: de_hauk
"""


import pandas as pd
import pingouin as pg
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




### Get reaction time (only hits)
def data_proc_RT(data_bl,data_exp):
    Fin_dat_RT = []
    for data,data_type in zip([data_raw_bl,data_raw_exp],['baseline','experiment']):
        fin_dat_experi = []
        fin_dat_111 = pd.DataFrame(columns = ['RT_0_mean','RT_0_std','RT_1_mean','RT_1_std'])
        fin_dat_bl = pd.DataFrame(columns = ['RT_mean','RT_std'])
        clms = ['ID','block_cond','trial_type','mean','std','hits','misses','incorrect']
        fin_datfin = pd.DataFrame(columns = clms)
        fin_dat_JASP = pd.DataFrame() 
        for vpn in data:
            curr_df = vpn[2].copy() 
            curr_id = vpn[0]
            hit = curr_df.copy()
            check = hit.copy()
            if data_type == 'baseline':
                rng = 6 # 5 Blocks a 20 in baseline
            elif data_type == 'experiment':
                rng = 11 # 10 Blocks a 30 in baseline
            #rt_DF = pd.DataFrame(index = ['B_' + str(i) for i in range(1,rng)])
            #rt_mean, rt_std,block_cond = [],[],[]
            hhhh = pd.DataFrame(columns = ['mean','std','block','block_cond'])
            # for every block
            for i in range(1,rng):
                curr_block = check.loc[(check['block_nr'] == i)]
                corr_block_proc = pd.DataFrame(columns = ['mean','std','hits','misses','incorrect'], index= ['AX','BX','AY' ,'BY'])
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
                    missed = [i for i in curr_block['R_type'].loc[(curr_block['type'] == trial_type)] if i == ' miss']
                    error = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' incorrect']
                    mean_list.append(RT_mean)
                    std_list.append(RT_std)
                    hits_L.append(len(hits))
                    missed_L.append(len(missed))
                    error_L.append(len(error))
                    
                corr_block_proc['mean'] = mean_list
                corr_block_proc['std'] = std_list
                corr_block_proc['hits'] = hits_L
                corr_block_proc['incorrect'] = error_L
                corr_block_proc['misses'] = missed_L

                corr_block_proc['block'] = [i,i,i,i]
                corr_block_proc['block_cond'] = [block_c,block_c,block_c,block_c]

                hhhh = pd.concat([hhhh,corr_block_proc])
                
            save_dict = pd.DataFrame(columns = clms)
            ## for every trialtype & block cond
            for tt in ['AX','BX','AY' ,'BY']:
                curr_df = hhhh.loc[tt].copy()
                curr_df_0_mean = curr_df.loc[curr_df['block_cond'] == 0]['mean'].mean()
                curr_df_0_std = curr_df.loc[curr_df['block_cond'] == 0]['mean'].std()
                curr_df_0_hit = curr_df.loc[curr_df['block_cond'] == 0]['hits'].sum()
                curr_df_0_miss = curr_df.loc[curr_df['block_cond'] == 0]['misses'].sum()
                curr_df_0_error = curr_df.loc[curr_df['block_cond'] == 0]['incorrect'].sum()
                
                curr_df_1_mean = curr_df.loc[curr_df['block_cond'] == 1]['mean'].mean()
                curr_df_1_std = curr_df.loc[curr_df['block_cond'] == 1]['mean'].std()
                curr_df_1_hit = curr_df.loc[curr_df['block_cond'] == 1]['hits'].sum()
                curr_df_1_miss = curr_df.loc[curr_df['block_cond'] == 1]['misses'].sum()
                curr_df_1_error = curr_df.loc[curr_df['block_cond'] == 1]['incorrect'].sum()
                fin_res_0 = pd.Series([curr_id,0,tt,curr_df_0_mean,curr_df_0_std,curr_df_0_hit,curr_df_0_miss,curr_df_0_error], index = clms)
                fin_res_1 = pd.Series([curr_id,1,tt,curr_df_1_mean,curr_df_1_std,curr_df_1_hit,curr_df_1_miss,curr_df_1_error], index = clms)
                save_dict = save_dict.append(fin_res_0,ignore_index=True)
                save_dict = save_dict.append(fin_res_1,ignore_index=True)
            
            save_dict_0 = save_dict.loc[save_dict['block_cond'] == 0].copy()
            save_dict_1 = save_dict.loc[save_dict['block_cond'] == 1].copy()
            save_dict_X = pd.DataFrame()
            save_dict_X['trialtype'],save_dict_X['id'] = save_dict_0['trial_type'],save_dict_0['ID']
            save_dict_X['mean_0'],save_dict_X['mean_1'] = save_dict_0['mean'],[i for i in save_dict_1['mean']]
            save_dict_X['hits_0'],save_dict_X['hits_1'] =save_dict_0['hits'],[i for i in save_dict_1['hits']]
            save_dict_X['miss_0'],save_dict_X['miss_1'] =save_dict_0['misses'],[i for i in save_dict_1['misses']]
            save_dict_X['error_0'],save_dict_X['error_1'] =save_dict_0['incorrect'],[i for i in save_dict_1['incorrect']]
            #save_dict_cond = pd.concat([save_dict_0,save_dict_1])
            fin_dat_experi.append((curr_id,hhhh,save_dict,save_dict_X))
            fin_datfin = fin_datfin.append(save_dict)
            fin_dat_JASP = fin_dat_JASP.append(save_dict_X)
        Fin_dat_RT.append((data_type,fin_dat_experi,fin_datfin,fin_dat_JASP))
           

    return Fin_dat_RT
        


DATA_rt = data_proc_RT(data_raw_bl,data_raw_exp)
data_raw = DATA_rt[1][2]
data_raw['ID'] = data_raw['ID'].copy().astype('int32')
data_raw['block_cond'] = data_raw['block_cond'].copy().astype('int32')
data_raw['trial_type'] = data_raw['trial_type'].copy().replace({'AX':1,
                                                                'BX':2,
                                                                'AY':3,
                                                                'BY':4})
data = data_raw.sort_values('ID')
groups_raw = pd.read_csv(r'C:\Users\de_hauk\Desktop\VP_Zuordnung.txt',sep ='\t').sort_values('id')
groups = groups_raw.loc[groups_raw['id'] != 22]
ids_list = []
conds_list = []
for ids,group in zip(groups['id'],groups['group']):
    aaa = [ids] *8
    ids_list = ids_list +aaa 
    bbb = [group] *8 
    conds_list = conds_list + bbb
data['ids'],data['BS_group'] = ids_list,conds_list
check_u = data['ids'] == data['ID']



data.to_csv(r'C:\Users\de_hauk\Desktop\data.csv', sep=',' )

###Data for JASP

group_BS = groups.copy()
data_JASP = DATA_rt[1][3]
data_JASP['id'] = data_JASP['id'].copy().astype('int32')
data_JASP = data_JASP.sort_values('id').copy()

check_ids = group_BS['id'] == np.unique(data_JASP['id'])
group_JASP = []
for i,j in zip(group_BS['id'],group_BS['group']):
    group_JASP = group_JASP + [j]*4
    
data_JASP['bs_group'] = group_JASP
    
data_JASP.to_csv(r'C:\Users\de_hauk\Desktop\data_JASP.csv', sep=',' )

data_PG = DATA_rt[1][2]
res = pg.mixed_anova(data=data_PG, dv='mean', subject ='ID', between=['trial_type','BS_group'], within ='block_cond', effsize='np2')


#res_m_ttest = pg.pairwise_ttests(data, dv='mean', between=['block_cond','trial_type'])
############################################# OLDv ################################
'''
DATA_incorrect_answers = data_proc_incorr(data_raw_bl,data_raw_exp)
DATA_missed_answers = data_proc_missed(data_raw_bl,data_raw_exp)
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


'''


