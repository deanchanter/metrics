[
 ]#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:21:01 2020

@author: deanchanter
"""

# Python code for 1-D random walk. 
#import random 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd


runs = 100

#limit_list= [3,4,5,6,7,8,9,10,15,20,25,50, 101]
limit_list = [1,2]

all_items = pd.DataFrame(0, index=range(runs*len(limit_list)+1),
                         columns=["Start_Day","End_Day", 'WIP_Limit'])



next_item_to_start = -1
for wipLimit in limit_list:
    np.random.seed(45)  #23,45,10 
    next_item_to_start = next_item_to_start + 1
    next_item_to_end = next_item_to_start
    all_items["Start_Day"][next_item_to_start] = 1
    all_items["WIP_Limit"][next_item_to_start] = wipLimit 
    wip = 1
    for day in range(runs) :
        br = np.random.choice(['b','r'])
        if br == 'r' and wip > 0 :                        
            all_items["End_Day"][next_item_to_end] = day + 1
            wip = wip - 1
            next_item_to_end = next_item_to_end + 1
            
        elif br == 'b' and wip < wipLimit :
            print(wip)
            print(wipLimit)
            all_items["WIP_Limit"][next_item_to_start] = wipLimit
            all_items["Start_Day"][next_item_to_start] = day + 1
            wip = wip + 1
            next_item_to_start = next_item_to_start + 1
            
        else:
            wip = wip

#shave
all_items = all_items[all_items['WIP_Limit'] > 0 ]  



#dump master to CSV/Clipboard
#all_items.to_csv("randomSample")
#all_items.to_clipboard()                                   
                           

#build Cycle Time Slice                       
all_items['CT'] = all_items["End_Day"] - all_items["Start_Day"]  + 1 


all_items_done = all_items[all_items['CT'] > 1 ]



#build Throughput Slice
throughput = all_items_done.copy()[['End_Day','WIP_Limit']]
throughput['Week_Num'] = throughput["End_Day"].floordiv(7) + 1

#print(throughput)

throughput_wip = throughput.groupby('WIP_Limit')['End_Day'].count()


#throughtputRunning = throughput_week.groupby(['WIP_Limit',])['']

#print(throughtputnning)


#plot
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)



max_Ct = all_items_done.groupby("WIP_Limit")['CT'].max()



max_Ct.plot.bar(ax=ax1)
print(throughput_wip)
throughput_wip.plot.bar(ax=ax2)




all_item_not_done = all_items[all_items['CT'] < -1].groupby("WIP_Limit")['CT'].count()

all_item_not_done.plot.bar(ax=ax3)

print(all_item_not_done)




#throughtputRunning.plot(ax=ax)

                                                
#throughput_week.plot.bar(ax = ax2)
#fig =bar.get_figure()

#all_items_done.plot.scatter(ax=ax3, x='End_Day', y='Cycle_Time')                                         





#CT Scatter
#plt.xlabel("Day Item Done")
#plt.ylabel("CycleTime")
#plt.scatter(all_items_done["End_Day"],all_items_done['CT'])
#plt.show() 


#throughtput = all_items_done.groupby()
