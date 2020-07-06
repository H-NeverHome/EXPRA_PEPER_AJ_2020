# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:26:33 2020

@author: de_hauk
"""

import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import scipy
from scipy import stats

np.random.seed(1993)

n_times = 2

#### T1
n_groups=3
size_group = 40
size_sample = n_groups * size_group
group1 = np.random.normal(450,25,size_group)
group1_id = np.full(size_group,1)
group2 = np.random.normal(445,25,size_group)
group2_id = np.full(size_group,2)
group3 = np.random.normal(460,25,size_group)
group3_id = np.full(size_group,3)
