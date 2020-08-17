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
from getTask import getTaskstoFinish
from datetime import datetime


runs = 1000
#days = 100
#limit = 3


limit_list= [3,4,5,7,11]
#limit_list = [3,5]

cycletimedf = pd.DataFrame()
throughtputdf = pd.DataFrame()
cycletime_maxdf = pd.DataFrame()
running_wipdf = pd.DataFrame()

#repeatable results
#np.random.seed(23)  #23,45,10 
#ct95th



for limit in limit_list:
    print("Limit:",limit)
    ctavglist = []
    ctmaxlist = []
    tptlist = []
    rwiplist = []
   
    for run in range(runs):
        finished_tasks, running_wip = getTaskstoFinish(limit,people=4,tasks=100)
        # Build a Cycle Time Slice (End Day - Start Day for each Item/Index)
        finished_tasks["Cycle_Time"] = finished_tasks["day_ended"] - finished_tasks["day_started"] + 1
        ctavg= finished_tasks["Cycle_Time"].mean()
        ctavglist.append(ctavg)
        
        #Build a Aging (Max CT) Slice
        ctmax = finished_tasks['Cycle_Time'].max()
        ctmaxlist.append(ctmax)
        
        #Build a Throughput slice
        numdays = finished_tasks.iloc[-1]["day_ended"]
        tpt = finished_tasks["day_ended"].count()/numdays
        tptlist.append(tpt)
        
        #Build a WIP Slice
        running_wipavg = running_wip[0].mean()
        rwiplist.append(running_wipavg)
        
        
    cycletimedf[limit] = ctavglist
    throughtputdf[limit] = tptlist
    cycletime_maxdf[limit] = ctmaxlist
    running_wipdf[limit] = rwiplist
   


cycletimedf.to_csv('ct.csv')
throughtputdf.to_csv('tp.csv')
cycletime_maxdf.to_csv('ctmax.csv')


ct = cycletimedf.plot.hist(alpha=.5, bins=25)
ct.set(title="Cycle Time",xlabel="Average Cycle Time (Days)")

tp = throughtputdf.plot.hist(alpha=.6)
tp.set(title= "Throughput", xlabel="Average # of Items per Day")

ctm = cycletime_maxdf.plot.hist(alpha=.6)
ctm.set(title="Max Age", xlabel= "Max Age (Days)")

rw = running_wipdf.plot.hist(alpha=.6, bins=30)
rw.set(title="WIP", xlabel= "Average # of Items in Progress")





