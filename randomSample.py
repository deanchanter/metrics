"""This is simple simulation script that gives the user a way to 
generate sample data for development of agile metrics in other enviroments.

The core (of will be func'ed out in the future) is a simulation of 
picking  Red and Black cards to decided if a item can make progress.  
At the end of 100 "days" it writes CSV. It also creates simple 
plot to show what a cycle time and throughput chart might look like.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from getTask import getTasks


finished_tasks, not_finshed_tasks = getTasks(100,10)




# dump to CSV
finished_tasks.to_csv("randomSample")


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
fig.tight_layout()
throughput["Weekly Throughput"].plot.bar(ax=axes[0,0])
throughput["Running Total Throuphput"].plot(ax=axes[1,0])

# Cycle Time Plot

finished_tasks.plot.scatter(x="day_ended", y="Cycle_Time" ,ax=axes[0,1])


#make an aging slice

not_finshed_tasks.columns=["day_started"]

not_finshed_tasks["days_old"] = 100 -  not_finshed_tasks["day_started"]
not_finshed_tasks.index.name='task#'
print(not_finshed_tasks)

lefts = not_finshed_tasks['day_started'].to_list()

#lefts=[1,2,3]

not_finshed_tasks["days_old"].plot.barh(ax=axes[1,1],legend=False, left=lefts)





