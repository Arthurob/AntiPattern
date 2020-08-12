# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:39:49 2020

@author: Arthur
"""
import itertools
import math
# import os
# from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont
# from random import shuffle

class AntiPattern:
    """Create the anti  pattern class."""


    # mark up paramaters
    show_gridlines = False
    margin = 0
    color_background = 255
    color_square = 0
    color_gridlines = 128
    font_color = 255

    def __init__(self, n):
        self.n = n
        self.combinatorist = []
        for i in range(0, n*n+1):
            self.combinatorist.append(list(itertools.combinations(range(0, n*n), i)))
        self.combis = [y for x in self.combinatorist for y in x]
        self.n_patterns_horizontal = 0
        self.n_patterns_vertical = 0
        self.n_shafts = 0
        self.n_rows = 0
        self.set_markup()

        # mark up paramaters
        #  self.show_gridlines = False
        #  self.margin = 0
        #  self.color_background = 255
        #  self.color_square = 0
        #  self.color_gridlines = 128
        #  self.font_color = 255

    def set_markup(self, show_gridlines=False, margin=0,color_background=255,
                   color_square=0, color_gridlines=128, font_color=255):

        """Set the markup parameters"""

        self.show_gridlines = show_gridlines
        self.margin = margin
        self.color_background = color_background
        self.color_square = color_square
        self.color_gridlines = color_gridlines
        self.font_color = font_color

    def set_parameters(self, n_patterns_power_horizontal):

        """Calculate the parametsr of the grid"""

        self.n_patterns_horizontal = 2**n_patterns_power_horizontal
        n_patterns_power_vertical = self.n**2 - n_patterns_power_horizontal
        self.n_patterns_vertical = 2**n_patterns_power_vertical
        self.n_shafts = self.n * self.n_patterns_horizontal
        self.n_rows = self.n * self.n_patterns_vertical

    def create_grid(self, n_patterns_power_horizontal, cell_size=5,
                    shuffle=False, display_numerics=False):

        """Create the grid"""

        self.set_parameters(n_patterns_power_horizontal)
        # Calculate some number values of the weave
        print(f'number of shafts:{self.n_shafts}')
        print(self.n_rows)

        # Restructere list
        if shuffle:
            random.shuffle(self.combis)

        combis = [self.combis[i:i + self.n_patterns_horizontal]
                  for i in range(0, len(self.combis), self.n_patterns_horizontal)]
        # Fix tuples have only 1 element
        list(map(lambda x: (x,) if isinstance(x, int) else x, combis))

        # set margin if self.show_gridlines is true, than add 1
        if self.show_gridlines:
            self.margin += 1

        # Set pixel size to fit nicely qith square while reatining to approximate container_n_pixels

        size_horizontal = cell_size * self.n_shafts + self.margin
        size_vertical = cell_size * self.n_rows + self.margin
        print(f'image width in pixels:{size_horizontal}')
        print(f'image height in pixels:{size_vertical}')
        image = Image.new(mode='L', size=(size_horizontal, size_vertical),
                          color=self.color_background)
        draw = ImageDraw.Draw(image)

        # Define text type
        if display_numerics:
            unicode_font = ImageFont.truetype("DejaVuSans.ttf", math.ceil(cell_size/2))
            margin_text = math.floor(cell_size/4)

        # Fill cells
        for indx_row, row_patterns in enumerate(combis):
            for  indx_column, column_patterns in enumerate(row_patterns):
                for pos in enumerate(column_patterns):
                    column = (pos[1] % self.n + indx_column*self.n)
                    row = (math.floor(pos[1] / self.n) + indx_row*self.n)
                    x_left_corner = column * cell_size
                    y_left_corner = row * cell_size
                    if self.color_square != 0:
                        print('wtf')
                    draw.rectangle([x_left_corner, y_left_corner,
                                    x_left_corner + cell_size - 1,
                                    y_left_corner + cell_size - 1],
                                   fill=self.color_square)

                    if display_numerics:
                        draw.text((x_left_corner + margin_text,
                                   y_left_corner + margin_text),
                                  str(column+1), font=unicode_font,
                                  fill=self.font_color)

        if self.show_gridlines:
            self.draw_gridlines(draw, cell_size, self.n_rows, self.n_shafts,
                                size_horizontal,size_vertical)

        return image

    def draw_gridlines(self, draw, cell_size, n_rows, n_shafts,
                       size_horizontal, size_vertical):
        """Draw the gridlines."""
        # Horizontal lines
        for i in range(0, (n_rows + 1)*self.n):
            draw.line(((0, cell_size * i), (size_horizontal, cell_size * i)),
                      fill=self.color_gridlines)

        # Vertical lines
        for i in range(0, (n_shafts+1)*self.n):
            draw.line(((cell_size *i, 0), (cell_size *i, size_vertical)),
                      fill=self.color_gridlines)

    def createMatrix(self, n_patterns_power_horizontal, shuffle=False):
        self.set_parameters(n_patterns_power_horizontal)
        matrix = [[0 for j in range(self.n_shafts)] for  i in range(self.n_rows)]
        # print(f'number of shafts:{n_shafts}')
        # print(n_rows)
        if shuffle:
            random.shuffle(self.combis)
        combis = [self.combis[i:i + self.n_patterns_horizontal]
                  for i in range(0, len(self.combis), self.n_patterns_horizontal)]
        # Fix tuples have only 1 element
        list(map(lambda x: (x,) if isinstance(x, int) else x, combis))
        # Fix tuples have only 1 element
        # list(map(lambda x: (x,) if type(x) == int else x,self.combis))


        for indx_row, row_patterns in enumerate(combis):
            for  indx_column, column_patterns in enumerate(row_patterns):
                for pos in enumerate(column_patterns):
                    column = (pos[1] % self.n + indx_column*self.n)
                    row = (math.floor(pos[1] / self.n) + indx_row*self.n)
                    matrix[row][column] = 1


        return matrix



# AP2 = AntiPattern(2)
# testImage2 = AP2.create_grid(n_patterns_power_horizontal=2, cell_size=15,
#                              display_numerics=False)
# AP2.combis

# AP3 = AntiPattern(3)
# testImage3 = AP3.create_grid(n_patterns_power_horizontal=4, cell_size=1,
#                               display_numerics=False)
# testImage3_shuffle = AP3.create_grid(n_patterns_power_horizontal=4, cell_size=1,
#                                       display_numerics=False, shuffle=True)



# # AP4 = AntiPattern(4)
# # testImage4 = AP4.create_grid(6,1)

# testImage2.show()
# test_matrix = AP2.createMatrix(n_patterns_power_horizontal=2)
