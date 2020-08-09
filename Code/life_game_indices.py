# -*- coding: utf-8 -*.
"""
Created on Tue May 19 22:17:58 2020

@author: Arthur
"""
from PIL import Image, ImageDraw
import math
import numpy as np

class LifeGame:

    def __init__(self, start_matrix, edges_connect=False,
                 include_corners=True, neighbours_cell_alive=[3, 4],
                 neighbours_cell_dead=[3, 3],
                 neighbours_dict = {"upper_left": True, "above": True,"upper_right": True,
                        "right": True, "lower_right": True, "below": True,
                        "lower_left": True, "left": True}):
        self.counter = 0
        self.start_matrix = start_matrix
        self.rows = start_matrix.shape[0]
        self.columns = start_matrix.shape[1]
        self.grid_matrix = np.copy(self.start_matrix)
        self.edges_connect = edges_connect
        self.include_corners= include_corners
        self.neighbours_cell_alive = neighbours_cell_alive
        self.neighbours_cell_dead = neighbours_cell_dead
        self.set_neighbours(neighbours_dict)

    def set_neigbours_indices(self):
        self.alive_indices = self.grid_matrix.nonzero()
        self.neighbour_indices_alive = []
        self.neighbour_indices_dead = []
        # loop through alive cells
        for index_alive in self.alive_indices:
            indices_neighbours = self.get_neighbours_indices(index_alive)
            # loop through neigbouring cells
            for index_neighbour in indices_neighbours:
                # check if the neighbouring cell is also alive
                if index_neighbour in self.alive_indices:
                    if index_neighbour in self.neighbour_indices_alive[:,0]:
                        index = self.neighbour_indices_alive[:,0](index)
                        self.neighbour_indices_alive[index,1] += 1
                    else:
                        self.neighbour_indices_alive.append([[index_neighbour,0]])
                else:
                    if index_neighbour in self.neighbour_indices_dead[:,0]:
                        index = self.neighbour_indices_dead[:,0](index)
                        self.neighbour_indices_dead[index,1] += 1
                    else:
                        self.neighbour_indices_dead.append([[index_neighbour,0]])

    def get_neighbours_indices(self, index):
        self.
        row = index[0]
        column = index[1]
        row_above = row-1
        row_below = row+1
        column_left = column - 1
        column_right = column + 1
        indices = []
        if self.edges_connect:
            row_above = row_above%self.rows
            row_below = row_below%self.rows
            column_left = column_left%self.columns
            column_right = column_right%self.columns
              # above
        if self.dict_neighbour_active["above"] & (row_above >= 0):
            indices.append([row_above,column])
        #below
        if self.dict_neighbour_active["below"] & (row_below <  self.rows):
            indices.append([row_below,column])
        #left
        if self.dict_neighbour_active["left"] & (column_left >= 0):
            indices.append([row,column_left])
        #right
        if self.dict_neighbour_active["right"] & (column_right < self.columns):
            indices.append([row,column_right])

        if self.include_corners:
            #left upper corner
            if self.dict_neighbour_active["upper_left"] & (row_above >= 0) & (column_left >= 0):
                indices.append([row_above,column_left])
            #left lower corner
            if self.dict_neighbour_active["lower_left"] & (row_below < self.rows) & (column_left >= 0):
                indices.append([row_below,column_left])
            #right upper corner
            if self.dict_neighbour_active["upper_right"] & (row_above >= 0) & (column_right < self.columns):
                indices.append([row_above,column_right])
            #right lower corner
            if self.dict_neighbour_active["lower_right"] & (row_below < self.rows) & (column_right < self.columns):
                indices.append([row_below,column_right])
        
        return indices

    def add_delete_neighbour(self, index, create_kill):

        """ In this function neighbours are added or deleted depending on creation
        or destruction of life with an index, the neigbours are relative to that
        the cell that is created/destroyed and so directions flip. So if the
        neighbour is upper left, the right lower index is used"""
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

        #below
        if below & (row_above >= 0):
            neighbours[row_above][column] += create_kill
        #above
        if above & (row_below <  rows):
            neighbours[row_below][column] += create_kill
        #right
        if right & (column_left >= 0):
            neighbours[row][column_left] += create_kill
        #left
        if left & (column_right < columns):
            neighbours[row][column_right] += create_kill

        if include_corners:
            #right lower corner
            if lower_right & (row_above >= 0)  & (column_left >= 0):
                neighbours[row_above][column_left] += create_kill
            #right upper corner
            if upper_right & (row_below <  rows) & (column_left >= 0):
                neighbours[row_below][column_left] += create_kill
            #left lower corner
            if lower_left & (row_above >= 0) & (column_right < columns):
                neighbours[row_above][column_right] += create_kill
            #left upper corner
            if upper_left & (row_below < rows) & (column_right < columns):
                neighbours[row_below][column_right] += create_kill


    def set_neighbours(self, neighbours_dict):
        self.dict_neighbour_active = {"upper_left": True, "above": True,"upper_right": True,
                        "right": True, "lower_right": True, "below": True,
                        "lower_left": True, "left": True}

        for pair in neighbours_dict:
            self.dict_neighbour_active[pair] = neighbours_dict[pair]



    def next_step(self):
        self.rowseighbours_vector = self.rowseighbours_transformation_matrix.dot(self.grid_vector)
        usefull_indices = np.union1d(self.rowseighbours_vector.nonzero()[0], self.grid_vector.nonzero()[0])
        for index in usefull_indices:
            # print(index, self.grid_vector[index], self.rowseighbours_vector[index])
            if self.grid_vector[index] == 1:
                if not (self.rowseighbours_cell_alive[0] <= self.rowseighbours_vector[index] <= self.rowseighbours_cell_alive[1]):
                    self.grid_vector[index] = 0
                    # print('dead')
            else:
                if (self.rowseighbours_cell_dead[0] <= self.rowseighbours_vector[index] <= self.rowseighbours_cell_dead[1]):
                    self.grid_vector[index] = 1
                    # print('alive')
        self.counter += 1

    def get_neighbours_vector(self):
        return self.rowseighbours_transformation_matrix.dot(self.grid_vector)

    def createGrid(self, cell_size=5, color_square=0, color_background=255,
                   color_gridlines=128, show_gridlines=False):
        #set margin if show_gridlines is true, than add 1
        size_vertical = cell_size * self.rows
        size_horizontal = cell_size * self.columns
        image = Image.new(mode='L', size=(size_horizontal, size_vertical), color=color_background)
        draw = ImageDraw.Draw(image)

        for index in self.alive_indices:
            row = math.floor(index/self.columns)
            column = index%self.columns
            x_left_corner = column * cell_size
            y_left_corner = row * cell_size
            draw.rectangle([x_left_corner, y_left_corner,
                            x_left_corner + cell_size-1,y_left_corner + cell_size-1],
                           fill=color_square)


        #Draw gridlines


        if show_gridlines:
            #Horizontal lines
            for i in range(m+1):
                draw.line( ( (0, cell_size *i  ),
                            (size_horizontal,cell_size *i ) ) , fill=color_gridlines)

            #Vertical lines
            for i in range(n+1):
                draw.line( ( ( cell_size *i, 0),
                            (cell_size *i, size_horizontal) ) , fill=color_gridlines)

        return image

    def return_to_initial_state(self):
        self.grid_vector = np.copy(self.start_vector)





