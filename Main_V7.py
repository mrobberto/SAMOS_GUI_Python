

#! /usr/bin/env python
#
# example2_tk.py -- Simple, configurable FITS viewer.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import sys
sys.path.append('/opt/anaconda3/envs/samos_env/lib/python3.10/site-packages')

import os
import threading


from ginga.tkw.ImageViewTk import CanvasView
from ginga.canvas.CanvasObject import get_canvas_types
from ginga.misc import log
from ginga.util.loader import load_data
from ginga import colors
from ginga.util.ap_region import astropy_region_to_ginga_canvas_object as r2g
from ginga.util.ap_region import ginga_canvas_object_to_astropy_region as g2r
from ginga.canvas import CompoundMixin as CM


from ginga.util import ap_region

from ginga.AstroImage import AstroImage
img = AstroImage()
from astropy.io import fits

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import regions
from regions import Regions

from astropy import units as u

from ginga.util import iqcalc
iq = iqcalc.IQCalc()



### Needed to run ConvertSIlly by C. Loomis
import math
import pathlib
from astropy.io import ascii
import numpy as np
import glob

#import sewpy   #to run sextractor wrapper

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'
# =============================d================================================
# 
# from Astrometry import tk_class_astrometry
# Astrometry = tk_class_astrometry
# 
# Astrometry.return_from_astrometry()
# 
# =============================================================================
import csv
from pathlib import Path
#define the local directory, absolute so it is not messed up when this is called
path = Path(__file__).parent.absolute()
local_dir = str(path.absolute())
sys.path.append(local_dir)

print("line 48 main local",local_dir)
os.sys.path.append(local_dir)
os.sys.path.append(local_dir+"/Astrometry")
os.sys.path.append(local_dir+"/SAMOS_CCD_dev")
os.sys.path.append(local_dir+"/SAMOS_DMD_dev")
os.sys.path.append(local_dir+"/SAMOS_MOTORS_dev")
os.sys.path.append(local_dir+"/SAMOS_SOAR_dev")
os.sys.path.append(local_dir+"/SAMOS_CONFIG_dev")


from SAMOS_CONFIG_dev.CONFIG_GUI import Config
#print(Config.return_directories)

from SAMOS_Astrometry_dev.tk_class_astrometry_V4 import Astrometry
from SAMOS_CCD_dev.GUI_CCD_dev import GUI_CCD

from SAMOS_CCD_dev.Class_CCD_dev import Class_Camera as CCD
from SAMOS_MOTORS_dev.Class_PCM  import Class_PCM 
Motors  = Class_PCM()
from SAMOS_MOTORS_dev.SAMOS_MOTORS_GUI_dev  import Window as SM_GUI
from SAMOS_DMD_dev.Class_DMD import DigitalMicroMirrorDevice as DMD
from SAMOS_DMD_dev.SAMOS_DMD_GUI_dev import GUI_DMD 
from SAMOS_SOAR_dev.tk_class_SOAR_V0 import SOAR as SOAR
from SAMOS_system_dev.SAMOS_Functions import Class_SAMOS_Functions as SF
#from ginga.misc import widgets 
#import PCM_module_GUI as Motors

#text format for writing new info to header. Global var
param_entry_format = '[Entry {}]\nType={}\nKeyword={}\nValue="{}"\nComment="{}\n"'


class SAMOS_Main(object):

    def __init__(self, logger):

        self.logger = logger
        self.drawcolors = colors.get_colors()
#        self.drawcolors = ['white', 'black', 'red', 'yellow', 'blue', 'green']
        self.canvas_types = get_canvas_types()
        
        root = tk.Tk()
        root.title("SAMOS")
       
        root.geometry("1280x800")   
        
        #root.set_border_width(2)
        #root.connect("delete_event", lambda w, e: self.quit(w))
        self.root = root

        # keep track of the entry number for header keys that need to be added
        # will be used to write "OtherParameters.txt" 
        self.extra_header_params = 0
        self.header_entry_string = '' #keep string of entries to write to a file after acquisition.

# =============================================================================
# #
# # Menu Bar goes into the mac header...
# #
# =============================================================================
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Motors Setup", command=self.load_Motors_module_GUI)
        filemenu.add_command(label="DMD Setup", command=self.load_DMD_module_GUI)
        filemenu.add_command(label="SOAR comm Setup", command=self.load_SOAR_module_GUI)
        filemenu.add_command(label="CCD Acquisition", command=self.load_CCD_module_GUI)
        filemenu.add_command(label="Astrometry", command=self.load_Astrometry)
#        filemenu.add_command(label="Config", command=self.CONFIG_GUI)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)                
        
        
# =============================================================================
#         
#  #    FILTER STATUS Label Frame
#         
# =============================================================================
        self.frame0l = tk.Frame(root,background="cyan")#, width=400, height=800)
        self.frame0l.place(x=4, y=0, anchor="nw", width=220, height=110)
 
        labelframe_Filters =  tk.LabelFrame(self.frame0l, text="Filter Status", font=("Arial", 24))
        labelframe_Filters.pack(fill="both", expand="yes")
          

#        label_FW1 =  tk.Label(labelframe_Filters, text="Filters")
#        label_FW1.place(x=4,y=10)

        all_dirs = SF.read_dir_user()
        filter_data= ascii.read(local_dir+all_dirs['dir_Motors']+'/IDG_Filter_positions.txt')
        filter_names = list(filter_data[0:9]['Filter'])
        print(filter_names)

        self.FW1_filter = tk.StringVar() 
        # initial menu text
        self.FW1_filter.set(filter_names[2])
        # Create Dropdown menu
        self.optionmenu_FW1 = tk.OptionMenu(labelframe_Filters, self.FW1_filter, *filter_names)
        self.optionmenu_FW1.place(x=5, y=8)
        button_SetFW1 =  tk.Button(labelframe_Filters, text="Set Filter", bd=3, command=self.set_filter)
        button_SetFW1.place(x=110,y=4)
        
#        self.Current_Filter = tk.StringVar()
#        self.Current_Filter.set(self.FW1_filter.get())
        self.Label_Current_Filter = tk.Text(labelframe_Filters,font=('Georgia 20'),width=8,height=1,bg='white', fg='green')
        #self.Label_Current_Filter.insert(tk.END,"",#self.FW1_Filter)
        self.Label_Current_Filter.insert(tk.END,self.FW1_filter.get())
        self.Label_Current_Filter.place(x=30,y=45)



# =============================================================================
#         entry_FW1 = tk.Entry(labelframe_Filters, width=11,  bd =3)
#         entry_FW1.place(x=100, y=10)
# # =============================================================================
# =============================================================================
#         label_FW1_template =  tk.Label(labelframe_Filters, text="HH:MM:SS.xx")
#         label_FW1_template.place(x=200,y=10)
#         
# =============================================================================
# =============================================================================
#         label_FW2 =  tk.Label(labelframe_Filters, text="FW 2")
#         label_FW2.place(x=4,y=40)
#         # Dropdown menu options
#         FW2_options = [
#             "[OIII]",
#             "Ha",
#             "[SII]",
#             "blank",
#             "open"
#         ]
#         # datatype of menu text
#         self.FW2_filter = tk.StringVar()
#         # initial menu text
#         self.FW2_filter.set(FW2_options[4])
#         # Create Dropdown menu
#         self.optionmenu_FW2 = tk.OptionMenu(labelframe_Filters, self.FW2_filter, *FW2_options)
#         self.optionmenu_FW2.place(x=40, y=38)
#         button_SetFW2 =  tk.Button(labelframe_Filters, text="Set FW2", bd=3)
#         button_SetFW2.place(x=125,y=34)
# 
# =============================================================================

# =============================================================================
#         entry_FW2 = tk.Entry(labelframe_Filters, width=11, bd =3)
#         entry_FW2.place(x=100, y=40)
# # =============================================================================
# =============================================================================
#         label_FW1_template =  tk.Label(labelframe_Filters, text="2213DD:MM:SS.xx")
#         label_FW1_template.place(x=200,y=10)
#         
# =============================================================================
#        button_HomeFW1 =  tk.Button(labelframe_Filters, text="Home FW1", bd=3)
#        button_HomeFW1.place(x=4,y=70)
#        button_HomeFW2 =  tk.Button(labelframe_Filters, text="Home FW2", bd=3)
#        button_HomeFW2.place(x=105,y=70)

