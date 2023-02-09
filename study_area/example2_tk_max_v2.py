#! /usr/bin/env python
#
# example2_tk.py -- Simple, configurable FITS viewer.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import sys
sys.path.append('/opt/anaconda3/envs/samos_env/lib/python3.10/site-packages')


from ginga.tkw.ImageViewTk import CanvasView
from ginga.misc import log
from ginga.canvas.CanvasObject import get_canvas_types
from ginga.util.loader import load_data
from ginga import colors

from ginga.util.ap_region import astropy_region_to_ginga_canvas_object as r2g
from ginga.util.ap_region import ginga_canvas_object_to_astropy_region as g2r


import tkinter as tk
from tkinter import ttk

from tkinter.filedialog import askopenfilename

import regions
from astropy import units as u

from ginga.util import iqcalc
iq = iqcalc.IQCalc()


STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'


class FitsViewer(object):

    def __init__(self, logger):

        self.logger = logger
        self.drawcolors = colors.get_colors()
#        self.drawcolors = ['white', 'black', 'red', 'yellow', 'blue', 'green']
        self.dc = get_canvas_types()

        root = tk.Tk()
        root.title("ImageViewTk Example")
        #root.set_border_width(2)
        #root.connect("delete_event", lambda w, e: self.quit(w))
        self.root = root

        #self.select = FileSelection.FileSelection()

        vbox = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
        vbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(vbox, bg="grey", height=512, width=512)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        fi = CanvasView(logger)
        fi.set_widget(canvas)
        #fi.set_redraw_lag(0.0)
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        # tk seems to not take focus with a click
        fi.set_enter_focus(True)
        fi.set_callback('cursor-changed', self.cursor_cb)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_set_active(True)
        fi.show_pan_mark(True)
        fi.show_mode_indicator(True, corner='ur')
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        # canvas that we will draw on
        canvas = self.dc.DrawingCanvas()
        canvas.enable_draw(True)
        canvas.enable_edit(True)
        canvas.set_drawtype('point', color='red')
        canvas.register_for_cursor_drawing(fi)
        canvas.add_callback('draw-event', self.draw_cb)
        canvas.set_draw_mode('draw')
        canvas.set_surface(fi)
        canvas.ui_set_active(True)
        self.canvas = canvas
                
        # add our new canvas to viewers default canvas
        fi.get_canvas().add(canvas)

        self.drawtypes = canvas.get_drawtypes()
        self.drawtypes.sort()

        
        # add little mode indicator that shows keyboard modal states
        fi.show_mode_indicator(True, corner='ur')

        fi.configure(512, 512)

        hbox = tk.Frame(root)
        hbox.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.readout = tk.Label(root, text='')
        self.readout.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.drawtypes = self.canvas.get_drawtypes()
        
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


        '''
        # Combobox creation
        n = tk.StringVar()
        wdrawtype = ttk.Combobox(hbox, values=self.drawtypes)
        #wdrawtype = ttk.Combobox(root, values=self.drawtypes, 
        #    command=self.set_drawparams)
        index = self.drawtypes.index('rectangle')
        wdrawtype.current(index)
        wdrawtype.bind("<<ComboboxSelected>>", self.set_drawparams)
        #wdrawtype = tk.Entry(hbox, width=12)
        #wdrawtype.insert(0, 'rectangle')
        #wdrawtype.bind("<Return>", self.set_drawparams)
        self.wdrawtype = wdrawtype
        '''

        wdrawcolor = ttk.Combobox(hbox, values=self.drawcolors)
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
        
#        str_walpha = tk.StringVar() 
#        walpha_box = ttk.Spinbox(hbox,from_=0,to=1,increment=0.1,
#                             width=3,
#                             textvariable = str_walpha)#, command=self.set_drawparams)
#        str_walpha.set(1.0) 
#    #      walpha.setRange(0.0, 1.0)
#  #      walpha.setSingleStep(0.1)
#  #      walpha.setValue(1.0)
#        #walpha.valueChanged.connect(self.set_drawparams)
#        self.walpha = walpha_box
#        print(self.walpha.get())


        wrun = tk.Button(hbox, text="Run code",
                                command=self.run_code)

        wclear = tk.Button(hbox, text="Clear Canvas",
                                command=self.clear_canvas)
        wsave = tk.Button(hbox, text="Save Canvas",
                                command=self.save_canvas)
        wopen = tk.Button(hbox, text="Open File",
                               command=self.open_file)
        wquit = tk.Button(hbox, text="Quit",
                               command=lambda: self.quit(root))

        #place everything on a row, right to left
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
        
  
###------


    def get_widget(self):
        return self.root

    def set_drawparams_max(self):
        pass
    
    def set_drawparams(self, evt):
#    def set_drawparams(self):
        kind = self.wdrawtype.get()
