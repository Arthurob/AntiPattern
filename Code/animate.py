# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 00:53:10 2020

@author: Arthur
"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import numpy as np
import threading
import time
import antipattern as ap
import life_game_matrix as lgm


class App(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        #self.running = True



    def callback(self):
        self.root.quit()



    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("1150x800+0+0")
        self.init_UI()

        self.stop = False
        self.running = False
        self.step = 0
        self.lifegame_initizalized = False
        self.loop()
        self.root.mainloop()


    def pressed_n(self, button):

        # buttons_to_disable = [self.button_nis2, self.button_nis3, self.button_nis4]
        button_text = button.config('text')[-1]
        if button_text == "2":
            self.n = 2
            buttons_to_disable = [self.button_nis3, self.button_nis4]
            self.button_nis2.configure(relief=tk.SUNKEN)

        elif button_text == "3":
            self.n = 3
            buttons_to_disable = [self.button_nis2, self.button_nis4]
            self.button_nis3.configure(relief=tk.SUNKEN)

        elif button_text == "4":
            self.n = 4
            buttons_to_disable = [self.button_nis2, self.button_nis3]
            self.button_nis4.configure(relief=tk.SUNKEN)

        self.disable_buttons(buttons_to_disable)


        print(self.n)

    def disable_buttons(self, buttons):
        for button in buttons:
            button.configure(relief=tk.RAISED)


    def init_UI(self):
        # canvas
        self.canvas = tk.Canvas(self.root , width=1000, height=700, bg="gray")
        self.canvas.grid(column=0, row=0)
        # play
        self.play = tk.Button(self.root, text="play", command=self.do_play)
        self.play.grid(column=1, row=1, sticky='w')
        # Pause
        self.pause = tk.Button(self.root, text="pause", command=self.do_pause)
        self.pause.grid(column=1, row=2, sticky='w')
        # Stop
        self.stop_button = tk.Button(self.root, text="stop", command=self.do_stop)
        self.stop_button.grid(column=1, row=3, sticky='w')
        # Speed


        # n
        self.lbl_n = tk.Label(self.root, text="n = ")
        self.lbl_n.grid(column=1, row=4, sticky='w')

        self.button_nis2 = tk.Button(self.root, text="2")
        self.button_nis2.configure(command=lambda button = self.button_nis2: self.pressed_n(button))
        self.button_nis2.grid(column=2, row=4, sticky='w')

        self.button_nis3 = tk.Button(self.root, text="3")
        self.button_nis3.configure(command=lambda button = self.button_nis3: self.pressed_n(button))
        self.button_nis3.grid(column=3, row=4, sticky='w')

        self.button_nis4 = tk.Button(self.root, text="4")
        self.button_nis4.configure(command=lambda button = self.button_nis4: self.pressed_n(button))
        self.button_nis4.grid(column=4, row=4, sticky='w')

        # self.txt_n = tk.Entry(self.root, width=5)
        # self.txt_n.grid(column=2, row=4, sticky='w')

        # n_patterns_power_horizontal
        self.lbl_n_patterns_power_horizontal = tk.Label(self.root, text="n powers horizontal = ")
        self.lbl_n_patterns_power_horizontal.grid(column=1, row=5, sticky='w')
        self.txt_n_patterns_power_horizontal = tk.Entry(self.root, width=5)
        self.txt_n_patterns_power_horizontal.grid(column=2, row=5, sticky='w')

        # rows
        self.lbl_rows = tk.Label(self.root, text="rows = ")
        self.lbl_rows.grid(column=1, row=6, sticky='w')
        self.txt_rows = tk.Entry(self.root, width=5)
        self.txt_rows.grid(column=2, row=6, sticky='w')
        # Columns
        self.lbl_columns = tk.Label(self.root,text="columns = ")
        self.lbl_columns.grid(column=1, row=7, sticky='w')
        self.txt_columns = tk.Entry(self.root, width=5)
        self.txt_columns.grid(column=2, row=7, sticky='w')

        # margin
        self.lbl_cell_margin = tk.Label(self.root,text="cell margin = ")
        self.lbl_cell_margin.grid(column=1, row=8, sticky='w')
        self.txt_cell_margin = tk.Entry(self.root, width=5)
        self.txt_cell_margin.grid(column=2, row=8, sticky='w')

        # cell  size
        self.lbl_cell_size = tk.Label(self.root,text="cell size = ")
        self.lbl_cell_size.grid(column=1, row=9, sticky='w')
        self.txt_cell_size = tk.Entry(self.root, width=5)
        self.txt_cell_size.grid(column=2, row=9, sticky='w')

        # neighbours_cell_alive
        self.lbl_neighbours_cell_alive = tk.Label(self.root,text="neighbours cell alive = ")
        self.lbl_neighbours_cell_alive.grid(column=1, row=10, sticky='w')
        self.txt_neighbours_cell_alive_min = tk.Entry(self.root, width=5)
        self.txt_neighbours_cell_alive_min.grid(column=2, row=10, sticky='w')
        self.txt_neighbours_cell_alive_max = tk.Entry(self.root, width=5)
        self.txt_neighbours_cell_alive_max.grid(column=3, row=10, sticky='w')

        # neighbours_cell_dead
        self.lbl_neighbours_cell_dead = tk.Label(self.root,text="neighbours cell dead = ")
        self.lbl_neighbours_cell_dead.grid(column=1, row=11, sticky='w')
        self.txt_neighbours_cell_dead_min = tk.Entry(self.root, width=5)
        self.txt_neighbours_cell_dead_min.grid(column=2, row=11, sticky='w')
        self.txt_neighbours_cell_dead_max = tk.Entry(self.root, width=5)
        self.txt_neighbours_cell_dead_max.grid(column=3, row=11, sticky='w')

        # init antipattern
        self.init_lifegame = tk.Button(self.root, text="initialize lifegame", command=self.init_lifegame)
        self.init_lifegame.grid(column=1, row=13, sticky='w')

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
            self.neighbours_cell_alive = [int(neighbours_cell_alive_min), int(neighbours_cell_alive_max)]
        else:
            self.neighbours_cell_alive = [3, 4]

        neighbours_cell_dead_min = self.txt_neighbours_cell_dead_min.get()
        neighbours_cell_dead_max = self.txt_neighbours_cell_dead_max.get()
        if (neighbours_cell_dead_min != '') and (neighbours_cell_dead_max != ''):
            self.neighbours_cell_dead = [int(neighbours_cell_dead_min), int(neighbours_cell_dead_max)]
        else:
            self.neighbours_cell_dead = [3, 3]



        self.n_patterns_power_horizontal = int(self.txt_n_patterns_power_horizontal.get())

        cell_size = self.txt_cell_size.get()
        if cell_size != '':
            self.cell_size = int(cell_size)
        else:
            self.cell_size = 3

        cell_margin = self.txt_cell_margin.get()
        if cell_margin != '':
            self.cell_margin = int(cell_margin)
        else:
            self.cell_margin = 0

    def init_lifegame(self):
        self.read_values()
        anti_pattern = ap.AntiPattern(self.n)
        smallMatrix = anti_pattern.createMatrix(
            n_patterns_power_horizontal = self.n_patterns_power_horizontal)
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
            bigArray, neighbours_cell_alive=self.neighbours_cell_alive, neighbours_cell_dead=self.neighbours_cell_dead)
        print("finnished lifegame")
        self.image = self.lifegame.createGrid(cell_size=self.cell_size, cell_margin=1)
        width = self.cell_size * bigArray.shape[1] + 2
        height = self.cell_size * bigArray.shape[0] + 2
        print(width, height)
        self.create_image()
        self.image_on_canvas = self.canvas.create_image(2, 2, image=self.imageTK, anchor='nw')
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
                    time.sleep(.05)
                else:
                    self.status = "enter_for_loop_again"


    def do_stop(self):
        self.stop = True


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

print('Now we can continue running code while mainloop runs!')


# for i in range(10):
#     print("hallo")
#     time.sleep(5)

# for i in range(100000):
#     print(i)