# =============================================================================
#         
#  #    GRISM STATUS Label Frame
#         
# =============================================================================
        self.frame1l = tk.Frame(root,background="cyan")#, width=400, height=800)
        self.frame1l.place(x=4, y=120, anchor="nw", width=220, height=110)

        labelframe_Grating =  tk.LabelFrame(self.frame1l, text="Grism Status", font=("Arial", 24))
        labelframe_Grating.pack(fill="both", expand="yes")
#        labelframe_Grating.place(x=4, y=10)
         
        all_dirs = SF.read_dir_user()
        Grating_data= ascii.read(local_dir+all_dirs['dir_Motors']+'/IDG_Filter_positions.txt')
        self.Grating_names = list(Grating_data[14:18]['Filter'])
        self.Grating_positions= list(Grating_data[14:18]['Position'])
#        print(Grating_names)
#
        self.Grating_Optioned = tk.StringVar() 
        # initial menu text
        index=2
        self.Grating_Optioned.set(self.Grating_names[index])
        # Create Dropdown menu
        self.optionmenu_GR = tk.OptionMenu(labelframe_Grating, self.Grating_Optioned, *self.Grating_names)
        self.optionmenu_GR.place(x=5, y=8)
        button_SetGR =  tk.Button(labelframe_Grating, text="Set Grating", bd=3, command=self.set_grating)
        button_SetGR.place(x=110,y=4)


# =============================================================================
#         self.Grating_int = tk.IntVar() 
#         self.Grating_int.set(2)  
#         self.optionmenu_GR = tk.OptionMenu(labelframe_Grating, self.Grating_int, *self.Grating_names)
#         self.optionmenu_GR.place(x=5, y=8)
#         button_SetGR =  tk.Button(labelframe_Grating, text="Set Grating", bd=3, command=self.set_grating)
#         button_SetGR.place(x=110,y=4)
# 
# =============================================================================
        self.Label_Current_Grating = tk.Text(labelframe_Grating,font=('Georgia 20'),width=8,height=1,bg='white', fg='green')
        #self.Label_Current_Filter.insert(tk.END,"",#self.FW1_Filter)
        self.Label_Current_Grating.insert(tk.END,self.Grating_names[index])
        self.Label_Current_Grating.place(x=30,y=45)

        
# =============================================================================
#         # Dropdown menu options
#         options = [
#             "Low Blue",
#             "Low Red",
#             "High Blue",
#             "High Red"
#         ]
#         # datatype of menu text
#         self.grating = tk.StringVar()
#         # initial menu text
#         self.grating.set(options[2])
#         # Create Dropdown menu
#         self.optionmenu_grating = tk.OptionMenu(labelframe_Grating, self.grating, *options)
#         self.optionmenu_grating.place(x=4, y=0)
# 
#         button_HomeGrating=  tk.Button(labelframe_Grating, text="Home Grating", bd=3)
#         button_HomeGrating.place(x=4,y=35)
# 
# =============================================================================
# =============================================================================

# =============================================================================
#         label_FW1 =  tk.Label(labelframe_Filters, text="Grism")
#         label_FW1.place(x=4,y=10)
#         entry_FW1 = tk.Entry(labelframe_Filters, width=5,  bd =3)
#         entry_FW1.place(x=100, y=10)
#         label_FW2 =  tk.Label(labelframe_Filters, text="Filter Wheel 2")
#         label_FW2.place(x=4,y=40)
#         entry_FW2 = tk.Entry(labelframe_Filters, width=5, bd =3)
#         entry_FW2.place(x=100, y=40)
#         
#         button_HomeFW1 =  tk.Button(labelframe_Filters, text="Home FW1", bd=3)
#         button_HomeFW1.place(x=0,y=70)
#         button_HomeFW2 =  tk.Button(labelframe_Filters, text="Home FW2", bd=3)
#         button_HomeFW2.place(x=105,y=70)
# 
# =============================================================================
#         self.frame0r = tk.Frame(root,background="cyan")#, width=400, height=800)
#         self.frame0r.place(x=601, y=0, anchor="nw", width=500, height=800)
#         
#         
#         vbox = tk.Frame(self.frame0l, relief=tk.RAISED, borderwidth=1)
#         vbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# =============================================================================


# =============================================================================
#         
#  #    ACQUIRE IMAGE Label Frame
#         
# =============================================================================
        self.frame2l = tk.Frame(root,background="cyan")#, width=400, height=800)
        self.frame2l.place(x=0, y=240, anchor="nw", width=370, height=280)

#        root = tk.Tk()
#        root.title("Tab Widget")
        tabControl = ttk.Notebook(self.frame2l)
  
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)
  
        tabControl.add(tab1, text ='Image')
        tabControl.add(tab2, text ='Bias')
        tabControl.add(tab3, text ='Dark')
        tabControl.add(tab4, text ='Flat')
        tabControl.pack(expand = 1, fill ="both")
  
# =============================================================================
#      SCIENCE
# =============================================================================

        labelframe_Acquire =  tk.LabelFrame(tab1, text="Acquire Image", font=("Arial", 24))
        labelframe_Acquire.pack(fill="both", expand="yes")
#        labelframe_Grating.place(x=4, y=10)

        label_ExpTime =  tk.Label(labelframe_Acquire, text="Exp. Time (s)")
        label_ExpTime.place(x=4,y=10)
        self.Light_ExpT=tk.StringVar()
        self.Light_ExpT.set("0.01")
        entry_ExpTime = tk.Entry(labelframe_Acquire, textvariable=self.Light_ExpT, width=5,  bd =3)
        entry_ExpTime.place(x=100, y=10)

        label_ObjectName =  tk.Label(labelframe_Acquire, text="Object Name:")
        label_ObjectName.place(x=4,y=40)
        entry_ObjectName = tk.Entry(labelframe_Acquire, width=11,  bd =3)
        entry_ObjectName.place(x=100, y=38)

        label_Comment =  tk.Label(labelframe_Acquire, text="Comment:")
        label_Comment.place(x=4,y=70)
#        scrollbar = tk.Scrollbar(orient="horizontal")
        entry_Comment = tk.Entry(labelframe_Acquire, width=11,  bd =3)# , xscrollcommand=scrollbar.set)
        entry_Comment.place(x=100, y=68)

        button_ExpStart=  tk.Button(labelframe_Acquire, text="START", bd=3, bg='#0052cc',font=("Arial", 24),
                                         command=self.expose_light)
        button_ExpStart.place(x=75,y=95)

        label_Display =  tk.Label(labelframe_Acquire, text="Subtract for Display:")
        label_Display.place(x=4,y=135)
        self.subtract_Bias = tk.IntVar()
        check_Bias = tk.Checkbutton(labelframe_Acquire, text='Bias',variable=self.subtract_Bias, onvalue=1, offvalue=0)
        check_Bias.place(x=4, y=155)
        self.subtract_Dark = tk.IntVar()
        check_Dark = tk.Checkbutton(labelframe_Acquire, text='Dark',variable=self.subtract_Dark, onvalue=1, offvalue=0)
        check_Dark.place(x=60,y=155)
        self.subtract_Flat = tk.IntVar()
        check_Flat = tk.Checkbutton(labelframe_Acquire, text='Flat',variable=self.subtract_Flat, onvalue=1, offvalue=0)
        check_Flat.place(x=120,y=155)

# =============================================================================
#      BIAS
# =============================================================================
        labelframe_Bias =  tk.LabelFrame(tab2, text="Bias", 
                                                     width=300, height=170,
                                                     font=("Arial", 24))
        labelframe_Bias.pack(fill="both", expand="yes")

