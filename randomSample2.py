import numpy as np
import pandas as pd


def get_cards(days: int):
    return [np.random.choice(["b", "r"]) for _ in range(days)]


np.random.seed(45)

wip_limit = 3
days = 100

cards = get_cards(days)

# this can be a funciton that returns 'finished_tasks'
stacks = []  # will have same length as 'cards'
finished_tasks = []
current_stack = []  # need this for 1st run
for day, card in enumerate(cards):
    # with red card we finish one already accumulated task
    if card == "r" and len(current_stack) > 0:
        day_started = current_stack.pop(0)
        dict_ = dict(day_started=day_started, day_ended=day)
        finished_tasks.append(dict_)
    # with black card we accumulate a new task
    # we skip a task if stack is above wip_limit
    elif card == "b" and len(current_stack) < wip_limit:
        current_stack.append(day)
    print("Day", day, "Tasks in queue:", current_stack)
    stacks.append(current_stack.copy())
# end of function

# previously was 'all_items'
finished_tasks_df = pd.DataFrame(finished_tasks)
