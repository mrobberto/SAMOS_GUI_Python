#! /usr/bin/env python
#
# example2_tk.py -- Simple, configurable FITS viewer.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import sys
import os
import threading


from ginga.tkw.ImageViewTk import ImageViewCanvas
from ginga.misc import log
from ginga.util.loader import load_data

import tkinter as tk
from tkinter.filedialog import askopenfilename

#import sewpy   #to run sextractor wrapper

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'
# =============================================================================
# 
# from Astrometry import tk_class_astrometry
# Astrometry = tk_class_astrometry
# 
# Astrometry.return_from_astrometry()
# 
# =============================================================================
os.sys.path.append(".")
os.sys.path.append("./Astrometry")


from tk_class_astrometry_V4 import Astrometry
#from ginga.misc import widgets 

class SAMOS_Main(object):

    def __init__(self, logger):

        self.logger = logger
        self.drawcolors = ['white', 'black', 'red', 'yellow', 'blue', 'green']

        root = tk.Tk()
        root.title("SAMOS")
       
        root.geometry("1000x800")   
        
        #root.set_border_width(2)
        #root.connect("delete_event", lambda w, e: self.quit(w))
        self.root = root

        self.frame0l = tk.Frame(root,background="cyan")#, width=400, height=800)
        self.frame0l.place(x=0, y=0, anchor="nw", width=220, height=140)
        
# =============================================================================
#         
#  #    FILTER STATUS Label Frame
#         
# =============================================================================
        labelframe_Filters =  tk.LabelFrame(self.frame0l, text="Filter Status", font=("Arial", 24))
        labelframe_Filters.pack(fill="both", expand="yes")
         

        label_FW1 =  tk.Label(labelframe_Filters, text="Filter Wheel 1")
        label_FW1.place(x=4,y=10)
        entry_FW1 = tk.Entry(labelframe_Filters, width=11,  bd =3)
        entry_FW1.place(x=100, y=10)
# =============================================================================
#         label_FW1_template =  tk.Label(labelframe_Filters, text="HH:MM:SS.xx")
#         label_FW1_template.place(x=200,y=10)
#         
# =============================================================================
        label_FW2 =  tk.Label(labelframe_Filters, text="Filter Wheel 2")
        label_FW2.place(x=4,y=40)
        entry_FW2 = tk.Entry(labelframe_Filters, width=11, bd =3)
        entry_FW2.place(x=100, y=40)
# =============================================================================
#         label_FW1_template =  tk.Label(labelframe_Filters, text="2213DD:MM:SS.xx")
#         label_FW1_template.place(x=200,y=10)
#         
# =============================================================================
        button_HomeFW1 =  tk.Button(labelframe_Filters, text="Home FW1", bd=3)
        button_HomeFW1.place(x=0,y=70)
        button_HomeFW2 =  tk.Button(labelframe_Filters, text="Home FW2", bd=3)
        button_HomeFW2.place(x=105,y=70)

# =============================================================================
#         
#  #    GRISM STATUS Label Frame
#         
# =============================================================================
        self.frame1l = tk.Frame(root,background="cyan")#, width=400, height=800)
        self.frame1l.place(x=0, y=150, anchor="nw", width=220, height=100)

        labelframe_Grating =  tk.LabelFrame(self.frame1l, text="Grism Status", font=("Arial", 24))
        labelframe_Grating.pack(fill="both", expand="yes")
         
#      labelframe_Grating.place(x=4, y=10)
         
        # Dropdown menu options
        options = [
            "Low Blue",
            "Low Red",
            "High Blue",
            "High Red"
        ]
        # datatype of menu text
        self.grating = tk.StringVar()
        # initial menu text
        self.grating.set(options[2])
        # Create Dropdown menu
        self.optionmenu_grating = tk.OptionMenu(labelframe_Grating, self.grating, *options)
        self.optionmenu_grating.place(x=4, y=10)

        button_HomeGrating=  tk.Button(labelframe_Grating, text="Home Grating", bd=3)
        button_HomeGrating.place(x=0,y=35)

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
#  #    FITS file
#         
# =============================================================================
        self.frame_FITSmanager = tk.Frame(root,background="pink")#, width=400, height=800)
        self.frame_FITSmanager.place(x=0, y=450, anchor="nw", width=220, height=200)

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
        button_FITS_Load.place(x=0,y=20)
        
        self.stop_it = 0
        button_FITS_start =  tk.Button(labelframe_FITSmanager, text="FITS start", bd=3, 
                                           command=self.check_for_file_existence)#start_the_loop)
        button_FITS_start.place(x=0,y=50)