#        labelframe_Bias.place(x=5,y=5)
        label_Bias_ExpT =  tk.Label(labelframe_Bias, text="Exposure time (s):")
        label_Bias_ExpT.place(x=4,y=10)
        self.Bias_ExpT = tk.StringVar(value="0.00")
        entry_Bias_ExpT = tk.Entry(labelframe_Bias, width=6,  bd =3, textvariable=self.Bias_ExpT)
        entry_Bias_ExpT.place(x=120, y=6)
        
        label_Bias_NofFrames =  tk.Label(labelframe_Bias, text="Nr. of Frames:")
        label_Bias_NofFrames.place(x=4,y=40)
        self.Bias_NofFrames = tk.StringVar(value="10")
        entry_Bias_NofFrames = tk.Entry(labelframe_Bias, width=5,  bd =3, textvariable=self.Bias_NofFrames)
        entry_Bias_NofFrames.place(x=100, y=38)
        
        
        self.var_Bias_saveall = tk.IntVar()
        r1_Bias_saveall = tk.Radiobutton(labelframe_Bias, text = "Save single frames", variable=self.var_Bias_saveall, value=1)
        r1_Bias_saveall.place(x=160, y=38)

        label_Bias_MasterFile =  tk.Label(labelframe_Bias, text="Master Bias File:")
        label_Bias_MasterFile.place(x=4,y=70)
        self.Bias_MasterFile = tk.StringVar(value="Bias")
        entry_Bias_MasterFile = tk.Entry(labelframe_Bias, width=11,  bd =3, textvariable=self.Bias_MasterFile)
        entry_Bias_MasterFile.place(x=120, y=68)

        button_ExpStart=  tk.Button(labelframe_Bias, text="START", bd=3, bg='#0052cc',font=("Arial", 24),
                                          command=self.expose_bias)
        button_ExpStart.place(x=75,y=95)
  
#        root.mainloop()  




        
# =============================================================================
#      Dark
# =============================================================================
        labelframe_Dark =  tk.LabelFrame(tab3, text="Dark", 
                                                     width=300, height=170,
                                                     font=("Arial", 24))
        labelframe_Dark.pack(fill="both", expand="yes")

        label_Dark_ExpT =  tk.Label(labelframe_Dark, text="Exposure time (s):")
        label_Dark_ExpT.place(x=4,y=10)
        self.Dark_ExpT = tk.StringVar(value="0.00")
        entry_Dark_ExpT = tk.Entry(labelframe_Dark, width=6,  bd =3, textvariable=self.Dark_ExpT)
        entry_Dark_ExpT.place(x=120, y=6)
        
        label_Dark_NofFrames =  tk.Label(labelframe_Dark, text="Nr. of Frames:")
        label_Dark_NofFrames.place(x=4,y=40)
        self.Dark_NofFrames = tk.StringVar(value="10")
        entry_Dark_NofFrames = tk.Entry(labelframe_Dark, width=5,  bd =3, textvariable=self.Dark_NofFrames)
        entry_Dark_NofFrames.place(x=100, y=38)
        
        
        self.var_Dark_saveall = tk.IntVar()
        r1_Dark_saveall = tk.Radiobutton(labelframe_Dark, text = "Save single frames", variable=self.var_Dark_saveall, value=1)
        r1_Dark_saveall.place(x=160, y=38)

        label_Dark_MasterFile =  tk.Label(labelframe_Dark, text="Master Dark File:")
        label_Dark_MasterFile.place(x=4,y=70)
        self.Dark_MasterFile = tk.StringVar(value="Dark")
        entry_Dark_MasterFile = tk.Entry(labelframe_Dark, width=11,  bd =3, textvariable=self.Dark_MasterFile)
        entry_Dark_MasterFile.place(x=120, y=68)

        button_ExpStart=  tk.Button(labelframe_Dark, text="START", bd=3, bg='#0052cc',font=("Arial", 24),
                                          command=self.expose_dark)
        button_ExpStart.place(x=75,y=95)

# =============================================================================
#      Flat
# =============================================================================
        labelframe_Flat =  tk.LabelFrame(tab4, text="Flat", 
                                                     width=300, height=170,
                                                     font=("Arial", 24))
        labelframe_Flat.pack(fill="both", expand="yes")

        label_Flat_ExpT =  tk.Label(labelframe_Flat, text="Exposure time (s):")
        label_Flat_ExpT.place(x=4,y=10)
        self.Flat_ExpT = tk.StringVar(value="0.00")
        entry_Flat_ExpT = tk.Entry(labelframe_Flat, width=6,  bd =3, textvariable=self.Flat_ExpT)
        entry_Flat_ExpT.place(x=120, y=6)
        
        label_Flat_NofFrames =  tk.Label(labelframe_Flat, text="Nr. of Frames:")
        label_Flat_NofFrames.place(x=4,y=40)
        self.Flat_NofFrames = tk.StringVar(value="10")
        entry_Flat_NofFrames = tk.Entry(labelframe_Flat, width=5,  bd =3, textvariable=self.Flat_NofFrames)
        entry_Flat_NofFrames.place(x=100, y=38)
        
        
        self.var_Flat_saveall = tk.IntVar()
        r1_Flat_saveall = tk.Radiobutton(labelframe_Flat, text = "Save single frames", variable=self.var_Flat_saveall, value=1)
        r1_Flat_saveall.place(x=160, y=38)

        label_Flat_MasterFile =  tk.Label(labelframe_Flat, text="Master Flat File:")
        label_Flat_MasterFile.place(x=4,y=70)
        self.Flat_MasterFile = tk.StringVar(value="Flat")
        entry_Flat_MasterFile = tk.Entry(labelframe_Flat, width=11,  bd =3, textvariable=self.Flat_MasterFile)
        entry_Flat_MasterFile.place(x=120, y=68)

        button_ExpStart=  tk.Button(labelframe_Flat, text="START", bd=3, bg='#0052cc',font=("Arial", 24),
                                          command=self.expose_flat)
        button_ExpStart.place(x=75,y=95)



        
        
# =============================================================================
#         
#  #    FITS manager
#         
# =============================================================================
        self.frame_FITSmanager = tk.Frame(root,background="pink")#, width=400, height=800)
        self.frame_FITSmanager.place(x=0, y=500, anchor="nw", width=220, height=250)

        labelframe_FITSmanager =  tk.LabelFrame(self.frame_FITSmanager, text="FITS manager", font=("Arial", 24))
        labelframe_FITSmanager.pack(fill="both", expand="yes")

# =============================================================================
# 
#          
# 
#         label_FW1 =  tk.Label(labelframe_Filters, text="Filter Wheel 1")
#         label_FW1.place(x=4,y=10)
#         entry_FW1 = tk.Entry(labelframe_Filters, width=5,  bd =3)
#         entry_FW1.place(x=100, y=10)
#         label_FW2 =  tk.Label(labelframe_Filters, text="Filter Wheel 2")
#         label_FW2.place(x=4,y=40)
#         entry_FW2 = tk.Entry(labelframe_Filters, width=5, bd =3)
#         entry_FW2.place(x=100, y=40)
#         
# =============================================================================
 
        button_FITS_Load =  tk.Button(labelframe_FITSmanager, text="FITS Load", bd=3, 
                                           command=self.load_last_file)
        button_FITS_Load.place(x=0,y=25)
        
        self.stop_it = 0
        button_FITS_start =  tk.Button(labelframe_FITSmanager, text="FITS start", bd=3, 
                                           command=self.check_for_file_existence)#start_the_loop)
        button_FITS_start.place(x=0,y=50)

# =============================================================================
        button_Astrometry =  tk.Button(labelframe_FITSmanager, text="Astrometry", bd=3, 
#                                            command=Astrometry)
                                            command=self.load_Astrometry)
        button_Astrometry.place(x=0,y=110)

# 
# =============================================================================
        button_run_Sextractor =  tk.Button(labelframe_FITSmanager, text="run DaoFind", bd=3, 
                                            command=self.run_DaoFind)
        button_run_Sextractor.place(x=0,y=80)
        label_sigma =  tk.Label(labelframe_FITSmanager, text="sigma")
        label_sigma.place(x=120,y=82)
        self.sigma=tk.StringVar()
        entry_sigma = tk.Entry(labelframe_FITSmanager, width=3,  bd =3, textvariable=self.sigma)
        entry_sigma.place(x=160, y=80)
        self.sigma.set('25')


# 
# =============================================================================
        button_show_slits =  tk.Button(labelframe_FITSmanager, text="Show slits", bd=3, 
#                                            command=Astrometry)
                                            command=self.show_slits)
        button_show_slits.place(x=0,y=140)

# =============================================================================
#
# GINGA DISPLAY
#
# =============================================================================

        vbox = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
