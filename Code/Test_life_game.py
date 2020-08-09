# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:23:03 2020

@author: Arthur
"""
import life_game_indices as lgi
import life_game as lg
import antipattern as ap
import numpy as np
import math

test_matrix = np.asarray([[1,1,1,0],[1,1,0,1],[0,0,1,1],[1,0,1,0],[1,1,1,1]],dtype=np.int8)
lifegame_indices = lgi.LifeGame(test_matrix)
test_index = lifegame_indices.get_neighbours_indices([1,1])
lifegame_indices.set_neigbours_indices()

# a = [1,2,3]



# index = a.index(5)

# # read_values()
# n = 2
# n_patterns_power_horizontal = 2
# cell_size = 5
# anti_pattern = ap.AntiPattern(n)


# smallMatrix = anti_pattern.createMatrix(
#     n_patterns_power_horizontal = n_patterns_power_horizontal)
# # smallMatrix = [[]]
# smallArray = np.array(smallMatrix)
# desired_dimension = [150, 200]
# lambda_x = math.ceil((desired_dimension[0]-smallArray.shape[0])/2)
# lambda_y = math.ceil((desired_dimension[1]-smallArray.shape[1])/2)
# bigArray = np.pad(
#     smallArray, ((lambda_x,desired_dimension[0]-lambda_x-smallArray.shape[0]),
#     (lambda_y,desired_dimension[1]-lambda_y-smallArray.shape[1])),'constant')

# np_array = np.array(smallMatrix)

# lifegame_normal = lg.LifeGame(np_array, {"left": False})
# lifegame_normal.dict_neighbour_active
# test_dict = {"upper_left": False, "above": False,"upper_right": False}
# lifegame_normal.set_neighbours(test_dict)
# lifegame_normal.dict_neighbour_active

# lifegame_normal.matrix


# image = lifegame_normal.createGrid()
# image.show()

# lifegame_normal.next_step()
# image = lifegame_normal.createGrid()
# image.show()

# lifegame_normal.neighbours

# lifegame_normal.start_matrix

# #Tests

# n = 3
# n_patterns_power_horizontal = 5
# anti_pattern = ap.AntiPattern(n)
# smallMatrix = anti_pattern.createMatrix(
#     n_patterns_power_horizontal = n_patterns_power_horizontal)
# smallArray = np.array(smallMatrix)
# smallArray.shape
# desired_dimension = [150,200]
# lambda_x = math.ceil((desired_dimension[0]-smallArray.shape[0])/2)
# lambda_y = math.ceil((desired_dimension[1]-smallArray.shape[1])/2)
# bigArray = np.pad(
#     smallArray, ((lambda_x,desired_dimension[0]-lambda_x-smallArray.shape[0]),
#     (lambda_y,desired_dimension[1]-lambda_y-smallArray.shape[1])),'constant')




 # time for 150 by 200 matrix:
# %timeit lifegame_normal = lg.LifeGame(bigArray, left=False)
# 12.7 µs ± 124 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

# lifegame_normal = lg.LifeGame(bigArray, left=False)

# %timeit lifegame_normal.next_step()
# 511 ms ± 5.65 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)




# lifegame = lgm.LifeGame(
#     bigArray,edges_connect=True, neighbours_cell_alive=[3,4], neighbours_cell_dead=[3, 4], lower_left=False)

# image = lifegame.createGrid(cell_size=cell_size, show_gridlines=True, cell_margin=0)
# image.show()

# image = lifegame.createGrid(cell_size=cell_size, cell_margin=1)
# image.show()

# n = 150
# m = 200
# test_matrix = np.random.randint(2, size=(n, m), dtype=np.int8)

# test_class_lifegame = LifeGame(test_matrix,edges_connect=True, neighbours_cell_dead=[3,4])

# """" time for 150 by 200 matrix:
#     %timeit LifeGame(test_matrix)
# 7.79 s ± 75.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# %timeit test_class_lifegame.next_step()
# 257 ms ± 5.15 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# %timeit test_class_lifegame.createGrid()
# 76.8 ms ± 145 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)


# test_class_lifegame.return_to_initial_state()

# start_vector = np.copy(test_class_lifegame.start_vector)
# current_vector = test_class_lifegame.grid_vector
# # test_class_lifegame.next_step()
# transformation_matrix = test_class_lifegame.neighbours_transformation_matrix.todense()
# grid_matrix = np.copy(test_class_lifegame.grid_vector.reshape((n, m)))
# neighbours_vector = test_class_lifegame.get_neighbours_vector()
# neighbours_matrix = neighbours_vector.reshape((n, m))
# image = test_class_lifegame.createGrid()
# grid_matrix_next = test_class_lifegame.grid_vector.reshape((n, m))


# test_class_lifegame.neighbours_vector.nonzero()[0]
# np.union1d(test_class_lifegame.neighbours_vector.nonzero()[0], grid_matrix.flatten().nonzero()[0])

# startArray = np.copy(np.array(bigArray, dtype=np.int8))
# test_life_anti = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[3,4])

# path = r'D:\My documents\Python\images\weave\test\test'
# n_steps = 300

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti.createGrid()
#     now = datetime.now()
#     counter = test_life_anti.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti.next_step()

# test_life_anti2 = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[3,4],left=False,above=False)
# path = r'D:\My documents\Python\images\weave\test\test2'
# n_steps = 300

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti2.createGrid()
#     now = datetime.now()
#     counter = test_life_anti2.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti2.next_step()

# test_life_anti3 = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[1,3],left=False,right=False)
# path = r'D:\My documents\Python\images\weave\test\test3'
# n_steps = 300

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti3.createGrid()
#     now = datetime.now()
#     counter = test_life_anti3.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti3.next_step()

# test_life_anti4 = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[2,3],left=False,right=False)
# path = r'D:\My documents\Python\images\weave\test\test4'
# n_steps = 300

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti4.createGrid()
#     now = datetime.now()
#     counter = test_life_anti4.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti4.next_step()

#     #not interesting
# test_life_anti5 = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[4,5],left=False,right=False)
# path = r'D:\My documents\Python\images\weave\test\test5'
# n_steps = 80

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti5.createGrid()
#     now = datetime.now()
#     counter = test_life_anti5.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti5.next_step()

#     #not interesting
# test_life_anti5 = LifeGame(startArray, edges_connect=True, neighbours_cell_dead=[4,5],left=False,right=False)
# path = r'D:\My documents\Python\images\weave\test\test5'
# n_steps = 80

# for step in range(n_steps):
#     print(step)
#     image = test_life_anti5.createGrid()
#     now = datetime.now()
#     counter = test_life_anti5.counter
#     name = f'{now.strftime("%Y%m%d%H%M")}{now.second}{now.microsecond}_test_{counter}.bmp'
#     image.save(os.path.join(path,name))
#     test_life_anti5.next_step()

