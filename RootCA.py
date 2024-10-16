import matplotlib.pyplot as plt 
import numpy as np 
import random
from matplotlib.colors import ListedColormap
import matplotlib.colors as mcolors

# 0 is soil, 1 is root, 2 is nutrients
size = 250
environment = np.zeros((size,size))
next_steps = np.zeros((size,size))
random_distribution = False
time_steps = 200
high_prob = .8
med_prob = .075 # 2x
low_prob = .025 # 2x
no_move_prob = 0
nutrient_bias = 0
downward_bias = 0

cmap = ListedColormap([mcolors.TABLEAU_COLORS['tab:brown'], "White", "Green"])

if random_distribution == True:
    percent_nutrients = .1
    for i in range(size):
        for j in range(size):
            coin_toss = random.uniform(0, 1)
            if coin_toss <= percent_nutrients:
                environment[i,j] = 2

else:
    environment[:200, 125] = 2

environment[0, 125] = 1
plt.figure()
img = plt.imshow(environment, cmap=cmap)
plt.colorbar()

for step in range(time_steps):
    next_steps = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            if environment[i,j] == 0 or environment[i,j] == 2:
                if next_steps[i,j] != 1:
                    next_steps[i,j] = environment[i,j]
                
            else:
                next_steps[i,j] = 1
                if j - 1 > 0:
                    left = environment[i,j - 1]
                else: 
                    left = None
                
                if j + 1 < size:
                    right = environment[i,j + 1]
                else: 
                    right = None
                if i - 1 > 0:
                    up = environment[i - 1,j]
                else: 
                    up = None
                if i + 1 < size:
                    down = environment[i+1,j]
                else: 
                    down = None
                if left != None and up != None:
                    up_left = environment[i - 1, j - 1]
                else:
                    up_left = None
                if right != None and up != None:
                    up_right = environment[i - 1, j + 1]
                else:
                    up_right = None
                if left != None and down != None:
                    down_left = environment[i + 1, j - 1]
                else:
                    down_left = None
                if right != None and down != None:
                    down_right = environment[i + 1, j + 1]
                else:
                    down_right = None
                    
                all_directions = np.array([up, down, left, right, up_left, up_right, down_left, down_right])
                is_root = all_directions == 1
                total_roots = np.sum(is_root)
                is_nutrients = all_directions == 2
                total_nutrients = np.sum(is_nutrients)
                moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1), (0, 0)]
                
                if total_roots == 0:
                    is_availible = (all_directions == 0) | (all_directions == 2)
                    availible_inds = np.where(is_availible)[0]
                    #probs = np.ones(len(moves)) * low_prob 
                    probs = np.zeros(len(moves))
                                        
                    for ind in availible_inds:
                        if all_directions[ind] == 2: 
                            probs[ind] += nutrient_bias
                        else:  
                            probs[ind] = 1 / len(availible_inds)
                    
                    for ind, move_direction in enumerate(moves):
                        if ind in [1, 6, 7]:  # down, down_left, down_right
                            probs[ind] += downward_bias
                    
                    probs = probs / np.sum(probs)  
                    move = random.choices(moves, weights=probs, k=1)
                    new_i = i + move[0][0]
                    new_j = j + move[0][1]
                
                    if 0 <= new_i < size and 0 <= new_j < size:
                        next_steps[new_i, new_j] = 1
                
                elif total_roots == 1:
                    location_of_root = np.where(all_directions == 1)[0]
                    if location_of_root == 0:
                        probs = [0, high_prob, low_prob, low_prob, 0, 0, med_prob, med_prob, no_move_prob]
                    if location_of_root == 1:
                        probs = [high_prob, 0,low_prob,low_prob,med_prob,med_prob, 0, 0, no_move_prob]
                    if location_of_root == 2:
                        probs = [low_prob,low_prob,0,high_prob, 0, med_prob, 0, med_prob, no_move_prob]
                    if location_of_root == 3:
                        probs = [low_prob,low_prob,high_prob,0, med_prob, 0, med_prob, 0, no_move_prob]
                    if location_of_root == 4:
                        probs = [0, med_prob, 0, med_prob, 0, low_prob, low_prob, high_prob, no_move_prob]
                    if location_of_root == 5:
                        probs = [0, med_prob, med_prob, 0, low_prob, 0, high_prob, low_prob, no_move_prob]
                    if location_of_root == 6:
                        probs = [med_prob, 0, 0, med_prob, low_prob, high_prob, 0, low_prob, no_move_prob]
                    if location_of_root == 7:
                        probs = [med_prob, 0, med_prob, 0, high_prob, low_prob, low_prob, 0, no_move_prob]
                    
                    
                    for ind, direction in enumerate(all_directions):
                        if direction == 2:  # Nutrient in that direction
                            probs[ind] += nutrient_bias
                        
                   
                    for ind, move_direction in enumerate(moves):
                        if ind in [1, 6, 7]:  # down, down_left, down_right
                            if probs[ind] > 0:
                                probs[ind] += downward_bias
                    
                    probs = np.array(probs) / np.sum(probs)  
                    move = random.choices(moves, weights=probs, k=1)
                    new_i = i + move[0][0]
                    new_j = j + move[0][1]
                
                    if 0 <= new_i < size and 0 <= new_j < size:
                        next_steps[new_i, new_j] = 1
                
                elif total_roots == 2:
                    is_availible = (all_directions == 0) | (all_directions == 2)
                    availible_inds = np.where(is_availible)[0]
                    probs = np.zeros(len(moves)) 
                    
                    
                    probs[-1] = .70
                    
                    for ind in availible_inds:
                        if all_directions[ind] == 2:  
                            probs[ind] += nutrient_bias
                        else:
                            probs[ind] += .05
                    
                    
                            
                    probs = np.array(probs) / np.sum(probs)  
                    move = random.choices(moves, weights=probs, k=1)
                    new_i = i + move[0][0]
                    new_j = j + move[0][1]
                    
                    if 0 <= new_i < size and 0 <= new_j < size:
                        next_steps[new_i, new_j] = 1
                
                elif total_roots == 3:
                    is_availible = (all_directions == 0) | (all_directions == 2)
                    availible_inds = np.where(is_availible)[0]
                    probs = np.zeros(len(moves)) 
                    
                   
                    probs[-1] = .95
                    
                    
                    for ind in availible_inds:
                        if all_directions[ind] == 2:  
                            probs[ind] += nutrient_bias
                        else:
                            probs[ind] += .01
                    
                    probs = np.array(probs) / np.sum(probs)  
                    move = random.choices(moves, weights=probs, k=1)
                    new_i = i + move[0][0]
                    new_j = j + move[0][1]
                    
                    if 0 <= new_i < size and 0 <= new_j < size:
                        next_steps[new_i, new_j] = 1
                else:
                    pass
                    
            
    environment = next_steps
    print(step)
    
    img.set_data(environment)
    plt.draw()
    plt.title(f"{step}")
    plt.pause(0.1)