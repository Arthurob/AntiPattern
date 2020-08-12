# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 00:53:10 2020

@author: Arthur
"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import numpy as np
import time
import antipattern as ap
import life_game as lgm
from datetime import datetime
import os


class App():


    def __init__(self):
        self.start()
        #self.running = True

    def start(self):
        self.root = tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.minsize(width=str(self.width), height=str(self.height))
        # self.minsize(1000,800)
        # self.root.geometry("1150x800")
        # self.root.attributes('-fullscreen', True)
        self.delay = tk.DoubleVar()
        self.delay.set(.05)
        self.init_UI()

        self.stop = False
        self.running = False
        self.step = 0
        self.lifegame_initizalized = False
        self.loop()
        self.root.mainloop()


    def pressed_n(self, button):

        # buttons_to_relief = [self.button_nis2, self.button_nis3, self.button_nis4]
        button_text = button.config('text')[-1]
        if button_text == "2":
            self.n = 2
            buttons_to_relief = [self.button_nis3, self.button_nis4]
            self.button_nis2.configure(relief=tk.SUNKEN)

        elif button_text == "3":
            self.n = 3
            buttons_to_relief = [self.button_nis2, self.button_nis4]
            self.button_nis3.configure(relief=tk.SUNKEN)

        elif button_text == "4":
            self.n = 4
            buttons_to_relief = [self.button_nis2, self.button_nis3]
            self.button_nis4.configure(relief=tk.SUNKEN)

        for button in buttons_to_relief:
            button.configure(relief=tk.RAISED)


        print(self.n)


    def pressed_neigbour(self, button_text):
        if self.dict_active[button_text]:
            self.dict_buttons[button_text].configure(relief=tk.RAISED)
            self.dict_active[button_text] = False
        else:
            self.dict_buttons[button_text].configure(relief=tk.SUNKEN)
            self.dict_active[button_text] = True
        self.lifegame.set_neighbours(self.dict_active)

    def pressed_shuffle(self):
        if self.shuffle:
            self.button_shuffle.configure(relief=tk.RAISED)
            self.shuffle = False
            
        else:
            self.button_shuffle.configure(relief=tk.SUNKEN)
            self.shuffle = True
        


    def init_UI(self):
        # Animation frames
        print(self.width, self.height)
        self.frame_animation = tk.Frame(self.root, width=(self.width-100), height=self.height)
        self.frame_animation.grid(row=0, column=0, sticky='nw')
        self.root.grid_columnconfigure(0, weight = 1)
        # canvas
        self.canvas_width = self.width-100
        self.canvas = tk.Canvas(self.frame_animation, width=self.canvas_width, height=self.height, bg="gray")
        self.canvas.grid(column=0, row=0)

        # controls frame
        self.frame_controls = tk.Frame(self.root, width=100, height=self.height)
        self.frame_controls.grid(row=0, column=1, sticky='nw')
        # play
        self.play = tk.Button(self.frame_controls, text="play", command=self.do_play)
        self.play.grid(column=0, row=0, sticky='w')
        # Pause
        self.pause = tk.Button(self.frame_controls, text="pause", command=self.do_pause)
        self.pause.grid(column=1, row=0, sticky='w')
        # Speed
        self.delay_slider = tk.Scale(
            self.frame_controls, from_=0, to=.75, resolution=.01, orient=tk.HORIZONTAL, variable=self.delay)
        self.delay_slider.grid(column=3, row=0, sticky='w')
        # n
        self.lbl_n = tk.Label(self.frame_controls, text="n = ")
        self.lbl_n.grid(column=0, row=4, sticky='e')

        self.button_nis2 = tk.Button(self.frame_controls, text="2")
        self.button_nis2.configure(command=lambda button = self.button_nis2: self.pressed_n(button))
        self.button_nis2.grid(column=2, row=4, sticky='w')

        self.button_nis3 = tk.Button(self.frame_controls, text="3")
        self.button_nis3.configure(command=lambda button = self.button_nis3: self.pressed_n(button))
        self.button_nis3.grid(column=3, row=4, sticky='w')

        self.button_nis4 = tk.Button(self.frame_controls, text="4")
        self.button_nis4.configure(command=lambda button = self.button_nis4: self.pressed_n(button))
        self.button_nis4.grid(column=4, row=4, sticky='w')

        # n_patterns_power_horizontal
        self.lbl_n_patterns_power_horizontal = tk.Label(self.frame_controls, text="n powers horizontal = ")
        self.lbl_n_patterns_power_horizontal.grid(column=1, row=5, sticky='w')
        self.txt_n_patterns_power_horizontal = tk.Entry(self.frame_controls, width=5)
        self.txt_n_patterns_power_horizontal.grid(column=2, row=5, sticky='w')

        # rows
        self.lbl_rows = tk.Label(self.frame_controls, text="rows = ")
        self.lbl_rows.grid(column=1, row=6, sticky='w')
        self.txt_rows = tk.Entry(self.frame_controls, width=5)
        self.txt_rows.grid(column=2, row=6, sticky='w')
        # Columns
        self.lbl_columns = tk.Label(self.frame_controls,text="columns = ")
        self.lbl_columns.grid(column=1, row=7, sticky='w')
        self.txt_columns = tk.Entry(self.frame_controls, width=5)
        self.txt_columns.grid(column=2, row=7, sticky='w')

        # margin
        self.lbl_cell_margin = tk.Label(self.frame_controls,text="cell margin = ")
        self.lbl_cell_margin.grid(column=1, row=8, sticky='w')
        self.txt_cell_margin = tk.Entry(self.frame_controls, width=5)
        self.txt_cell_margin.grid(column=2, row=8, sticky='w')

        # cell  size
        self.lbl_cell_size = tk.Label(self.frame_controls,text="cell size = ")
        self.lbl_cell_size.grid(column=1, row=9, sticky='w')
        self.txt_cell_size = tk.Entry(self.frame_controls, width=5)
        self.txt_cell_size.grid(column=2, row=9, sticky='w')

        # neighbours_cell_alive
        self.lbl_neighbours_cell_alive = tk.Label(self.frame_controls,text="neighbours cell alive = ")
        self.lbl_neighbours_cell_alive.grid(column=1, row=10, sticky='w')
        self.txt_neighbours_cell_alive_min = tk.Entry(self.frame_controls, width=5)
        self.txt_neighbours_cell_alive_min.grid(column=2, row=10, sticky='w')
        self.txt_neighbours_cell_alive_max = tk.Entry(self.frame_controls, width=5)
        self.txt_neighbours_cell_alive_max.grid(column=3, row=10, sticky='w')

        # neighbours_cell_dead
        self.lbl_neighbours_cell_dead = tk.Label(self.frame_controls,text="neighbours cell dead = ")
        self.lbl_neighbours_cell_dead.grid(column=1, row=11, sticky='w')
        self.txt_neighbours_cell_dead_min = tk.Entry(self.frame_controls, width=5)
        self.txt_neighbours_cell_dead_min.grid(column=2, row=11, sticky='w')
        self.txt_neighbours_cell_dead_max = tk.Entry(self.frame_controls, width=5)
        self.txt_neighbours_cell_dead_max.grid(column=3, row=11, sticky='w')

        # Neighbours contributing to # of neigbouring cells

        #upper left
        self.button_upper_left = tk.Button(self.frame_controls, text="upper_left")
        self.button_upper_left.configure(command=lambda button = self.button_upper_left: self.pressed_neigbour("upper_left"))
        self.button_upper_left.grid(column=1, row=12, sticky='w')
        self.button_upper_left.configure(relief=tk.SUNKEN)

        self.button_above = tk.Button(self.frame_controls, text="above")
        self.button_above.configure(command=lambda button = self.button_above: self.pressed_neigbour("above"))
        self.button_above.grid(column=2, row=12, sticky='w')
        self.button_above.configure(relief=tk.SUNKEN)

        self.button_upper_right = tk.Button(self.frame_controls, text="upper_right")
        self.button_upper_right.configure(command=lambda button = self.button_upper_right: self.pressed_neigbour("upper_right"))
        self.button_upper_right.grid(column=3, row=12, sticky='w')
        self.button_upper_right.configure(relief=tk.SUNKEN)

        self.button_right = tk.Button(self.frame_controls, text="right")
        self.button_right.configure(command=lambda button = self.button_right: self.pressed_neigbour("right"))
        self.button_right.grid(column=3, row=13, sticky='w')
        self.button_right.configure(relief=tk.SUNKEN)

        self.button_lower_right = tk.Button(self.frame_controls, text="lower_right")
        self.button_lower_right.configure(command=lambda button = self.button_lower_right: self.pressed_neigbour("lower_right"))
        self.button_lower_right.grid(column=3, row=14, sticky='w')
        self.button_lower_right.configure(relief=tk.SUNKEN)

        self.button_below = tk.Button(self.frame_controls, text="below")
        self.button_below.configure(command=lambda button = self.button_below: self.pressed_neigbour("below"))
        self.button_below.grid(column=2, row=14, sticky='w')
        self.button_below.configure(relief=tk.SUNKEN)

        self.button_lower_left = tk.Button(self.frame_controls, text="lower_left")
        self.button_lower_left.configure(command=lambda button = self.button_lower_left: self.pressed_neigbour("lower_left"))
        self.button_lower_left.grid(column=1, row=14, sticky='w')
        self.button_lower_left.configure(relief=tk.SUNKEN)

        self.button_left = tk.Button(self.frame_controls, text="left")
        self.button_left.configure(command=lambda button = self.button_left: self.pressed_neigbour("left"))
        self.button_left.grid(column=1, row=13, sticky='w')
        self.button_left.configure(relief=tk.SUNKEN)


        self.dict_buttons = {"upper_left": self.button_upper_left, "above": self.button_above,"upper_right": self.button_upper_right,
                        "right": self.button_right, "lower_right": self.button_lower_right, "below": self.button_below,
                        "lower_left": self.button_lower_left, "left": self.button_left}

        self.dict_active = {"upper_left": True, "above": True,"upper_right": True,
                        "right": True, "lower_right": True, "below": True,
                        "lower_left": True, "left": True}

        # edges connect
        self.button_edges_connect = tk.Button(self.frame_controls, text="edges connect")
        self.button_edges_connect.configure(command=self.pressed_edges_connect)
        self.button_edges_connect.configure(relief=tk.RAISED)
        self.button_edges_connect.grid(column=1, row=15, sticky='w')
        self.edges_connect = False

        # init antipattern
        self.init_lifegame = tk.Button(self.frame_controls, text="initialize lifegame", command=self.init_lifegame)
        self.init_lifegame.grid(column=1, row=16, sticky='w')
        
        # Shuffle
        self.shuffle = False
        self.button_shuffle = tk.Button(self.frame_controls, text="shuffle")
        self.button_shuffle.configure(command=self.pressed_shuffle)
        self.button_shuffle.configure(relief=tk.RAISED)
        self.button_shuffle.grid(column=1, row=20, sticky='w')
        
        # save
        self.button_save = tk.Button(self.frame_controls, text="save")
        self.button_save.configure(command=self.save_image)
        self.button_save.grid(column=1, row=21, sticky='w')

    def pressed_edges_connect(self):
        if self.lifegame.edges_connect:
            self.button_edges_connect.configure(relief=tk.RAISED)
            self.edges_connect = False
            
        else:
            self.button_edges_connect.configure(relief=tk.SUNKEN)
            self.edges_connect = True
        self.lifegame.edges_connect = self.edges_connect

    def read_values(self):
        # columns
        columns = self.txt_columns.get()
        if columns != '':
            self.columns = int(columns)
        else:
            self.columns = 0

        # rows
        rows = self.txt_rows.get()
        if rows != '':
            self.rows = int(rows)
        else:
            self.rows = 0

        neighbours_cell_alive_min = self.txt_neighbours_cell_alive_min.get()
        neighbours_cell_alive_max = self.txt_neighbours_cell_alive_max.get()
        if (neighbours_cell_alive_min != '') and (neighbours_cell_alive_max != ''):
            self.neighbours_cell_alive = list( range(int(neighbours_cell_alive_min), int(neighbours_cell_alive_max)+1))
        else:
            self.neighbours_cell_alive = [3, 4]

        neighbours_cell_dead_min = self.txt_neighbours_cell_dead_min.get()
        neighbours_cell_dead_max = self.txt_neighbours_cell_dead_max.get()
        if (neighbours_cell_dead_min != '') and (neighbours_cell_dead_max != ''):
            self.neighbours_cell_dead = list( range(int(neighbours_cell_dead_min), int(neighbours_cell_dead_max)+1))
        else:
            self.neighbours_cell_dead = [3, 3]



        self.n_patterns_power_horizontal = int(self.txt_n_patterns_power_horizontal.get())

        cell_size = self.txt_cell_size.get()
        if cell_size != '':
            self.cell_size = int(cell_size)
        else:
            self.cell_size = 4

        cell_margin = self.txt_cell_margin.get()
        if cell_margin != '':
            self.cell_margin = int(cell_margin)
        else:
            self.cell_margin = 0

    def init_lifegame(self):
        self.read_values()
        anti_pattern = ap.AntiPattern(self.n)
        print(self.shuffle)
        smallMatrix = anti_pattern.createMatrix(
            n_patterns_power_horizontal = self.n_patterns_power_horizontal, shuffle  =  self.shuffle)
        # smallMatrix = [[]]
        smallArray = np.array(smallMatrix)
        if (self.columns == 0) or (self.rows == 0):
            desired_dimension = smallArray.shape
        else:
            desired_dimension = [self.rows, self.columns]
        lambda_x = math.ceil((desired_dimension[0]-smallArray.shape[0])/2)
        lambda_y = math.ceil((desired_dimension[1]-smallArray.shape[1])/2)
        bigArray = np.pad(
            smallArray, ((lambda_x,desired_dimension[0]-lambda_x-smallArray.shape[0]),
            (lambda_y,desired_dimension[1]-lambda_y-smallArray.shape[1])),'constant')
        print(bigArray.shape)

        self.lifegame = lgm.LifeGame(
            bigArray, neighbours_cell_alive=self.neighbours_cell_alive,
            neighbours_cell_dead=self.neighbours_cell_dead, neighbours_dict=self.dict_active,
            edges_connect=self.edges_connect)
        print("finnished lifegame")
        self.image = self.lifegame.createGrid(cell_size=self.cell_size, cell_margin=self.cell_margin)
        width = self.cell_size * bigArray.shape[1] + 2
        height = self.cell_size * bigArray.shape[0] + 2
        print(height, width )
        self.create_image()
        self.image_on_canvas = self.canvas.create_image(int(self.canvas_width/2), int(self.height/2), image=self.imageTK, anchor=tk.CENTER)
        self.stop = False
        # self.loop()


    def create_image(self):
        self.image = self.lifegame.createGrid(cell_size=self.cell_size, cell_margin=self.cell_margin)
        self.imageTK = ImageTk.PhotoImage(image=self.image)

    def loop(self):
        while True:
            # time.sleep(.5)
            if self.stop:
                print("stopped")
                break

            self.status = "continue_while_loop"
            while self.status == "continue_while_loop":
                self.status = "enter_for_loop_again"
                self.pause.update()
                self.play.update()
                if self.running:
                    self.next_step()
                    time.sleep(self.delay_slider.get())
                else:
                    self.status = "enter_for_loop_again"


    def do_stop(self):
        self.stop = True

    def save_image(self):
        image_to_save = self.lifegame.createGrid(cell_size=1)
        path = r'D:\My documents\Python\images'
        image_name = f'n={self.n}_n_hori={self.n_patterns_power_horizontal}_{datetime.now():%Y_%m_%d_%H_%M_%S.%f}.bmp'
        image_to_save.save(os.path.join(path,image_name))
        

    def next_step(self):
        self.lifegame.next_step()
        self.create_image()
        self.canvas.itemconfig(self.image_on_canvas, image=self.imageTK)
        self.root.update_idletasks()
        self.step += 1

    def do_pause(self):
        self.running = False
        # global running
        # running = False

    def do_play(self):
        self.running = True
        self.stop = False

app = App()

# Interesting settings:
    # n=3, hori=3, allice= 3 - 5, dead = 3-3
    # n = 2, n_hori = 1, rows = 140, columns = 40 neigbeours alive = 3,4 dead = 2,3
    # Switch off above, upper_right, rigt, lower_right
    #Kind off a wave: n = 3, powers hori = 3, alive = 4-6, dead = 3-5, edges connect, play for a while and turn off above and upper_right

# print('Now we can continue running code while mainloop runs!')


# for i in range(10):
#     print("hallo")
#     time.sleep(5)

# for i in range(100000):
#     print(i)
