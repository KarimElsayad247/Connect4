import minimax
import GameState
import math
import time
from importlib import reload
import numpy as np
from matplotlib import pyplot as plt
from ete3 import Tree

#%%
reload(plt)

#%%
def countExpandedNodes(root: Tree):
    
    if root.is_leaf():
        return 0
    else:
        totalExpandedChildren = 0
        for child in root.children:
            totalExpandedChildren += countExpandedNodes(child)
        return 1 + totalExpandedChildren 
    


# %%
initial_state_string = '000000000000000000000000000000000000000000'
initial_state = GameState.GameState(initial_state_string, GameState.AI_PLAYER, None)
action_sequence = [3]
repeats = 1
k_minimax = [1, 2, 3, 4, 5, 6]
k_alphabeta = [1, 2, 3, 4, 5, 6, 7]
#%%
data_points_minimax = []

tree_points_noab = []

state = initial_state

for k in k_minimax:
    avgDuration = 0
    for i in range(repeats):
        duration = 0
        for action in action_sequence:
            state = initial_state.makeMove(action)
            startTime = time.time()
            action, tree = minimax.decisionMinimax(state, k)
            endTime = time.time()
            duration += (endTime - startTime)
             
        avgDuration += (duration / len(action_sequence))
    tree_points_noab.append(countExpandedNodes(tree))
    data_points_minimax.append(avgDuration/repeats)

#%%
duration = 0
for action in [2,3]:
    state = initial_state.makeMove(action)
    startTime = time.time()
    action = minimax.decisionMinimax(state, 7)
    endTime = time.time()
    duration += (endTime - startTime)
avg = duration/2
print(avg)

#%%
data_points_ab = []
state = initial_state
tree_points_ab = []
for k in k_alphabeta:
    avgDuration = 0
    for i in range(repeats):
        duration = 0
        for action in action_sequence:
            state = initial_state.makeMove(action)
            startTime = time.time()
            action, tree = minimax.decisionAlphaBeta(state, -math.inf, +math.inf, k)
            endTime = time.time()
            duration += (endTime - startTime)
             
        avgDuration += (duration / len(action_sequence))
    print(f'Depth {k} done')
    tree_points_ab.append(countExpandedNodes(tree))
    data_points_ab.append(avgDuration/repeats)
print('Done')

#%%

SMALL_SIZE = 26
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

plt.style.use('fivethirtyeight')

#%%
figure = plt.figure(figsize=(16,10))

plt.plot(k_minimax, data_points_minimax, label='No Pruning')
plt.plot(k_alphabeta, data_points_ab, label='With Pruning')

plt.xlabel("Maximum Depth")
plt.ylabel("Time (in seconds)")
plt.xticks(k_alphabeta)
plt.legend()

plt.show()

#%%
figure2 = plt.figure(figsize=(16,10))

plt.plot(k_minimax, tree_points_noab, label='No Pruning')
plt.plot(k_alphabeta, tree_points_ab, label='With Pruning')

plt.xlabel("Maximum Depth")
plt.ylabel("Number of expanded nodes")
plt.xticks(k_alphabeta)
plt.legend()

plt.show()























