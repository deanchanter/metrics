"""This is simple simulation script that gives the user a way to 
generate sample data for development of agile metrics in other enviroments.

The core (of will be func'ed out in the future) is a simulation of 
picking  Red and Black cards to decided if a item can make progress.  
At the end of 100 "days" it writes CSV. It also creates simple 
plot to show what a cycle time and throughput chart might look like.
"""


import matplotlib.pyplot as plt
import pandas as pd
import getTask as gt


finished_tasks = gt.getTaskstoFinish(10, people=4, tasks=100)



# dump to CSV
finished_tasks.to_csv("randomSample.csv")


# Build a Cycle Time Slice (End Day - Start Day for each Item/Index)
finished_tasks["Cycle_Time"] = finished_tasks["day_ended"] - finished_tasks["day_started"] + 1


# Build a Throuphout Slice (Count of Items the Ended for a given week)
throughput = pd.DataFrame(finished_tasks["day_ended"].floordiv(7) + 1)
throughput = throughput.reset_index()
throughput.columns=["Task#","Week"]
throughput = pd.DataFrame(throughput.groupby("Week")["Task#"].count())
throughput.columns=['Weekly Throughput']

# Running Total Throughput
throughput["Running Total Throuphput"] = throughput['Weekly Throughput'].cumsum()


# plot for reference
# Throughtput plot
fig, axes = plt.subplots(2, 2)
#fig.subplots_adjust(wspace=1, hspace=1, left=0.125,right=0.9,top=2,bottom=0.9)
fig.tight_layout(w_pad=1.5, h_pad=4.0)

throughput["Weekly Throughput"].plot.bar(ax=axes[0,0])
axes[0,0].set(title="Weekly Throughput", xlabel = "Time (Weeks)", ylabel="# of items completed")
throughput["Running Total Throuphput"].plot(ax=axes[1,0])
axes[1,0].set(title="Cumulative Throughtput",xlabel = "Time (Weeks)", ylabel="# of items completed")

# Cycle Time Plot

finished_tasks.plot.scatter(x="day_ended", y="Cycle_Time" ,ax=axes[0,1])
axes[0,1].set(title="Cycle Time Scatter Plot",xlabel = "Time (Days)", ylabel="# of days in prgress")


#make an aging slice and chart if there are leftover tasks
'''
if len(not_finshed_tasks.index) > 0: 
    not_finshed_tasks.columns=["day_started"] 
    not_finshed_tasks["days_old"] = 100 -  not_finshed_tasks["day_started"]
    not_finshed_tasks.index.name='task#'
    lefts = not_finshed_tasks['day_started'].to_list()
    not_finshed_tasks["days_old"].plot.barh(ax=axes[1,1],legend=False, left=lefts)
    
    axes[1,1].set(title="Aging Plot",xlabel = "Time (Days)")
    axes[1,1].axes.yaxis.set_visible(False)
'''




