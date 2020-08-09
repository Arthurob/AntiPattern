# -*- coding: utf-8 -*.
"""
Created on Tue May 19 22:17:58 2020

@author: Arthur
"""
from PIL import Image, ImageDraw
import math
import numpy as np
import scipy.sparse as sparse
import os
from datetime import datetime

class LifeGame:

    def __init__(self, start_matrix, above=True, below=True, left=True,
                 right=True,upper_left=True, upper_right=True,
                 lower_left=True, lower_right=True, edges_connect=False,
                 include_corners=True, neighbours_cell_alive=[3, 4],
                 neighbours_cell_dead=[3, 3]):
        self.counter = 0
        self.start_matrix = start_matrix
        self.n = start_matrix.shape[0]
        self.m = start_matrix.shape[1]
        self.start_vector = start_matrix.flatten()
        self.grid_vector = np.copy(self.start_vector)
        self.edges_connect = edges_connect
        self.include_corners= include_corners
        self.above = above
        self.below = below
        self.left = left
        self.right = right

        if self.include_corners:
            self.upper_left = upper_left
            self.upper_right = upper_right
            self.lower_left = lower_left
            self.lower_right = lower_right
        else:
            self.upper_left = False
            self.upper_right = False
            self.lower_left = False
            self.lower_right = False

        self.neighbour_boolean = [self.upper_left, self.left, self.lower_left,
                                  self.above, self.below, self.upper_right,
                                  self.right, self.lower_right]
        self.size = self.n * self.m

        self.neighbours_cell_alive = neighbours_cell_alive
        self.neighbours_cell_dead = neighbours_cell_dead

        self.neighbours_transformation_matrix = np.zeros((self.size, self.size), dtype=np.int8)
        self.create_neighbours_transformation_matrix()
        self.neighbours_vector =np.zeros((self.n, self.m), dtype=np.int8)


    def create_neighbours_transformation_matrix(self):
        indices_neighbours_general_relative_to_l = np.array(
            [-self.m-1,-1,self.m-1,-self.m,self.m,-self.m+1,1,self.m+1])
        indices_neighbours_general_relative_to_l_with_booleans = indices_neighbours_general_relative_to_l * self.neighbour_boolean
        horizontals_general = [-1,0,1] #[left,right]
        verticals_general = [-self.m,0,self.m] #[up,dpwn]

        for l in range(self.size):
            row = math.floor(l/self.m)
            column = l%self.m
            #away from the edges:
            if (0 < row < self.n-1) & (0 < column < self.m-1):
                 indices_l_lneighbour = l + indices_neighbours_general_relative_to_l_with_booleans.copy()
            #at edges
            else:
                horizontals = horizontals_general.copy()
                verticals = verticals_general.copy()
                #Top row neighbour, if edges connect i = 0->i = self.n-1
                if row == 0:
                    if self.edges_connect:
                        verticals[0] = (self.n-1)*self.m
                    else:
                        verticals[0] = 0
                #bottum row neighbour
                elif row == (self.n-1):
                    if self.edges_connect:
                        verticals[2] = -(self.n-1)*self.m
                    else:
                        verticals[2] = 0

                if column == 0:
                    if self.edges_connect:
                        horizontals[0] = (self.m-1)
                    else:
                        horizontals[0] = 0
                if column == self.m-1:
                    if self.edges_connect:
                        horizontals[2] = -(self.m-1)
                    else:
                        horizontals[2] = 0

                indices_neighbours_relative_to_l_edges = np.array(
                    [horizontal+vertical for horizontal in horizontals for vertical in verticals ])
                indices_neighbours_relative_to_l_edges = np.delete(indices_neighbours_relative_to_l_edges,4)
                indices_l_lneighbour = l + np.unique(indices_neighbours_relative_to_l_edges * self.neighbour_boolean)
                indices_l_lneighbour = indices_l_lneighbour[indices_l_lneighbour != l]

            for l_neighbour in indices_l_lneighbour:
                self.neighbours_transformation_matrix[l, l_neighbour] = 1

        self.neighbours_transformation_matrix = sparse.csr_matrix(
            self.neighbours_transformation_matrix)

    def set_neighbours_booleans(self,above=True, below=True, left=True,
                 right=True,upper_left=True, upper_right=True,
                 lower_left=True, lower_right=True,include_corners = True):
        self.above = above
        self.below = below
        self.left = left
        self.right = right

        if include_corners:
            self.upper_left = upper_left
            self.upper_right = upper_right
            self.lower_left = lower_left
            self.lower_right = lower_right
        else:
            self.upper_left = False
            self.upper_right = False
            self.lower_left = False
            self.lower_right = False

        self.neighbour_boolean = [self.upper_left, self.left, self.lower_left,
                                  self.above, self.below, self.upper_right,
                                  self.right, self.lower_right]


    def next_step(self):
        self.neighbours_vector = self.neighbours_transformation_matrix.dot(self.grid_vector)
        usefull_indices = np.union1d(self.neighbours_vector.nonzero()[0], self.grid_vector.nonzero()[0])
        for index in usefull_indices:
            # print(index, self.grid_vector[index], self.neighbours_vector[index])
            if self.grid_vector[index] == 1:
                if not (self.neighbours_cell_alive[0] <= self.neighbours_vector[index] <= self.neighbours_cell_alive[1]):
                    self.grid_vector[index] = 0
                    # print('dead')
            else:
                if (self.neighbours_cell_dead[0] <= self.neighbours_vector[index] <= self.neighbours_cell_dead[1]):
                    self.grid_vector[index] = 1
                    # print('alive')
        self.counter += 1

    def get_neighbours_vector(self):
        return self.neighbours_transformation_matrix.dot(self.grid_vector)

    def createGrid(self, cell_size=5, color_square=0, color_background=255,
                   color_gridlines=128, show_gridlines=False, margins=[0,0], cell_margin=0):
        #set margin if show_gridlines is true, than add 1

        if show_gridlines:
            margins = [margins[0]+1,margins[1]+1]
            cell_margin += 1
        total_cell_size = cell_size + cell_margin
        size_vertical = total_cell_size * self.n + margins[0]
        size_horizontal = total_cell_size * self.m +margins[1]
        image = Image.new(mode='L', size=(size_horizontal, size_vertical), color=color_background)
        draw = ImageDraw.Draw(image)

        filled = self.grid_vector.nonzero()[0]
        for index in filled:
            row = math.floor(index/self.m)
            column = index%self.m
            x_left_corner = margins[1] + column * total_cell_size
            y_left_corner = margins[0] + row * total_cell_size
            draw.rectangle([x_left_corner, y_left_corner,
                            x_left_corner + cell_size-1,y_left_corner + cell_size-1],
                           fill=color_square)


        #Draw gridlines


        if show_gridlines:
            #Horizontal lines
            for i in range(self.m + 1):
                draw.line(
                    ((0, total_cell_size * i),(size_horizontal,total_cell_size * i)),
                     fill=color_gridlines)


            #Vertical lines
            for i in range(self.n+1):
                draw.line(
                    ((total_cell_size * i, 0),(total_cell_size *i, size_horizontal)),
                    fill=color_gridlines)

        return image

    def return_to_initial_state(self):
        self.grid_vector = np.copy(self.start_vector)


# n = 150
# m = 200
# test_matrix = np.random.randint(2, size=(n, m), dtype=np.int8)

# test_class_lifegame = LifeGame(test_matrix,edges_connect=True, neighbours_cell_dead=[3,4])

# time for 150 by 200 matrix:
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


