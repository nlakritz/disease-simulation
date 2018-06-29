#!/usr/bin/env python3
#
# Graphics for cellular simulations.

import sys
if sys.version[0] != '3':
    raise Exception('diseasegraphics only works with Python 3')

import tkinter as tk
import time

class DiseaseGrid:
    '''
    Manage a grid of cells that can display the state of each individual cell.
    '''
    def __init__ (self, gridsize, sq=0):
        '''
        Initialize the graphics window.
        Set up a grid of cells size gridsize x gridsize.  sq is the size of an individual cell,
        which defaults to 600/gridsize.
        '''
        if (not isinstance (gridsize, int)) or gridsize < 4 or gridsize > 100:
            raise ValueError ('gridsize must be an integer 4-100 (inclusive)')
        if sq == 0:
            sq = 600 // gridsize
        if (not isinstance (sq, int)) or sq < 1:
            raise ValueError ('sq must be a positive integer')
        self.sq = sq
        self.gridsize = gridsize
        totalsize = sq * gridsize
        if totalsize > 3000:
            raise ValueError ('grid would be too big (sq * gridsize > 3000)')
        self.cells = dict()
        self.root = tk.Tk()
        self.canvas = tk.Canvas (self.root, width=self.sq*self.gridsize,
                                 height=self.sq*self.gridsize)
        self.canvas.pack ()
        self.speed = tk.DoubleVar ()
        self.speed.set (10.0)
        self.day_value = tk.StringVar ()
        self.day_value.set ("Start")
        self.day_label = tk.Label (self.root, textvariable=self.day_value)
        self.day_label.pack ()
        self.speed_slider = tk.Scale (self.root, variable=self.speed, from_=0.0, to=20,
                                      resolution=0.2, length=300, orient=tk.HORIZONTAL)
        self.speed_slider.pack ()
        for x in range (self.gridsize):
            for y in range (self.gridsize):
                self.cells[x,y] = self.canvas.create_rectangle (x*self.sq, y*self.sq,
                                                                (x+1)*self.sq, (y+1)*self.sq,
                                                                fill='#ffffff')

    def update_cell (self, x, y, state):
        '''
        Update the state of the cell at position x,y to state.

        Possible values for state are:
        negative: cell is empty
        0:        cell is healthy
        1-100:    cell is sick.  Higher numbers mean the cell has been sick for longer

        We suggest that you calculate the "sick" parameter by sick_days * 100 / max_sick_days
        so that low values mean "barely sick" and 100 means "about to die/survive".
        '''
        if state < 0:
            self.canvas.itemconfig (self.cells[x,y], fill='#ffffff')
        elif state == 0:
            self.canvas.itemconfig (self.cells[x,y], fill='#00cc00')
        else:
            red = 255
            other = int ((100 - state) * 255 / 100)
            self.canvas.itemconfig (self.cells[x,y], fill='#{0:02x}{1:02x}{1:02x}'.format (red, other))


    def display_grid (self, day):
        '''
        Set the displayed day, and then pause for 1/speed seconds.
        So, if speed is set to 10, you'll simulate 10 days per second.
        '''
        t = 0.0
        self.day_value.set ('Day: {0:5d}'.format (day))
        while t < 1.0:
            time.sleep (0.02)
            t += self.speed.get () / 50
            self.root.update ()

    def set_speed (self, speed):
        '''
        Set the number of days simulated per second to speed.  This only impacts the length
        of time that display_grid() pauses when called.
        '''
        self.speed.set (speed)
        self.root.update_idletasks ()

    def self_test (self, n_days = 50):
        for day in range (n_days):
            for x in range (side):
                for y in range (side):
                    shade = max (100 * max ((x + day) % side, (y + day) % side) / side, 1)
                    if x == 10 and y == 10:
                        shade = 0
                    elif 9 <= x <= 11 and 9 <= y <= 11:
                        shade = -1
                    z.update_cell (x, y, shade)
            z.display_grid (day)

if __name__ == '__main__':
    side = 20
    z = DiseaseGrid (side,500 // side)
    z.set_speed (20)
    z.self_test (100)