#        vbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        vbox.pack(side=tk.TOP)
        vbox.place(x=350, y=0, anchor="nw")#, width=500, height=800)
        #self.vb = vbox

        canvas = tk.Canvas(vbox, bg="grey", height=514, width=522)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        fi = CanvasView(logger) #=> ImageViewTk -- a backend for Ginga using a Tk canvas widget
        fi.set_widget(canvas)  #=> Call this method with the Tkinter canvas that will be used for the display.
        #fi.set_redraw_lag(0.0)
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        #fi.enable_draw(False)
        # tk seems to not take focus with a click
        fi.set_enter_focus(True)
        fi.set_callback('cursor-changed', self.cursor_cb)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_set_active(True)
        fi.show_pan_mark(True)
        # add little mode indicator that shows keyboard modal states
        fi.show_mode_indicator(True, corner = 'ur')
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        # canvas that we will draw on
#        DrawingCanvas = fi.getDrawClasses('drawingcanvas')
        canvas = self.canvas_types.DrawingCanvas()
        canvas.enable_draw(True)
        canvas.enable_edit(True)
        canvas.set_drawtype('point', color='red')
        canvas.register_for_cursor_drawing(fi)
        canvas.add_callback('draw-event', self.draw_cb)
        canvas.set_draw_mode('draw')
        canvas.set_surface(fi)
        canvas.ui_set_active(True)
        self.canvas = canvas


#        # add canvas to viewers default canvas
        fi.get_canvas().add(canvas)

        self.drawtypes = canvas.get_drawtypes()
        self.drawtypes.sort()

#        fi.configure(516, 528) #height, width
        fi.set_window_size(514,522)

        hbox = tk.Frame(root)
        hbox.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.readout = tk.Label(root, text='')
        self.readout.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.drawtypes = canvas.get_drawtypes()
        ## wdrawtype = ttk.Combobox(root, values=self.drawtypes,
        ##                          command=self.set_drawparams)
        ## index = self.drawtypes.index('ruler')
        ## wdrawtype.current(index)
        wdrawtype = tk.Entry(hbox, width=12)
        wdrawtype.insert(0, 'point')
        wdrawtype.bind("<Return>", self.set_drawparams)
        self.wdrawtype = wdrawtype

        self.vslit = tk.IntVar()
        wslit = tk.Checkbutton(hbox, text="Slit", variable=self.vslit)
        self.wslit = wslit

        wdrawcolor = ttk.Combobox(hbox, values=self.drawcolors)#,
        #                           command=self.set_drawparams)
        index = self.drawcolors.index('lightblue')
        wdrawcolor.current(index)
        wdrawcolor.bind("<<ComboboxSelected>>", self.set_drawparams)
        #wdrawcolor = tk.Entry(hbox, width=12)
        #wdrawcolor.insert(0, 'blue')
        #wdrawcolor.bind("<Return>", self.set_drawparams)
        self.wdrawcolor = wdrawcolor

        self.vfill = tk.IntVar()
        wfill = tk.Checkbutton(hbox, text="Fill", variable=self.vfill)
        self.wfill = wfill

        walpha = tk.Entry(hbox, width=12)
        walpha.insert(0, '0.0')
        walpha.bind("<Return>", self.set_drawparams)
        self.walpha = walpha

        wrun = tk.Button(hbox, text="Run code",
                                command=self.run_code)
        wclear = tk.Button(hbox, text="Clear Canvas",
                                command=self.clear_canvas)
        wsave = tk.Button(hbox, text="Save Canvas",
                                command=self.save_canvas)
        wopen = tk.Button(hbox, text="Open File",
                               command=self.open_file)
                # pressing quit button freezes application and forces kernel restart.
        wquit = tk.Button(hbox, text="Quit",
                               command=lambda: self.quit(root))

        for w in (wquit, wsave, wclear, wrun, walpha, tk.Label(hbox, text='Alpha:'),
                  wfill, wdrawcolor, wslit, wdrawtype, wopen):
            w.pack(side=tk.RIGHT)

        mode = self.canvas.get_draw_mode() #initially set to draw by line >canvas.set_draw_mode('draw')
        hbox1 = tk.Frame(hbox)
        hbox1.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.setChecked = tk.StringVar(None,"draw")
        btn1 = tk.Radiobutton(hbox1,text="Draw",padx=20,variable=self.setChecked,value="draw", command=self.set_mode_cb).pack(anchor=tk.SW)
        btn2 = tk.Radiobutton(hbox1,text="Edit",padx=20,variable=self.setChecked,value="edit", command=self.set_mode_cb).pack(anchor=tk.SW)
        btn3 = tk.Radiobutton(hbox1,text="Pick",padx=20,variable=self.setChecked,value="pick", command=self.set_mode_cb).pack(anchor=tk.SW)
 





#        IPs = Config.load_IP_user(self)
        #print(IPs)
# =============================================================================
#     def open_Astrometry(self):
#         btn = tk.Button(master,
#              text ="Click to open a new window",
#              command = openNewWindow)
#         btn.pack(pady = 10)ƒ
#         return self.Astrometry(master)
# =============================================================================
    def set_filter(self):
        print(self.FW1_filter.get())
        print('moving to filter:',self.FW1_filter.get()) 
#        self.Current_Filter.set(self.FW1_filter.get())
        filter = self.FW1_filter.get()
        print(filter)
        t = Motors.move_filter_wheel(filter)
        #self.Echo_String.set(t)
        print(t)
 
        self.Label_Current_Filter.delete("1.0","end")
        self.Label_Current_Filter.insert(tk.END,self.FW1_filter.get())
        
        self.extra_header_params+=1
        entry_string = param_entry_format.format(self.extra_header_params,'String','FILTER',
                                                 filter,'Selected filter')
        self.header_entry_string+=entry_string
        
    def set_grating(self):
        print(self.Grating_names,self.Grating_Optioned.get())
        i_selected = self.Grating_names.index(self.Grating_Optioned.get())
        print(i_selected) 
#        Grating_Position_Optioned 
        GR_pos = self.Grating_positions[i_selected]
        print(GR_pos)
 #       print('moving to grating',Grating_Position_Optioned) 
#        self.Current_Filter.set(self.FW1_filter.get())
#        grating = str(Grating_Position_Optioned)
#        print(grating)
#        t = Motors.move_grism_rails(grating)
#        GR_pos = self.selected_GR_pos.get()
#        print(type(GR_pos),type(str(GR_pos)),type("GR_B1")) 
        t = Motors.move_grism_rails(GR_pos)
#        self.Echo_String.set(t)
        print(t)
        #self.Label_Current_Filter.insert(tk.END,"",#self.FW1_Filter)
        self.Label_Current_Grating.delete("1.0","end")
        self.Label_Current_Grating.insert(tk.END,self.Grating_Optioned.get())
       
        
        self.extra_header_params+=1
        entry_string = param_entry_format.format(self.extra_header_params,'String','GRISM',
                                                  i_selected,'Grism position')
        self.header_entry_string+=entry_string
        
        print(entry_string)
        
    def get_widget(self):
        return self.root

    def set_drawparams(self, evt):
        kind = self.wdrawtype.get()
        color = self.wdrawcolor.get()
        alpha = float(self.walpha.get())
        fill = self.vfill.get() != 0

        params = {'color': color,
                  'alpha': alpha,
                  #'cap': 'ball',
                  }
        if kind in ('circle', 'rectangle', 'polygon', 'triangle',
                    'righttriangle', 'ellipse', 'square', 'box'):
            params['fill'] = fill
            params['fillalpha'] = alpha

        self.canvas.set_drawtype(kind, **params)

    def save_canvas(self):
        from ginga.util import ap_region
        regs = ap_region.export_regions_canvas(self.canvas, logger=self.logger)
        #self.canvas.save_all_objects()

    def clear_canvas(self):
        CM.CompoundMixin.delete_all_objects(self.canvas,redraw=True)
#        self.canvas.deleteAllObjects()

