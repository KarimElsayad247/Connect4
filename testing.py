import minimax
import GameState
import math
import time
from importlib import reload
import numpy as np
from matplotlib import pyplot as plt

#%%
reload(plt)

# %%
initial_state_string = '000000000000000000000000000000000000000000'
initial_state = GameState.GameState(initial_state_string, GameState.AI_PLAYER, None)
action_sequence = [3, 4, 2, 5, 6]
repeats = 3
k_minimax = [1, 2, 3, 4, 5, 6, 7]
k_alphabeta = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#%%
data_points_minimax = []

state = initial_state

for k in k_minimax:
    avgDuration = 0
    for i in range(repeats):
        duration = 0
        for action in action_sequence:
            state = initial_state.makeMove(action)
            startTime = time.time()
            action = minimax.decisionMinimax(state, k)
            endTime = time.time()
            duration += (endTime - startTime)
             
        avgDuration += (duration / len(action_sequence))
    
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

for k in k_alphabeta:
    avgDuration = 0
    for i in range(repeats):
        duration = 0
        for action in action_sequence:
            state = initial_state.makeMove(action)
            startTime = time.time()
            action = minimax.decisionAlphaBeta(state, -math.inf, +math.inf, k)
            endTime = time.time()
            duration += (endTime - startTime)
             
        avgDuration += (duration / len(action_sequence))
    print(f'Depth {k} done')
    data_points_ab.append(avgDuration/repeats)
print('Done')

#%%
figure = plt.figure(figsize=(12,12))
plt.style.use('fivethirtyeight')
plt.plot(k_minimax, data_points_minimax, label='No Pruning')
plt.plot(k_alphabeta, data_points_ab, label='With Pruning')

plt.xlabel("Maximum Depth")
plt.ylabel("Time (in seconds)")
plt.xticks(k_alphabeta)
plt.legend()

plt.show()



























