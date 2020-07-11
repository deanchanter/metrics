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


days = 100


#Data Frame indexed by "item"
all_items = pd.DataFrame(0, index=range(days),
                         columns=["Start_Day","End_Day"])

#Item 0 Day 1
all_items["Start_Day"][0] = 1
next_item_to_start = 1
next_item_to_end = 0
wip = 1

#This is a huge control  see WIPStudy to see why I picked 3
wipLimit = 3

#repeatable results
np.random.seed(45)  #23,45,10 


   
for day in range(days) :
    #same odds as a deck of cards: black = no progress (start something ) new
    #red = finish something (This is the same logic as a 1 person 1 WIP Featureban)
    
    br = np.random.choice(['b','r'])
    
    if br == 'r' and wip > 0 :                        
        all_items["End_Day"][next_item_to_end] = day + 1
        wip = wip - 1
        next_item_to_end = next_item_to_end + 1
        
    elif br == 'b' and wip < wipLimit :
        all_items["Start_Day"][next_item_to_start] = day + 1
        wip = wip + 1
        next_item_to_start = next_item_to_start + 1
        
    else:
        wip = wip




#dump master to CSV/Clipboard
all_items.to_csv("randomSample")
all_items.to_clipboard()                                   
                           

#plot to check                          
all_items['Cycle_Time'] = all_items["End_Day"] - all_items["Start_Day"]  + 1 
                                            
all_items_done = all_items[all_items['Cycle_Time'] > 1 ]



throughput = all_items_done.copy()[['End_Day']]

throughput['Week'] = throughput["End_Day"].floordiv(7) + 1

throughput_week = throughput.groupby('Week')['End_Day'].count()

throughtputRunning = throughput.groupby('Week').count().cumsum()

throughtputRunning.rename(columns={'End_Day': "Running_Total"}, inplace=True)


print(throughtputRunning)


fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)



tr = throughtputRunning.plot(ax=ax2)


                                                
throughput_week.plot.bar(ax = ax1, title = 'Throughtput')
#fig =bar.get_figure()


all_items_done.plot.scatter(x='End_Day', y='Cycle_Time')