#ConvertSIlly courtesy of C. Loomis
    def convertSIlly(self,fname, outname=None):
    	FITSblock = 2880

    # If no output file given, just prepend "fixed"
    	if outname is None:
            fname = pathlib.Path(fname)
            dd = fname.parent
            outname = pathlib.Path(fname.parent, 'fixed'+fname.name)
    
    	with open(fname, "rb") as in_f:
            buf = in_f.read()

    # Two fixes:
    # Header cards:
    	buf = buf.replace(b'SIMPLE  =                    F', b'SIMPLE  =                    T')
    	buf = buf.replace(b'BITPIX  =                  -16', b'BITPIX  =                   16')
    	buf = buf.replace(b"INSTRUME= Spectral Instruments, Inc. 850-406 camera  ", b"INSTRUME= 'Spectral Instruments, Inc. 850-406 camera'")
    
    # Pad to full FITS block:
    	blocks = len(buf) / FITSblock
    	pad = round((math.ceil(blocks) - blocks) * FITSblock)
    	buf = buf + (b'\0' * pad)
    
    	with open(outname, "wb+") as out_f:
            out_f.write(buf)

# =============================================================================
# # Expose_light
# 
# =============================================================================
    def expose_light(self):
        self.image_type = "science"
        ExpTime_ms = float(self.Light_ExpT.get())*1000
        params = {'Exposure Time':ExpTime_ms,'CCD Temperature':2300, 'Trigger Mode': 4, 'NofFrames': 1}
        self.expose(params)
#        self.combine_files()
        self.handle_light()
        print("science file created")

# =============================================================================
# # Expose_bias
# 
# =============================================================================
    def expose_bias(self):
        self.image_type = "bias"
        ExpTime_ms = float(self.Bias_ExpT.get())*1000
        params = {'Exposure Time':ExpTime_ms,'CCD Temperature':2300, 'Trigger Mode': 5, 'NofFrames': int(self.Bias_NofFrames.get())}
        #cleanup the directory to remove setimage_ files that may be refreshed
        self.cleanup_files()
        self.expose(params)
        self.combine_files()
        print("Superbias file created")
        
                       
# =============================================================================
# # Expose_dark
# 
# =============================================================================
    def expose_dark(self):
        self.image_type = "dark"
        ExpTime_ms = float(self.Dark_ExpT.get())*1000
        params = {'Exposure Time':ExpTime_ms,'CCD Temperature':2300, 'Trigger Mode': 5, 'NofFrames': int(self.Dark_NofFrames.get())}
        self.expose(params)
        self.combine_files()
        self.handle_dark()
        print("Superdark file created")


# =============================================================================
# # Expose_flat
# 
# =============================================================================
    def expose_flat(self):
        self.image_type = "flat"
        ExpTime_ms = float(self.Flat_ExpT.get())*1000
        params = {'Exposure Time':ExpTime_ms,'CCD Temperature':2300, 'Trigger Mode': 4, 'NofFrames': int(self.Flat_NofFrames.get())}
        self.expose(params)
        self.combine_files()
        self.handle_flat()
        print("Superflat file created")
        #Camera= CCD(dict_params=params)

# =============================================================================
# # Handle files: sets or single?
# 
# =============================================================================
    def combine_files(self):
        #this procedure runs after the CCD.expose()
        #to handle the decision of saving all single files or just the averages
        file_names = local_dir+"/fits_image/setimage_*.fit"
        files = glob.glob(file_names)
        superfile_cube = np.zeros((1032,1056,len(files)))   #note y,x,z
        for i in range(len(files)):
            print(files[i])
            with fits.open(files[i]) as hdu:
                superfile_cube[:,:,i] = hdu[0].data
                if self.var_Bias_saveall.get() == 1 or \
                   self.var_Dark_saveall.get() == 1 or \
                   self.var_Flat_saveall.get() == 1:
                   #save every single frame
                    os.rename(files[i],local_dir+"/fits_image/"+self.image_type+"_"+str(i)+".fits")
                else: 
                    os.remove(files[i])
        superfile = superfile_cube.mean(axis=2)        
        superfile_header = hdu[0].header
        fits.writeto(local_dir+"/fits_image/super"+self.image_type+".fits",superfile,superfile_header,overwrite=True)
            
    def cleanup_files(self):
        file_names = local_dir+"/fits_image/"+self.image_type+"_*.fits"
        files = glob.glob(file_names)
        for i in range(len(files)):
             os.remove(files[i])
        
    def handle_dark(self):
        dark_file = local_dir+"/fits_image/superdark.fits"
        bias_file = local_dir+"/fits_image/superbias.fits"
        hdu_dark = fits.open(dark_file)
        dark = hdu_dark[0].data
        hdu_bias = fits.open(bias_file)
        bias = hdu_bias[0].data
        
        if self.subtract_Bias.get() == 1:
            dark_bias = dark-bias
        else:    
            dark_bias = dark
        
        hdr = hdu_dark[0].header
        exptime = hdr['PARAM2']
        dark_sec = dark_bias / exptime
        hdr_out = hdr
        hdr_out['PARAM2']=1
        fits.writeto(local_dir+"/fits_image/superdark_s.fits",dark_sec,hdr_out,overwrite=True)

    def handle_flat(self):
        flat_file = local_dir+"/fits_image/superflat.fits"
        dark_s_file = local_dir+"/fits_image/superdark_s.fits"
        bias_file = local_dir+"/fits_image/superbias.fits"
        hdu_flat = fits.open(flat_file)
        flat = hdu_flat[0].data
        hdu_bias = fits.open(bias_file)
        bias = hdu_bias[0].data
        if self.subtract_Bias.get() == 1:
            flat_bias = flat-bias
        else:    
            flat_bias = flat

        hdr = hdu_flat[0].header
        exptime = hdr['PARAM2']
        hdu_dark_s = fits.open(dark_s_file)
        dark_s = hdu_dark_s[0].data
        dark = dark_s * exptime
        if self.subtract_Dark.get() == 1:
            flat_dark = flat-dark
            flat_dark = flat - dark
        else:    
            flat_dark = flat
        flat_norm = flat_dark / np.median(flat_dark)
        fits.writeto(local_dir+"/fits_image/superflat_norm.fits",flat_norm,hdr,overwrite=True)
        
    def handle_light(self):
        light_file = local_dir+"/fits_image/newimage.fit"
        flat_file = local_dir+"/fits_image/superflat_norm.fits"
        dark_s_file = local_dir+"/fits_image/superdark_s.fits"
        bias_file = local_dir+"/fits_image/superbias.fits"
        
        hdu_light = fits.open(light_file)
        light = hdu_light[0].data
        
        hdu_bias = fits.open(bias_file)
        bias = hdu_bias[0].data
        
        hdu_dark_s = fits.open(dark_s_file)
        dark_s = hdu_dark_s[0].data
        
        hdu_flat = fits.open(flat_file)
        flat = hdu_flat[0].data

        hdr = hdu_light[0].header
        exptime = hdr['PARAM2']

        if self.subtract_Bias.get() == 1:
            light_bias = light-bias
        else:    
            light_bias = light
            
        if self.subtract_Dark.get() == 1:
            light_dark = light_bias - dark_s * exptime
        else:    
            light_dark = light_bias

        if self.subtract_Flat.get() == 1:
            light_dark_bias = np.divide(light_dark, flat) 
        else:    
            light_dark_bias = light_dark
        fits_image = local_dir+"/fits_image/newimage_ff.fits"    
        fits.writeto(fits_image,light_dark_bias,hdr,overwrite=True)
        self.Display(fits_image)
       

# =============================================================================
# # Expose
# 
# =============================================================================

    def expose(self,params):
        
        #Prepare the exposure parameers
        #ExpTime_ms = float(self.ExpTime.get())*1000
        #params = {'Exposure Time':ExpTime_ms,'CCD Temperature':2300, 'Trigger Mode': 4}
        Camera= CCD(dict_params=params)
        
        self.this_param_file = open("{}/Parameters.txt".format(os.getcwd()),"w")
        
        self.this_param_file.write(self.header_entry_string)
        self.this_param_file.close()
        #Expose
        data = Camera.expose()
        
        #Fix the fit header from U16 to I16, creating a new image
        #create proper working directory
        work_dir = os.getcwd()

        ##fits_image = "/Users/robberto/Box/@Massimo/_Python/SAMOS_GUI_dev/fits_image/newimage_fixed.fit"
        #fits_image = "{}/fits_image/newimage_fixed.fit".format(work_dir)
        self.fits_image = "{}/fits_image/newimage.fit".format(work_dir)
        
        ##fits_image_converted = "/Users/robberto/Box/@Massimo/_Python/SAMOS_GUI_dev/fits_image/newimage_fixed.fit"             		
