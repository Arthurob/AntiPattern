# -*- coding: utf-8 -*.
"""
Created on Tue May 19 22:17:58 2020

@author: Arthur
"""
from PIL import Image, ImageDraw
import math
import numpy as np
import scipy.sparse as sparse

class LifeGame:

    def __init__(self, start_matrix, above=True, below=True, left=True,
                 right=True,upper_left=True, upper_right=True,
                 lower_left=True, lower_right=True, edges_connect=False,
                 include_corners=True, neighbours_cell_alive=[3, 4],
                 neighbours_cell_dead=[3, 3], method = "normal"):
        self.method = method
        self.counter = 0
        self.start_matrix = start_matrix
        self.matrix = np.copy(self.start_matrix)
        self.n = start_matrix.shape[0]
        self.m = start_matrix.shape[1]
        self.edges_connect = edges_connect
        self.include_corners= include_corners
        self.set_neighbours_booleans(
            above, below, left,right,upper_left, upper_right,lower_left,
            lower_right,include_corners)

        self.neighbours_cell_alive = neighbours_cell_alive
        self.neighbours_cell_dead = neighbours_cell_dead

        if self.method == "matrix":
            self.matrix()

    def matrix(self):
        self.start_vector = self.start_matrix.flatten()
        self.grid_vector = np.copy(self.start_vector)
        self.size = self.n * self.m
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

    def set_neigbours_dict(self, neighbours_dict):
        for pair in neighbours_dict:
            self.dict_neighbour_active[pair] = neighbours_dict[pair]



    def set_neighbours_booleans(self,above=True, below=True, left=True,
                 right=True,upper_left=True, upper_right=True,
                 lower_left=True, lower_right=True, include_corners=True):
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

        self.dict_neighbour_active = {"upper_left": upper_left, "above": above,"upper_right": upper_right,
                        "right": right, "lower_right": lower_right, "below": below,
                        "lower_left": lower_left, "left": left}

    def create_neighbours_matrix(self):
        rows = self.n
        columns = self.m
        self.neighbours = np.zeros_like(self.matrix)
        for index, value in np.ndenumerate(self.neighbours):
            row = index[0]
            column = index[1]
            row_above = row-1
            row_below = row+1
            column_left = column - 1
            column_right = column + 1
            if self.edges_connect:
                row_above = row_above%rows
                row_below = row_below%rows
                column_left = column_left%columns
                column_right = column_right%columns

            # above
            if self.above & (row_above >= 0):
                self.neighbours[index] += self.matrix[row_above][column]
            #below
            if self.below & (row_below <  rows):
                self.neighbours[index] += self.matrix[row_below][column]
            #left
            if self.left & (column_left >= 0):
                self.neighbours[index] += self.matrix[row][column_left]
            #right
            if self.right & (column_right < columns):
                self.neighbours[index] += self.matrix[row][column_right]

            if self.include_corners:
                #left upper corner
                if self.upper_left & (row_above >= 0)  & (column_left >= 0):
                    self.neighbours[index] += self.matrix[row_above][column_left]
                #left lower corner
                if self.lower_left & (row_below <  rows) & (column_left >= 0):
                    self.neighbours[index] += self.matrix[row_below][column_left]
                #right upper corner
                if self.upper_right & (row_above >= 0)  & (column_right < columns):
                    self.neighbours[index] += self.matrix[row_above][column_right]
                #right lower corner
                if self.lower_right & (row_below <  rows) & (column_right < columns):
                    self.neighbours[index] += self.matrix[row_below][column_right]



    def next_step(self):
        if self.method == "normal":
            self.next_step_normal()
        elif self.method == "matrix":
            self.next_step_matrix()

    def next_step_normal(self):
        self.create_neighbours_matrix()
        for index, state in np.ndenumerate(self.matrix):
            #If the cell is alive and there are too many or too few neigbours it dies
            if (state == 1) & (not self.neighbours[index] in self.neighbours_cell_alive):
                self.matrix[index] = 0
            #If the cell is dead and it has enough living neigbours it will live
            elif (state == 0) & (self.neighbours[index] in self.neighbours_cell_dead):
                #print('new live: ',index)
               self. matrix[index] = 1
            #In all other cases, nothing changes, the cell remains dead or alive



    def next_step_matrix(self):
        self.neighbours_vector = self.neighbours_transformation_matrix.dot(self.grid_vector)
        usefull_indices = np.union1d(self.neighbours_vector.nonzero()[0], self.grid_vector.nonzero()[0])
        for index in usefull_indices:
            # print(index, self.grid_vector[index], self.neighbours_vector[index])
            if self.grid_vector[index] == 1:
                if not (self.neighbours_vector[index] in self.neighbours_cell_alive):
                    self.grid_vector[index] = 0
                    # print('dead')
            else:
                if (self.neighbours_vector[index] in self.neighbours_cell_dead):
                    self.grid_vector[index] = 1
                    # print('alive')
        self.counter += 1

    def get_neighbours_vector(self):
        return self.neighbours_transformation_matrix.dot(self.grid_vector)

    def createGrid(self, cell_size=5, color_square=0, color_background=255,
                   color_gridlines=128, show_gridlines=False, margins=[0,0], cell_margin=0):
        if self.method == "normal":
            self.createGrid_normal(cell_size, color_square, color_background,
                   color_gridlines, show_gridlines, margins, cell_margin)
        else:
            self.createGrid_matrix(cell_size, color_square, color_background,
                   color_gridlines, show_gridlines, margins, cell_margin)

    def createGrid_normal(self, cell_size=5, color_square=0, color_background=255,
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

        filled = self.matrix.nonzero()
        for i in range(len(filled[0])):
            x_left_corner = margins[1] + filled[1][i] * total_cell_size
            y_left_corner = margins[0] + filled[0][i] * total_cell_size
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

    def createGrid_matrix(self, cell_size=5, color_square=0, color_background=255,
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





