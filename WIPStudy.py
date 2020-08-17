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

def run_WIP_study(runs=100,days=100,limit_list=[3,5,7], bins=10, alpha=.6):

    #runs = 100000
    #days = 100
    #limit = 3
    
    
    #limit_list= [3,5,7,10,25,101]
    #limit_list = [3,5]
    
    cycletimedf = pd.DataFrame()
    throughtputdf = pd.DataFrame()
    notfinishedtotaldf = pd.DataFrame()
    notfinishedagedf = pd.DataFrame()
    
    #repeatable results
    #np.random.seed(23)  #23,45,10 
    #ct95th
    
    for limit in limit_list:
        print("Limit:",limit)
        ct85thlist = []
        tptlist = []
        nftlisit = []
        nfalisit = []
        for run in range(runs):
            #if run % 1000 == 0:
                #print(run)
            finished_tasks, not_finished_tasks = getTasks(days,limit)
            # Build a Cycle Time Slice (End Day - Start Day for each Item/Index)
            finished_tasks["Cycle_Time"] = finished_tasks["day_ended"] - finished_tasks["day_started"] + 1
            ct85th = int(finished_tasks["Cycle_Time"].quantile(.85))
            ct85thlist.append(ct85th)
            
            #Build a Throughput slice
            tpt = finished_tasks["day_ended"].count()
            tptlist.append(tpt)
            
            #Buidling a aging slice
            if not_finished_tasks.empty:
                nftlisit.append(0)
                nfalisit.append(0)
             
            else:
                not_finished_tasks.columns=["day_started"]
                nftt = not_finished_tasks["day_started"].count()
                nftlisit.append(nftt)
            
                not_finished_tasks["days_old"] = 100 -  not_finished_tasks["day_started"]
                nfam = not_finished_tasks["days_old"].max()
                nfalisit.append(nfam)
           
    
                
            
            
        cycletimedf[limit] = ct85thlist
        throughtputdf[limit] = tptlist
        notfinishedtotaldf[limit] = nftlisit
        notfinishedagedf[limit] = nfalisit
        
    cycletimedf.to_csv('ct.csv')
    throughtputdf.to_csv('tp.csv')
    notfinishedagedf.to_csv('nf.csv')
    notfinishedagedf.to_csv('age.csv')
    
    cycletimedf.plot.hist(bins=bins, alpha=alpha).set_title("Cycle Time")
    throughtputdf.plot.hist(bins=bins, alpha=alpha).set_title("Throughput")
    notfinishedtotaldf.plot.hist(bins=bins, alpha=alpha).set_title("# of WIP tasks ")
    notfinishedagedf.plot.hist(bins=bins, alpha=alpha).set_title("max age of WIP")
    return 0