#        fits_image_converted = "{}/fits_image/newimage_fixed.fit".format(work_dir)         		
        
#        self.convertSIlly(fits_image,fits_image_converted)
        #To do: cancel the original image.= If the canera is active; otherwise leave it.
        #Hence, we need a general switch to activate if the camera is running.
        #Hence, we may need a general login window.
        self.Display(self.fits_image)

    def Display(self,imagefile): 
#        image = load_data(fits_image_converted, logger=self.logger)

        # AstroImage object of ginga.AstroImage module
        self.AstroImage = load_data(imagefile, logger=self.logger)
      
        # passes the image to the viewer through the set_image() method
        self.fitsimage.set_image(self.AstroImage)

       
        

    def load_last_file(self):
        FITSfiledir = './fits_image/'
        self.fullpath_FITSfilename = FITSfiledir + (os.listdir(FITSfiledir))[0] 
            # './fits_image/cutout_rebined_resized.fits'
        self.AstroImage = load_data(self.fullpath_FITSfilename, logger=self.logger)
        # AstroImage object of ginga.AstroImage module
        
        # passes the image to the viewer through the set_image() method
        self.fitsimage.set_image(self.AstroImage)
        self.root.title(self.fullpath_FITSfilename)

        
# =============================================================================
#     def start_the_loop(self):
#         while self.stop_it == 0:
#             threading.Timer(1.0, self.load_manager_last_file).start() 
# 
#     def load_manager_last_file(self):
#         FITSfiledir = './fits_image/'
#         self.fullpath_FITSfilename = FITSfiledir + (os.listdir(FITSfiledir))[0]
#         print(self.fullpath_FITSfilename)        
# 
#     def stop_the_loop(self):
#         self.stop_it == 1
# 
# =============================================================================
    def check_for_file_existence(self):
        from os.path import exists as file_exists
        import time
        FITSfiledir = './fits_image/'
        while len(os.listdir(FITSfiledir)) == 0:
            print('nothing here')
            time.sleep(1)
        time.sleep(1) #one second to complete data transfer
        self.load_last_file()
        print('and move fits file')
        

# =============================================================================
#         image = load_data(self.fullpath_FITSfilename, logger=self.logger)
#         self.fitsimage.set_image(image)
#         self.root.title(self.fullpath_FITSfilename)
# 
# =============================================================================



    def load_file(self):
        self.AstroImage = load_data(self.fullpath_FITSfilename, logger=self.logger)
        self.canvas.set_image(self.AstroImage)
        self.root.title(self.fullpath_FITSfilename)

    def open_file(self):
        filename = askopenfilename(filetypes=[("allfiles", "*"),
                                              ("fitsfiles", "*.fits")])
        self.load_file(filename)

    def run_code(self):
        """
        # Find approximate bright peaks in a sub-area
        from ginga.util import iqcalc
        iq = iqcalc.IQCalc()
    
        r = self.canvas.objects[0]
        img_data = self.AstroImage.get_data()
        data_box = self.AstroImage.cutout_shape(r)
        
        peaks = iq.find_bright_peaks(data_box)
        print(peaks[:20])  # subarea coordinates
        px,py=round(peaks[0][0]+r.x1),round(peaks[0][1]+r.y2)
        print(px,py)   #image coordinates
        print(img_data[px,py]) #actual counts
     
        # evaluate peaks to get FWHM, center of each peak, etc.
        objs = iq.evaluate_peaks(peaks, data_box)       
        # how many did we find with standard thresholding, etc.
        # see params for find_bright_peaks() and evaluate_peaks() for details
        print(len(objs))
        # example of what is returned
        o1 = objs[0]
        print(o1)
           
        # pixel coords are for cutout, so add back in origin of cutout
        #  to get full data coords RA, DEC of first object
        x1, y1, x2, y2 = r.get_llur()
        self.img.pixtoradec(x1+o1.objx, y1+o1.objy)
          
        # Draw circles around all objects
        Circle = self.canvas.get_draw_class('circle')
        for obj in objs:
            x, y = x1+obj.objx, y1+obj.objy
            if r.contains(x, y):
                self.canvas.add(Circle(x, y, radius=10, color='yellow'))
        
        # set pan and zoom to center
        self.fitsimage.set_pan((x1+x2)/2, (y1+y2)/2)
        self.fitsimage.scale_to(0.75, 0.75)
        
        r_all = self.canvas.objects[:]
        print(r_all)
        
        
        EXERCISE COMPOUNDMIXING CLASS
        r_all is a CompountMixing object, see class ginga.canvas.CompoundMixin.CompoundMixin
         https://ginga.readthedocs.io/en/stable/_modules/ginga/canvas/CompoundMixin.html#CompoundMixin.get_objects_by_kinds        
              
        #check that we have created a compostition of objects:
        from ginga.canvas import CompoundMixin as CM
        CM.CompoundMixin.is_compound(self.canvas.objects)     # True

        #we can find out what are the "points" objects
        points = CM.CompoundMixin.get_objects_by_kind(self.canvas,'point')
        print(list(points))
        
        #we can remove what we don't like, e.g. points
        points = CM.CompoundMixin.get_objects_by_kind(self.canvas,'point')
        list_point=list(points)
        CM.CompoundMixin.delete_objects(self.canvas,list_point)
        self.canvas.objects   #check that the points are gone
           
        #we can remove both points and boxes
        points = CM.CompoundMixin.get_objects_by_kinds(self.canvas,['point','box'])
        list_points=list(points)
        CM.CompoundMixin.delete_objects(self.canvas,list_points)
        self.canvas.objects   #check that the points are gone
       
        #drawing an object can be done rather easily
        #first take an object fromt the list and change something
        objects=CM.CompoundMixin.get_objects(self.canvas)
        o0=objects[0]
        o0.y1=40
        o0.height=100
        o0.width=70
        o0.color='lightblue'
        CM.CompoundMixin.draw(self.canvas,self.canvas.viewer)
        
        END OF THE COMPOUNDMIXING EXCERCISE
                
        # region = 'fk5;circle(290.96388,14.019167,843.31194")'
        # astropy_region = pyregion.parse(region)
        #astropy_region=ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[0])
        #print(astropy_region)
         
        #List all regions that we have created
        #n_objects = len(self.canvas.objects)
        #for i_obj in range(n_objects):
        #   astropy_region=ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[i_obj])
        #   print(astropy_region) 
           
        #create a list of astropy regions, so we export a .reg file
        #first put the initial region in square brackets, argument of Regions to initiate the list
        RRR=Regions([ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[0])])
        #then append to the list adding all other regions
        for i_obj in range(1,len(self.canvas.objects)):
           RRR.append(ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[i_obj]))
           print(RRR) 
 
        #write the regions to file
        #this does not seem to work...
        RRR.write('/Users/SAMOS_dev/Desktop/new_regions.reg', format='ds9',overwrite=True)
       
        #reading back the ds9 regions in ginga
        pyregions = Regions.read('/Users/SAMOS_dev/Desktop/new_regions.reg', format='ds9')
        n_regions = len(pyregions)
        for i in range(n_regions):
            pyregion = pyregions[i]
            pyregion.width=7
            pyregion.width=3
            ap_region.add_region(self.canvas,pyregion)

        print("yay!")            
        """
        #Export all Ginga objects to Astropy region
        #1. list of ginga objects
        objects = CM.CompoundMixin.get_objects(self.canvas)
        counter = 0
        for obj in objects:
            if counter == 0:
                astropy_regions=[g2r(obj)]  #here we create the first astropy region and the Regions list []
            else:
                astropy_regions.append(g2r(obj)) #will with the other slits 
            counter += 1
        regs = Regions(astropy_regions)     #convert to astropy-Regions
        regs.write('my_regions.reg',overwrite=True)   #write to file
        
        #2, Extract the slits and convert pixel->DMD values
        
        from SAMOS_DMD_dev.Class_DMD_dev import DigitalMicroMirrorDevice
        dmd = DigitalMicroMirrorDevice()#config_id='pass') 
        dmd.initialize()
        dmd._open()
        
        #create initial DMD slit mask
        slit_shape = np.ones((1080,2048)) # This is the size of the DC2K
        
        regions = Regions.read('my_regions.reg')

        from SAMOS_DMD_dev.CONVERT.CONVERT_class import CONVERT 
        convert = CONVERT()

        for i in range(len(regions)):
            reg = regions[i]
            corners = reg.corners
            #convert CCD corners to DMD corners here
            #TBD
            #dmd_corners=[] 
            #for j in range(len(corners)):
            x1,y1 = convert.CCD2DMD(corners[0][0], corners[0][1])
            x1,y1 = int(np.floor(x1)), int(np.floor(y1))
            x2,y2 = convert.CCD2DMD(corners[2][0], corners[2][1])
            x2,y2 = int(np.ceil(x2)), int(np.ceil(y2))
            #dmd_corners[:][1] = corners[:][1]+500
            ####   
            #x1 = round(dmd_corners[0][0])
            #y1 = round(dmd_corners[0][1])+400
            #x2 = round(dmd_corners[2][0])
            #y2 = round(dmd_corners[2][1])+400
        #3 load the slit pattern   
            slit_shape[x1:x2,y1:y2]=0
        dmd.apply_shape(slit_shape)  
        #dmd.apply_invert()   

        
        print("check")
        

    def cursor_cb(self, viewer, button, data_x, data_y):
        """This gets called when the data position relative to the cursor
        changes.
        """
        # Get the value under the data coordinates
        try:
            # We report the value across the pixel, even though the coords
            # change halfway across the pixel
            value = viewer.get_data(int(data_x + viewer.data_off),
                                    int(data_y + viewer.data_off))

        except Exception:
            value = None

        fits_x, fits_y = data_x + 1, data_y + 1

        # Calculate WCS RA
        try:
            # NOTE: image function operates on DATA space coords
            image = viewer.get_image()
            if image is None:
                # No image loaded
                return
            ra_txt, dec_txt = image.pixtoradec(fits_x, fits_y,
                                               format='str', coords='fits')
            self.ra_center, self.dec_center = image.pixtoradec(528, 516,
                                               format='str', coords='fits')

        except Exception as e:
            #self.logger.warning("Bad coordinate conversion: %s" % (
            #    str(e)))
            ra_txt = 'BAD WCS'
            dec_txt = 'BAD WCS'

        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (
            ra_txt, dec_txt, fits_x, fits_y, value)
        self.readout.config(text=text)

    def quit(self, root):
        root.destroy()
        return True

