#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:31:31 2023

@author: samos_dev
"""



import tkinter as tk
# Used for styling the GUI
#from tkinter import ttk
# import filedialog module
from tkinter import filedialog

from PIL import Image,ImageTk,ImageOps

import os,sys
import shutil
#from astropy.io import ascii
import time

import numpy as np
import pandas as pd

from pathlib import Path
path = Path(__file__).parent.absolute()
local_dir = str(path.absolute())
parent_dir = str(path.parent)   
sys.path.append(parent_dir)

SF_path = parent_dir+"/SAMOS_system_dev"
os.sys.path.append(SF_path)

from SlitTableViewer import SlitTableView as STView

#slitView = STView()

import tksheet


import regions
from regions import Regions
from regions import PixCoord, RectanglePixelRegion, PointPixelRegion, RegionVisual

from SAMOS_DMD_dev.CONVERT.CONVERT_class import CONVERT 
convert = CONVERT()
x = 500
y = 700
width = 50
height = 20

viewer = 'test, no canvas viewer'

from regions import PixCoord, RectanglePixelRegion, PointPixelRegion, RegionVisual


class NewWindow(tk.Tk):
    
    def __init__(self,):# master = None):
        super().__init__()#(master = master)
        
        self.title("New Window")
        self.geometry("200x200")
        
        label = tk.Label(self, text = "New Window")
        label.pack()
        


        btn = tk.Button(self, text = "Open table window")

        btn.bind("<Button>", self.display_slit_table)
        btn.pack(pady=10)
    
    def display_slit_table(self, event):
        
        self.SlitTabView = STView()
        
    def add_slit(self, obj, viewer):
        rect_obj = RectanglePixelRegion(PixCoord(x=x,y=y), width=width, height=height)
        self.SlitTabView.add_slit_obj(rect_obj, viewer)


        
        
root = NewWindow()

root.mainloop()



