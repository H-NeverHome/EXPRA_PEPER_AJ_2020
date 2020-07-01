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
#### get additional info

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

### get group data

groups_raw = pd.read_csv(r'C:\Users\de_hauk\Desktop\VP_Zuordnung.txt',sep ='\t').sort_values('id').drop('ID', axis =1)
groups = groups_raw.loc[groups_raw['id'].isin(unique_IDs)].copy()

###
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


###Merge all DF 
total_dat = pd.DataFrame()
AAA_dat = pd.concat([PERF_bl_DF.sort_values('id'),
                     PERF_exp_DF_0.sort_values('id').drop(['id','trial_type'], axis =1),
                     PERF_exp_DF_1.sort_values('id').drop(['id','trial_type'], axis =1)]
                    ,axis=1)

group_aaa = []
for i in AAA_dat['id'].unique():
    group_aaa = group_aaa +list(groups['group'].loc[groups['id'] == i])*4
AAA_dat['group'] = group_aaa
AAA_dat.to_csv(r'C:\Users\de_hauk\Desktop\data_JASP_2.csv', sep=',' )
# total_dat = total_dat.copy().append(PERF_bl_DF)
# total_dat = total_dat.copy().append(PERF_exp_DF_1)
# total_dat = total_dat.copy().append(PERF_exp_DF_0)
# ### Get reaction time, errors & misses
# data_bl = data_raw_bl
# data_exp = data_raw_exp

# DATA_total = []
# for data,data_type in zip([data_raw_bl,data_raw_exp],['baseline','experiment']):
#     fin_dat_experi = []
#     clms = ['ID','block_cond','trial_type','mean','std','hits','misses','incorrect']
#     fin_datfin = pd.DataFrame(columns = clms)
#     fin_dat_JASP = pd.DataFrame() 
#     for vpn in data:
#         curr_df = vpn[2].copy() 
#         curr_id = int(vpn[0])
#         hit = curr_df.copy()
#         check = hit.copy()
        
#         #check if experimental or baseline data
#         if data_type == 'baseline':
#             rng = 6 # 5 Blocks a 20 in baseline
#         elif data_type == 'experiment':
#             rng = 11 # 10 Blocks a 30 in baseline

#         data_id = pd.DataFrame(columns = ['mean','std','block','block_cond'])
#         # for every block
#         for i in range(1,rng):
#             curr_block = check.loc[(check['block_nr'] == i)]
#             corr_block_proc = pd.DataFrame(columns = ['mean','std','hits','misses','incorrect'], index= ['AX','BX','AY' ,'BY'])
#             #print(curr_block)
#             block_c = np.unique(np.array(curr_block['block_cond']))[0]
#             mean_L = []
#             std_L = []
#             hits_L = []
#             missed_L = []
#             error_L = []
#             id_L = []
#             # for every trialtype
#             for trial_type in range(1,5):
#                 # get RT
#                 RT_mean = curr_block['RT'].loc[(curr_block['type'] == trial_type) & (curr_block['R_type'] == ' hit')].mean()
#                 RT_std = curr_block['RT'].loc[(curr_block['type'] == trial_type) & (curr_block['R_type'] == ' hit')].std()
#                 #hit,miss,error
#                 hits = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' hit']
#                 missed = [i for i in curr_block['R_type'].loc[(curr_block['type'] == trial_type)] if i == ' miss']
#                 error = [i for i in curr_block['R_type'].loc[curr_block['type'] == trial_type] if i == ' incorrect']
#                 mean_L.append(RT_mean)
#                 std_L.append(RT_std)
#                 hits_L.append(len(hits))
#                 missed_L.append(len(missed))
#                 error_L.append(len(error))
#                 id_L.append(curr_id)
                
#             corr_block_proc['mean'] = mean_L
#             corr_block_proc['std'] = std_L
#             corr_block_proc['hits'] = hits_L
#             corr_block_proc['incorrect'] = error_L
#             corr_block_proc['misses'] = missed_L
#             corr_block_proc['ID'] = id_L
#             corr_block_proc['block'] = [i,i,i,i]
#             corr_block_proc['block_cond'] = [block_c,block_c,block_c,block_c]

#             data_id = pd.concat([data_id,corr_block_proc])
            
#         save_dict = pd.DataFrame(columns = clms)
        
        
#         ## for every block cond
#         for tt in ['AX','BX','AY' ,'BY']:
#             # get data from curr id
#             curr_df = data_id.loc[tt].copy()
            
#             # block cond 0 == no malinger
#             curr_df_0_mean = curr_df.loc[curr_df['block_cond'] == 0]['mean'].mean()
#             curr_df_0_std = curr_df.loc[curr_df['block_cond'] == 0]['mean'].std()
#             curr_df_0_hit = curr_df.loc[curr_df['block_cond'] == 0]['hits'].sum()
#             curr_df_0_miss = curr_df.loc[curr_df['block_cond'] == 0]['misses'].sum()
#             curr_df_0_error = curr_df.loc[curr_df['block_cond'] == 0]['incorrect'].sum()
            