# =============================================================================
        button_Astrometry =  tk.Button(labelframe_FITSmanager, text="Astrometry", bd=3, 
#                                            command=Astrometry)
                                            command=self.load_Astrometry)
        button_Astrometry.place(x=0,y=80)

# 
# =============================================================================
        button_run_Sextractor =  tk.Button(labelframe_FITSmanager, text="run DaoFind", bd=3, 
                                            command=self.run_DaoFind)
        button_run_Sextractor.place(x=0,y=110)
        label_sigma =  tk.Label(labelframe_FITSmanager, text="sigma")
        label_sigma.place(x=120,y=112)
        self.sigma=tk.StringVar()
        entry_sigma = tk.Entry(labelframe_FITSmanager, width=3,  bd =3, textvariable=self.sigma)
        entry_sigma.place(x=160, y=110)
        self.sigma.set('50')


# 
# =============================================================================


        vbox = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
#        vbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        vbox.pack(side=tk.TOP)
        vbox.place(x=230, y=0, anchor="nw")#, width=500, height=800)
        self.vb = vbox
# =============================================================================
# #
# # Menu Bar goes into the mac header...
# #
# =============================================================================
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Setup", command=self.donothing)
        filemenu.add_command(label="Acquisition", command=self.donothing)
        filemenu.add_command(label="Calibration", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)                

        canvas = tk.Canvas(vbox, bg="grey", height=516, width=528)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        fi = ImageViewCanvas(logger) #=> ImageViewTk -- a backend for Ginga using a Tk canvas widget
        fi.set_widget(canvas)  #=> Call this method with the Tkinter canvas that will be used for the display.
        #fi.set_redraw_lag(0.0)
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        fi.enable_draw(False)
        # tk seems to not take focus with a click
        fi.set_enter_focus(True)
        fi.set_callback('cursor-changed', self.cursor_cb)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_set_active(True)
        fi.show_pan_mark(True)
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        # canvas that we will draw on
        DrawingCanvas = fi.getDrawClass('drawingcanvas')
        canvas2 = DrawingCanvas()
        canvas2.enable_draw(True)
        #canvas.enable_edit(True)
        canvas2.set_drawtype('rectangle', color='blue')
        canvas2.set_surface(fi)
        self.canvas2 = canvas2
        # add canvas to view
        fi.add(canvas2)
        canvas2.ui_set_active(True)

        fi.configure(516, 528) #height, width

        hbox = tk.Frame(root)
        hbox.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.readout = tk.Label(root, text='')
        self.readout.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.drawtypes = fi.get_drawtypes()
        ## wdrawtype = ttk.Combobox(root, values=self.drawtypes,
        ##                          command=self.set_drawparams)
        ## index = self.drawtypes.index('ruler')
        ## wdrawtype.current(index)
        wdrawtype = tk.Entry(hbox, width=12)
        wdrawtype.insert(0, 'rectangle')
        wdrawtype.bind("<Return>", self.set_drawparams)
        self.wdrawtype = wdrawtype

        # wdrawcolor = ttk.Combobox(root, values=self.drawcolors,
        #                           command=self.set_drawparams)
        # index = self.drawcolors.index('blue')
        # wdrawcolor.current(index)
        wdrawcolor = tk.Entry(hbox, width=12)
        wdrawcolor.insert(0, 'blue')
        wdrawcolor.bind("<Return>", self.set_drawparams)
        self.wdrawcolor = wdrawcolor

        self.vfill = tk.IntVar()
        wfill = tk.Checkbutton(hbox, text="Fill", variable=self.vfill)
        self.wfill = wfill

        walpha = tk.Entry(hbox, width=12)
        walpha.insert(0, '1.0')
        walpha.bind("<Return>", self.set_drawparams)
        self.walpha = walpha

        wclear = tk.Button(hbox, text="Clear Canvas",
                                command=self.clear_canvas)
        wopen = tk.Button(hbox, text="Open File",
                               command=self.open_file)
        wquit = tk.Button(hbox, text="Quit",
                               command=lambda: self.quit(root))
        for w in (wquit, wclear, walpha, tk.Label(hbox, text='Alpha:'),
                  wfill, wdrawcolor, wdrawtype, wopen):
            w.pack(side=tk.RIGHT)

