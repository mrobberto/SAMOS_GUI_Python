#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 09:00:48 2023

@author: samos_dev
"""
import numpy as np
from regions import Regions

from SAMOS_DMD_dev.Class_DMD_dev import DigitalMicroMirrorDevice
dmd = DigitalMicroMirrorDevice()#config_id='pass') 
dmd.initialize()
dmd._open()

#create initial DMD slit mask
slit_shape = np.ones((1080,2048)) # This is the size of the DC2K

regions = Regions.read('my_regions.reg')
for i in range(len(regions)):
    reg = regions[i]
    corners = reg.corners
    #convert CCD corners to DMD corners here
    #TBD
    dmd_corners = corners
    dmd_corners[:][1] = corners[:][1]+500
    ####   
    x1 = round(dmd_corners[0][0])
    y1 = round(dmd_corners[0][1])
    x2 = round(dmd_corners[2][0])
    y2 = round(dmd_corners[2][1])
slit_shape[x1:x2,y1:y2]=0
dmd.apply_shape(slit_shape)  
#dmd.apply_invert()   