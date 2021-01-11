import numpy as np
import pandas as pd


'''
getTasks returns a DataFrame of finshed tasks with start and end days and a
dataframe of not finshed task with just start days
thanks to @epogrebnyak for the refactor help''

getTaskstoFinish return a dataFrame of a specific# of finshed tasks start 
and end days 
'''


def get_cards(days: int):
    return [np.random.choice(["b", "r"]) for _ in range(days)]

def getTasks(days, wip_limit, seed = None, people=1):
    if seed != None :
        np.random.seed(seed)
    
    cards = get_cards(days)

# this can be a funciton that returns 'finished_tasks'
    stacks = []  # will have same length as 'cards'
    finished_tasks = []
    running_wip = []
    current_stack = []  # need this for 1st run
    for day in range(days):
        cards = get_cards(people)
         
        for card in cards:
            # with red card we finish one already accumulated task
            if card == "r" and len(current_stack) > 0:
                day_started = current_stack.pop(0)
                dict_ = dict(day_started=day_started, day_ended=day)
                finished_tasks.append(dict_)
            # with black card we accumulate a new task
            # we skip a task if stack is above wip_limit
            elif card == "b" and len(current_stack) < wip_limit:
                current_stack.append(day)
            #print("Day", day, "Tasks in queue:", current_stack)
            stacks.append(current_stack.copy())
        running_wip.append(len(current_stack))
    finished_tasks_df = pd.DataFrame(finished_tasks)
    not_finished_task_df = pd.DataFrame(current_stack)
    running_wip_df = pd.DataFrame(running_wip)
    return finished_tasks_df, not_finished_task_df, running_wip_df



def getTaskstoFinish(wip_limit, seed = None, tasks=27, people=4):
    if seed != None :
        np.random.seed(seed)
    
    unning_wip = []
    stacks = []  # will have same length as 'cards'
    finished_tasks = []
    current_stack = [1]  # need this for 1st run
    running_wip = []
    day = 0
    while tasks > 0:
        day = day + 1
        # with red card we finish one already accumulated task
        cards = get_cards(people)
        for card in cards:
            if card == "r" and len(current_stack) > 0:
                day_started = current_stack.pop(0)
                dict_ = dict(day_started=day_started, day_ended=day)
                finished_tasks.append(dict_)
                tasks = tasks - 1
            # with black card we accumulate a new task
            # we skip a task if stack is above wip_limit
            elif card == "b" and len(current_stack) < wip_limit:
                current_stack.append(day)
            #print("Day", day, "Tasks in queue:", current_stack)
            stacks.append(current_stack.copy())  
        running_wip.append(len(current_stack))
    # end of function
    
    # previously was 'all_items'
    finished_tasks_df = pd.DataFrame(finished_tasks)
    running_wip_df = pd.DataFrame(running_wip)
    
    
   
 
    return finished_tasks_df, running_wip_df
