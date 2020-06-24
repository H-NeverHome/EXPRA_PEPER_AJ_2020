# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:07:23 2020

@author: hauke
"""

import pingouin as pg
import pandas as pd
import numpy as np
import seaborn as sns
### 3 treatment groups

one = np.random.normal(16,1.5,35)
two = np.random.normal(17,1.5,35)
three = np.random.normal(17.5,1.5,35)
group = np.append(np.full(len(one),1), [np.full(len(one),2), np.full(len(one),3)])
dict_dat = {'data': np.append(one, [two, three]),
            'group' : group}
data = pd.DataFrame(data = dict_dat)
# hello = np.zeros(35).fill(1)
# hello
# sns.kdeplot(data = one)
# sns.kdeplot(data = two)
# sns.kdeplot(data = three)
# sns.kdeplot(data = np.append(one, [two, three]))

res = pg.anova(data=data, dv='data', between='group', ss_type=2, detailed=True, effsize='np2')