#             # block cond 1 == no malinger
#             curr_df_1_mean = curr_df.loc[curr_df['block_cond'] == 1]['mean'].mean()
#             curr_df_1_std = curr_df.loc[curr_df['block_cond'] == 1]['mean'].std()
#             curr_df_1_hit = curr_df.loc[curr_df['block_cond'] == 1]['hits'].sum()
#             curr_df_1_miss = curr_df.loc[curr_df['block_cond'] == 1]['misses'].sum()
#             curr_df_1_error = curr_df.loc[curr_df['block_cond'] == 1]['incorrect'].sum()
            
#             #get data together
#             fin_res_0 = pd.Series([curr_id,0,tt,curr_df_0_mean,curr_df_0_std,curr_df_0_hit,curr_df_0_miss,curr_df_0_error], index = clms)
#             fin_res_1 = pd.Series([curr_id,1,tt,curr_df_1_mean,curr_df_1_std,curr_df_1_hit,curr_df_1_miss,curr_df_1_error], index = clms)
            
#             # append to DF
#             save_dict = save_dict.append(fin_res_0,ignore_index=True)
#             save_dict = save_dict.append(fin_res_1,ignore_index=True)
        
#         save_dict_0 = save_dict.loc[save_dict['block_cond'] == 0].copy()
#         save_dict_1 = save_dict.loc[save_dict['block_cond'] == 1].copy()
        
#         #change from long format to wide for JASP
#         save_dict_JASP = pd.DataFrame()
#         save_dict_JASP['trialtype'],save_dict_JASP['id'] = save_dict_0['trial_type'],save_dict_0['ID'].copy().astype('int32')
#         save_dict_JASP['mean_0'],save_dict_JASP['mean_1'] = save_dict_0['mean'],[i for i in save_dict_1['mean']]
#         save_dict_JASP['hits_0'],save_dict_JASP['hits_1'] =save_dict_0['hits'],[i for i in save_dict_1['hits']]
#         save_dict_JASP['miss_0'],save_dict_JASP['miss_1'] =save_dict_0['misses'],[i for i in save_dict_1['misses']]
#         save_dict_JASP['error_0'],save_dict_JASP['error_1'] =save_dict_0['incorrect'],[i for i in save_dict_1['incorrect']]
#         fin_dat_experi.append((curr_id,data_id,save_dict,save_dict_JASP))
#         fin_datfin = fin_datfin.append(save_dict)
#         fin_dat_JASP = fin_dat_JASP.append(save_dict_JASP)
#     DATA_total.append((data_type,fin_dat_experi,fin_datfin.sort_values('ID'),fin_dat_JASP.sort_values('id')))
       
# ### get Baseline into DF as another WS-FActor+
# erc = []
# for dat_bl,dat_exp in zip(DATA_total[0][1],DATA_total[1][1]):
#     DF_curr_id_bl = dat_bl[3]
#     DF_curr_id_exp = dat_exp[3]
    
#     erc.append((dat_bl,dat_exp))
    
        


# DATA_rt = DATA_total
# data_raw = DATA_rt[1][2]
# data_raw['ID'] = data_raw['ID'].copy().astype('int32')
# data_raw['block_cond'] = data_raw['block_cond'].copy().astype('int32')
# data_raw['trial_type'] = data_raw['trial_type'].copy().replace({'AX':1,
#                                                                 'BX':2,
#                                                                 'AY':3,
#                                                                 'BY':4})
# data = data_raw.sort_values('ID')
# groups_raw = pd.read_csv(r'C:\Users\de_hauk\Desktop\VP_Zuordnung.txt',sep ='\t').sort_values('id')
# groups = groups_raw.loc[groups_raw['id'] != 22]
# ids_list = []
# conds_list = []
# for ids,group in zip(groups['id'],groups['group']):
#     aaa = [ids] *8
#     ids_list = ids_list +aaa 
#     bbb = [group] *8 
#     conds_list = conds_list + bbb
# data['ids'],data['BS_group'] = ids_list,conds_list
# check_u = data['ids'] == data['ID']



# data.to_csv(r'C:\Users\de_hauk\Desktop\data.csv', sep=',' )

# ###Data for JASP

# group_BS = groups.copy()
# data_JASP = DATA_rt[1][3]
# data_JASP['id'] = data_JASP['id'].copy().astype('int32')
# data_JASP = data_JASP.sort_values('id').copy()

# check_ids = group_BS['id'] == np.unique(data_JASP['id'])
# group_JASP = []
# for i,j in zip(group_BS['id'],group_BS['group']):
#     group_JASP = group_JASP + [j]*4
    
# data_JASP['bs_group'] = group_JASP
    
# data_JASP.to_csv(r'C:\Users\de_hauk\Desktop\data_JASP.csv', sep=',' )

# data_PG = DATA_rt[1][2]
# #res = pg.mixed_anova(data=data_PG, dv='mean', subject ='ID', between=['trial_type','BS_group'], within ='block_cond', effsize='np2')