# =============================================================================
#     def open_Astrometry(self):
#         btn = tk.Button(master,
#              text ="Click to open a new window",
#              command = openNewWindow)
#         btn.pack(pady = 10)
#         return self.Astrometry(master)
# =============================================================================

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

    def clear_canvas(self):
        self.canvas.deleteAllObjects()

    def load_last_file(self):
        FITSfiledir = './fits_image/'
        self.fullpath_FITSfilename = FITSfiledir + (os.listdir(FITSfiledir))[0] 
            # './fits_image/cutout_rebined_resized.fits'
        image = load_data(self.fullpath_FITSfilename, logger=self.logger)
            # AstroImage object of ginga.AstroImage module
        
        self.AstroImage = image    #make the AstroImage available
        self.fitsimage.set_image(image)
            # passes the image to the viewer through the set_image() method
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
        image = load_data(self.fullpath_FITSfilename, logger=self.logger)
        self.canvas.set_image(image)
        self.root.title(self.fullpath_FITSfilename)

    def open_file(self):
        filename = askopenfilename(filetypes=[("allfiles", "*"),
                                              ("fitsfiles", "*.fits")])
        self.load_file(filename)

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
            self.logger.warning("Bad coordinate conversion: %s" % (
                str(e)))
            ra_txt = 'BAD WCS'
            dec_txt = 'BAD WCS'

        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (
            ra_txt, dec_txt, fits_x, fits_y, value)
        self.readout.config(text=text)

    def quit(self, root):
        root.destroy()
        return True

######
    def donothing(self):
        x = 0
       
######
    def load_Astrometry(self):
#        print(Astrometry().string_RA.get())
        Astrometry().receive_radec([self.ra_center,self.dec_center])
        
#        self.ra_center, self.dec_center))

######
# from https://sewpy.readthedocs.io/en/latest/
    def run_DaoFind(self):
        from astropy.stats import sigma_clipped_stats
        from astropy.io import fits
        self.fullpath_FITSfilename
        ### here is the daophot part of the procedure
        hdu = fits.open(self.fullpath_FITSfilename, logger=self.logger)
        data = hdu[0].data
        sigma = float(self.sigma.get())
        print(sigma)
        mean, median, std = sigma_clipped_stats(data, sigma=sigma)
        print((mean, median, std))  
        from photutils.detection import DAOStarFinder
        daofind = DAOStarFinder(fwhm=3.0, threshold=3.*std)  
        sources = daofind(data - median)  
        for col in sources.colnames:  
            sources[col].info.format = '%.8g'  # for consistent table output
        print(sources)  
        #
# =============================================================================
#         self.display_Daofind(sources)
# =============================================================================
#
        #### back to ginga
        self.fitsimage.set_image(self.AstroImage)
            # passes the image to the viewer through the set_image() method

#        image = load_data(self.fullpath_FITSfilename, logger=self.logger)
        viewer=self.fitsimage#.set_image(image)   #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas2 = viewer.get_private_canvas() #ImageViewCanvas object of ginga.tkw.ImageViewTk module
        canvas2.delete_all_objects(redraw=True)
        canvas2.show_pan_mark(True)
        x = sources['xcentroid']
        y = sources['ycentroid']
        tag = '_$pan_mark'
        radius = 10
        color='green'
#        canvas2 = viewer.get_private_canvas()
#        viewer.initialize_private_canvas(canvas)
#        mark = canvas2.get_object_by_tag(tag)
#        mark.color = color  
        Point = canvas2.get_draw_class('point')
 #       canvas2.set.drawtype('cross',color='green')
#        self.canvas.redraw(whence=3)
        i=0
        for i in range(len(x)):
            x[0]=1055
            y[0]=1031
            canvas2.add(Point(x[i]/2.-264, y[i]/2-258, radius, style='plus', color=color,                             
#            canvas2.add((Point( (x[i]-528)/2., (y[i]-516)/2., radius, style='plus', color=color,                             
                             coord='cartesian'),
                       redraw=True)#False)
            print(x[i], y[i],x[i]/2.-264, y[i]/2.2-258)
        canvas2.update_canvas(whence=3)
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

        print("%s profile:" % sys.argv[0])
        profile.run('main(options, args)')

    else:
        main(options, args)
        

# END