#        if self.vslit != 0 and kind == 'point':
#            true_kind='Slit'
#            print("It is a slit")
#            print("Handle the rectangle as a slit")
#            self.slit_handler
            
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
        self.canvas.delete_all_objects()

    def load_file(self, filepath):
        image = load_data(filepath, logger=self.logger)
        self.fitsimage.set_image(image)
        self.root.title(filepath)
        
        #THIS ALLOWS TO USE THE DATA PLANE ACROSS THE APPLICATION
        self.img = image

    def open_file(self):
        filename = askopenfilename(filetypes=[("allfiles", "*"),
                                              ("fitsfiles", "*.fits")])
        self.load_file(filename)
        
        
    def run_code(self):
        # Find approximate bright peaks in a sub-area
        from ginga.util import iqcalc
        iq = iqcalc.IQCalc()
    
        r = self.canvas.objects[0]
        img_data = self.img.get_data()
        data_box = self.img.cutout_shape(r)
        """
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
        """
        r_all = self.canvas.objects[:]
        print(r_all)
        
        #r_all is a CompountMixing object, see class ginga.canvas.CompoundMixin.CompoundMixin
        #check:
        from ginga.canvas import CompoundMixin as CM
        CM.CompoundMixin.is_compound(self.canvas.objects)     # True
        
        #we can find out what are the "points" objects
        points = CM.CompoundMixin.get_objects_by_kind(self.canvas,'point')
        print(list(points))
        
        """
        #we can remove what we don't like, e.g. points
        points = CM.CompoundMixin.get_objects_by_kind(self.canvas,'point')
        list_point=list(points)
        CM.CompoundMixin.delete_objects(self.canvas,list_point)
        self.canvas.objects   #check that the points are gone
        """
        
        #we can remove both points and boxes
        points = CM.CompoundMixin.get_objects_by_kinds(self.canvas,['point','box'])
        list_points=list(points)
        CM.CompoundMixin.delete_objects(self.canvas,list_points)
        self.canvas.objects   #check that the points are gone
        
        
        from ginga.util import ap_region

        from regions import Regions
        # region = 'fk5;circle(290.96388,14.019167,843.31194")'
        # astropy_region = pyregion.parse(region)
        astropy_region=ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[0])
        print(astropy_region)
         
        #List all regions that we have created
        n_objects = len(self.canvas.objects)
        for i_obj in range(n_objects):
           astropy_region=ap_region.ginga_canvas_object_to_astropy_region(self.canvas.objects[i_obj])
           print(astropy_region) 
           
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
            pyregion.width=100
            ap_region.add_region(self.canvas,pyregion)

        print("yay!")            
       
            

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
        except Exception as e:
            self.logger.warning("Bad coordinate conversion: %s" % (
                str(e)))
            ra_txt = 'BAD WCS'
            dec_txt = 'BAD WCS'

        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (
            ra_txt, dec_txt, fits_x, fits_y, value)
        self.readout.config(text=text)
        
        
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
        img_data = self.img.get_data()
        #create box
        x_c = point.points[0][0]-1#really needed?
        y_c = point.points[0][1]-1
        #create area to search, using astropy instead of ginga (still unclear how you do it with ginga)
        r = regions.RectanglePixelRegion(center=regions.PixCoord(x=x_c, y=y_c),
                                        width=15, height=15,
                                        angle = 0*u.deg)
        # and we convert it to ginga...
        obj = r2g(r)
        #this retuns a Box object 
        self.canvas.add(obj)
        print("check")
        data_box = self.img.cutout_shape(obj)
        
#        obj = self.canvas.get_draw_class('rectangle')
#        obj(x1=x_c-20,y1=y_c-20,x2=x_c+20,y2=y_c+20,
#                        width=100,
#                        height=30,
#                        angle = 0*u.deg)
#        data_box = self.img.cutout_shape(obj)
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
        print(self.img.pixtoradec(objs[0].objx,objs[0].objy))
        slit_box = self.canvas.get_draw_class('rectangle')
        slit_h=3
        slit_w=7
        self.canvas.add(slit_box(x1=objs[0].objx+x1-slit_w,y1=objs[0].objy+y1-slit_h,x2=objs[0].objx+x1+slit_w,y2=objs[0].objy+y1+slit_h,
                        width=100,
                        height=30,
                        angle = 0*u.deg))
        print("check")
        
    def pick_cb(self, obj, canvas, event, pt, ptype):
        self.logger.info("pick event '%s' with obj %s at (%.2f, %.2f)" % (
            ptype, obj.kind, pt[0], pt[1]))
        return True
    
    def edit_cb(self, obj):
        self.logger.info("object %s has been edited" % (obj.kind))
        return True



    def quit(self, root):
        root.destroy()
        return True


def main(options, args):

    logger = log.get_logger("example2", options=options)

    fv = FitsViewer(logger)
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
