[
 ]#!/usr/bin/env python3
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

# Python code for 1-D random walk. 
#import random 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd



runs = 1
days = 100

limit_list= [3,4,5,6,7,8,9,10,15,20,25,50, 101]
#limit_list = [3,4,5]

#repeatable results
np.random.seed(23)  #23,45,10 

all_items = pd.DataFrame(0, index=range(days*runs*len(limit_list)+1),
                         columns=["Start_Day","End_Day", 'WIP_Limit'])

next_item_to_start = -1

for run in range(runs):
    for wipLimit in limit_list:
        next_item_to_start = next_item_to_start + 1
        next_item_to_end = next_item_to_start
        all_items["Start_Day"][next_item_to_start] = 1
        all_items["WIP_Limit"][next_item_to_start] = wipLimit 
        wip = 1
    
        for day in range(days) :
            
            br = np.random.choice(['b','r'])
            
            if br == 'r' and wip > 0 :                        
                all_items["End_Day"][next_item_to_end] = day + 1
                wip = wip - 1
                next_item_to_end = next_item_to_end + 1
                
            elif br == 'b' and wip < wipLimit :
                all_items["WIP_Limit"][next_item_to_start] = wipLimit
                all_items["Start_Day"][next_item_to_start] = day + 1
                wip = wip + 1
                next_item_to_start = next_item_to_start + 1
                
            else:
                wip = wip



#shave the dataFrame
all_items = all_items[all_items['WIP_Limit'] > 0 ]  





#build Cycle Time Slice 
#TODO one line this                    
all_items['CT'] = all_items["End_Day"] - all_items["Start_Day"]  + 1 
all_items_done = all_items[all_items['CT'] > 1 ]
max_Ct = all_items_done.groupby("WIP_Limit")['CT'].max()


#build Throughput Slice
#TODO one line this 
throughput = all_items_done.copy()[['End_Day','WIP_Limit']]
throughput['Week_Num'] = throughput["End_Day"].floordiv(7) + 1
throughput_wip = throughput.groupby('WIP_Limit')['End_Day'].count()

#build Slice the shows not what is not finished
all_item_not_done = all_items[all_items['CT'] < -1].groupby("WIP_Limit")['CT'].count()



 

#plot
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)
max_Ct.plot.bar(ax=ax1)
throughput_wip.plot.bar(ax=ax2)
all_item_not_done.plot.bar(ax=ax3)                                          