######
    def set_mode_cb(self):
        mode = self.setChecked.get()
#        self.logger.info("canvas mode changed (%s) %s" % (mode))
        self.logger.info("canvas mode changed (%s)" % (mode))
        self.canvas.set_draw_mode(mode)

    def draw_cb(self, canvas, tag):
        obj = canvas.get_object_by_tag(tag)
        obj.add_callback('pick-down', self.pick_cb, 'down')
        obj.add_callback('pick-up', self.pick_cb, 'up')
        obj.add_callback('pick-move', self.pick_cb, 'move')
        obj.add_callback('pick-hover', self.pick_cb, 'hover')
        obj.add_callback('pick-enter', self.pick_cb, 'enter')
        obj.add_callback('pick-leave', self.pick_cb, 'leave')
        obj.add_callback('pick-key', self.pick_cb, 'key')
        obj.pickable = True
        obj.add_callback('edited', self.edit_cb)
        kind = self.wdrawtype.get()
        if self.vslit.get() != 0 and kind == 'point':
            true_kind='Slit'
            print("It is a slit")
            print("Handle the rectangle as a slit")
            self.slit_handler(obj)    
        
    def slit_handler(self, point):
        print('ready to associate a slit to ')
        print(point)
        img_data = self.AstroImage.get_data()
        #create box
        x_c = point.points[0][0]-1#really needed?
        y_c = point.points[0][1]-1
        #create area to search, using astropy instead of ginga (still unclear how you do it with ginga)
        r = regions.RectanglePixelRegion(center=regions.PixCoord(x=round(x_c), y=round(y_c)),
                                        width=10, height=10,
                                        angle = 0*u.deg)
        # and we convert it to ginga...
        obj = r2g(r)
        #this retuns a Box object 
        self.canvas.add(obj)
        print("check")
        data_box = self.AstroImage.cutout_shape(obj)
        
  #      obj = self.canvas.get_draw_class('rectangle')
  #      obj(x1=x_c-20,y1=y_c-20,x2=x_c+20,y2=y_c+20,
  #                      width=100,
  #                      height=30,
  #                      angle = 0*u.deg)
  #      data_box = self.img.cutout_shape(obj)
        peaks = iq.find_bright_peaks(data_box)
        print(peaks[:20])  # subarea coordinates
        x1=obj.x-obj.xradius
        y1=obj.y-obj.yradius
        px,py=round(peaks[0][0]+x1),round(peaks[0][1]+y1)
        print('peak found at: ', px,py)   #image coordinates
        print('with counts: ',img_data[px,py]) #actual counts
        # evaluate peaks to get FWHM, center of each peak, etc.
        objs = iq.evaluate_peaks(peaks, data_box)       
        #from ginga.readthedocs.io
        """
        Each result contains the following keys:

           * ``objx``, ``objy``: Fitted centroid from :meth:`get_fwhm`.
           * ``pos``: A measure of distance from the center of the image.
           * ``oid_x``, ``oid_y``: Center-of-mass centroid from :meth:`centroid`.
           * ``fwhm_x``, ``fwhm_y``: Fitted FWHM from :meth:`get_fwhm`.
           * ``fwhm``: Overall measure of fwhm as a single value.
           * ``fwhm_radius``: Input FWHM radius.
           * ``brightness``: Average peak value based on :meth:`get_fwhm` fits.
           * ``elipse``: A measure of ellipticity.
           * ``x``, ``y``: Input indices of the peak.
           * ``skylevel``: Sky level estimated from median of data array and
             ``skylevel_magnification`` and ``skylevel_offset`` attributes.
           * ``background``: Median of the input array.
           * ``ensquared_energy_fn``: Function of ensquared energy for different pixel radii.
           * ``encircled_energy_fn``: Function of encircled energy for different pixel radii.

        """
        print('full evaluation: ',objs)
        print('fitted centroid: ', objs[0].objx,objs[0].objy) 
        print('FWHM: ', objs[0].fwhm) 
        print('peak value: ',objs[0].brightness)
        print('sky level: ',objs[0].skylevel)
        print('median of area: ',objs[0].background)
        print("the four vertex of the rectangle are, in pixel coord:")
        x1, y1, x2, y2 = obj.get_llur()
        print("the RADEC of the fitted centroid are, in decimal degrees:")
        print(self.AstroImage.pixtoradec(objs[0].objx,objs[0].objy))
        slit_box = self.canvas.get_draw_class('rectangle')
        slit_h=3
        slit_w=7
        self.canvas.add(slit_box(x1=objs[0].objx+x1-slit_w,y1=objs[0].objy+y1-slit_h,x2=objs[0].objx+x1+slit_w,y2=objs[0].objy+y1+slit_h,
                        width=100,
                        height=30,
                        angle = 0*u.deg))
        print("slit added")
        self.cleanup_kind('point')
        self.cleanup_kind('box')


    def pick_cb(self, obj, canvas, event, pt, ptype):
        self.logger.info("pick event '%s' with obj %s at (%.2f, %.2f)" % (
            ptype, obj.kind, pt[0], pt[1]))
        return True
    
    def edit_cb(self, obj):
        self.logger.info("object %s has been edited" % (obj.kind))
        return True

    def cleanup_kind(self,kind):
        #check that we have created a compostition of objects:
        from ginga.canvas import CompoundMixin as CM
        CM.CompoundMixin.is_compound(self.canvas.objects)     # True

        #we can find out what are the "points" objects
        #points = CM.CompoundMixin.get_objects_by_kind(self.canvas,'point')
        found = CM.CompoundMixin.get_objects_by_kind(self.canvas,str(kind))
        list_found=list(found)
        CM.CompoundMixin.delete_objects(self.canvas,list_found)
        self.canvas.objects   #check that the points are gone

    def push_objects_to_slits(self):
        #1) print all the objects as a astropy region file
        #2) edit the file into a dmd file
        #3) load the dmd file
        print("check")





