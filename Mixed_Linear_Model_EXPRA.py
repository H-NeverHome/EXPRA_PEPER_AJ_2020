# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:04:53 2020

@author: de_hauk
"""

import statsmodels.api as sm

import statsmodels.formula.api as smf

data = sm.datasets.get_rdataset("dietox", "geepack").data

md = smf.mixedlm("Weight ~ Time", data, groups=data["Pig"])

mdf = md.fit()