[]  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:21:01 2020

@author: deanchanter

This a simulation to study different WIP Limits on the effect of work progress
in "world"  where work as a 50/50 probabilty of completing each "day."

In current state setting runs to 1 is the only thing that works. ToDo: refactor
post data slicing to account for multiple runs

The ulitate goal is to push runs to 1MM and create distorbution. 

My Hypothise is the WIP Limits b/t 3-6 is ideal to balalce Cycle Time, Throughtput
and Quequed work (item not done but in progress at the end of 100 days )

"""

import pandas as pd
from getTask import getTasks



runs = 5000
days = 100
#limit = 3


limit_list= [3,5,7,10,25]
#limit_list = [3,5]

cycletimedf = pd.DataFrame()

#repeatable results
#np.random.seed(23)  #23,45,10 
#ct95th
for limit in limit_list:
    ct85thlist = []
    for run in range(runs):
        finished_tasks, not_finished_tasks = getTasks(days,limit)
        # Build a Cycle Time Slice (End Day - Start Day for each Item/Index)
        finished_tasks["Cycle_Time"] = finished_tasks["day_ended"] - finished_tasks["day_started"] + 1
        ct85th = int(finished_tasks["Cycle_Time"].quantile(.85))
        ct85thlist.append(ct85th)
    cycletimedf[limit] = ct85thlist

cycletimedf.plot.hist(bins=50)
                                          