######
    def donothing(self):
        pass

     
######
    def load_Astrometry(self):
        #=> send center and list coodinates to Astrometry, and start Astrometry!
        Astrometry().receive_radec([self.ra_center,self.dec_center],[self.ra_list,self.dec_list],self.xy_list)


######
    def load_Motors_module_GUI(self):
        #calls class "Motors" in tk_class_motors_V1.py; starts the gui and initialize
        SM_GUI()
#        Motors()        
#        pass

######
    def load_DMD_module_GUI(self):
        GUI_DMD()       
        pass

######
    def load_CCD_module_GUI(self):
        GUI_CCD().receive_radec([self.ra_center,self.dec_center],[self.ra_list,self.dec_list],self.xy_list)       
        pass

######
    def load_SOAR_module_GUI(self):
        SOAR()       
        pass

######
    def load_CONFIG_GUI(self):
        print(Config.load_IP_user(self))       
#        pass

######
# from https://sewpy.readthedocs.io/en/latest/
    def run_DaoFind(self):
        from astropy.stats import sigma_clipped_stats
        from astropy.io import fits
        self.fullpath_FITSfilename
        import astropy.wcs as wcs
        ### here is the daophot part of the procedure
        hdu = fits.open(self.fullpath_FITSfilename, logger=self.logger)

        ### read the wcs to get radec from the pixels
        ### see https://docs.astropy.org/en/stable/api/astropy.wcs.WCS.html#astropy.wcs.WCS.pixel_to_world_values
        w = wcs.WCS(hdu[('sci',1)].header, hdu)

        data = hdu[0].data
        hdu.close()   #good practice
        
        #1d background estimate
        sigma = float(self.sigma.get())
        print(sigma)
        mean, median, std = sigma_clipped_stats(data, sigma=sigma)
        print((mean, median, std))  
        
        #2d background estimate
        # FROM https://photutils.readthedocs.io/en/stable/background.html
        from astropy.stats import SigmaClip
        from photutils.background import Background2D, MedianBackground
        sigma_clip = SigmaClip(sigma=3.)
        bkg_estimator = MedianBackground()
        bkg = Background2D(data, (50, 50), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
        median = bkg.background    
        import matplotlib.pyplot as plt
        plt.imshow(bkg.background, origin='lower', cmap='Greys_r', interpolation='nearest')
        
        
        from photutils.detection import DAOStarFinder
        daofind = DAOStarFinder(fwhm=3.0, threshold=3.*std)  
        sources = daofind(data - median)  
        for col in sources.colnames:  
            sources[col].info.format = '%.8g'  # for consistent table output
        print(sources)  
        
# =============================================================================
#         self.display_Daofind(sources)
# =============================================================================
#
        #### back to ginga
        self.fitsimage.set_image(self.AstroImage)
            # passes the image to the viewer through the set_image() method

#        image = load_data(self.fullpath_FITSfilename, logger=self.logger)
        viewer=self.fitsimage#.set_image(image)   #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas = viewer.get_private_canvas() #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas.delete_all_objects(redraw=True)
        canvas.show_pan_mark(True)
        x = sources['xcentroid']
        y = sources['ycentroid']
        
        ### get radec
        ### see https://docs.astropy.org/en/stable/api/astropy.wcs.WCS.html#astropy.wcs.WCS.pixel_to_world_values
        self.ra_list, self.dec_list = w.all_pix2world(x, y, 1)  # we send this to astrometry for cross-matching sources
        self.xy_list = (x,y)   # we send this to astrometry to build the new wcs
        #

        tag = '_$pan_mark'
        radius = 10
        color='green'
#        canvas = viewer.get_private_canvas()
#        viewer.initialize_private_canvas(canvas)
#        mark = canvas.get_object_by_tag(tag)
#        mark.color = color  
        Point = canvas.get_draw_class('point')
 #       canvas.set.drawtype('cross',color='green')
#        self.canvas.redraw(whence=3)
        i=0
        for i in range(len(x)):
 #           x[0]=886
#            y[0]=938
#            canvas.add(Point(x[i]/2.-258, y[i]/2-264, radius, style='plus', color=color,                             
#            canvas.add(Point( (x[i]/2.-264)*1.01, (y[i]/2-258)*1.01, radius, style='plus', color=color,                             
#            canvas.add(Point( (x[i]/2.-264.5), (y[i]/2-258.5), radius, style='plus', color=color,                             
            canvas.add(Point( (x[i]-526)/2., (y[i]-514)/2., radius, style='plus', color=color,                             
                             coord='cartesian'),
                       redraw=True)#False)
            print(x[i], y[i],x[i]/2.-264, y[i]/2.-258)
#            print(x[i], y[i],x[i]/2.-258, y[i]/2.2-258)
        canvas.update_canvas(whence=3)
        print('done')

    def show_slits(self):
        #### back to ginga
        self.fitsimage.set_image(self.AstroImage)
            # passes the image to the viewer through the set_image() method

#        image = load_data(self.fullpath_FITSfilename, logger=self.logger)
        viewer=self.fitsimage#.set_image(image)   #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas = viewer.get_private_canvas() #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas.delete_all_objects(redraw=True)
        canvas.show_pan_mark(True)
        x = [10,110,210,310,410,510,610,710]#sources['xcentroid']
        y = [10,110,210,310,410,510,610,710]#)sources['ycentroid']
        Dx = [7,7,  7,  7,  7,  7,  7,  7]
        Dy = [3,3,  3,  3,  3,  3,  3,  3]
        tag = '_$pan_mark'
        radius = 1
        color='green'
#        canvas = viewer.get_private_canvas()
#        viewer.initialize_private_canvas(canvas)
#        mark = canvas.get_object_by_tag(tag)
#        mark.color = color  
        Point = canvas.get_draw_class('point')
 #       canvas.set.drawtype('cross',color='green')
#        self.canvas.redraw(whence=3)
        i=0
        for i in range(len(x)):
            x[0]=886
            y[0]=938
#            canvas.add(Point(x[i]/2.-258, y[i]/2-264, radius, style='plus', color=color,                             
#            canvas.add(Point( (x[i]/2.-264)*1.01, (y[i]/2-258)*1.01, radius, style='plus', color=color,                             
#            canvas.add(Point( (x[i]/2.-264.5), (y[i]/2-258.5), radius, style='plus', color=color,                             
            for ix in range(Dx[i]):
                for iy in range(Dy[i]):
                    xp = ((x[i] + (ix-int(Dx[i]/2)))-526)/2.
                    yp = ((y[i] + (iy-int(Dy[i]/2)))-514)/2.
#                    canvas.add(Point( (x[i]-526)/2., (y[i]-514)/2., radius, style='square', color='black',                             
                    canvas.add(Point( xp, yp, radius, style='square', color='black',                             
                             coord='cartesian'),
                       redraw=True)#False)
            print(x[i], y[i],x[i]/2.-264, y[i]/2.-258)
#            print(x[i], y[i],x[i]/2.-258, y[i]/2.2-258)
        canvas.update_canvas(whence=3)
        print('done')
    


######
def main(options, args):

    logger = log.get_logger("example2", options=options)

    fv = SAMOS_Main(logger)
    top = fv.get_widget()

    if len(args) > 0:
        fv.load_file(args[0])

    top.mainloop()


if __name__ == "__main__":

    # Parse command line options
    from argparse import ArgumentParser

    argprs = ArgumentParser()

    argprs.add_argument("--debug", dest="debug", default=False,
                        action="store_true",
                        help="Enter the pdb debugger on main()")
    argprs.add_argument("--profile", dest="profile", action="store_true",
                        default=False,
                        help="Run the profiler on main()")
    log.addlogopts(argprs)

    (options, args) = argprs.parse_known_args(sys.argv[1:])

    # Are we debugging this?
    if options.debug:
        import pdb

        pdb.run('main(options, args)')

    # Are we profiling this?
    elif options.profile:
        import profile

       # print("%s profile:" % sys.argv[0])
        profile.run('main(options, args)')

    else:
        main(options, args)
        

# END
