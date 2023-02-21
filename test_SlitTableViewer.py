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


slitdf = STView()


x = 500
y = 700
width = 50
height = 20

viewer = 'test, no canvas viewer'

from regions import PixCoord, RectanglePixelRegion, PointPixelRegion, RegionVisual

rect_obj = RectanglePixelRegion(PixCoord(x=x,y=y), width=width, height=height)

slitdf.add_slit_obj(rect_obj,viewer)