#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 10:49:37 2021

@author: robberto
"""
import tkinter as tk
from Class_PCM_module import Class_PCM as PCM
#PCM = Class_PCM_module()


class Motors(tk.Toplevel):     #the Motors class inherits from the tk.Toplevel widget
#    def __init__(self, master=None):
    def __init__(self, master=None):  #__init__ constructor method. 
        #>>> AM = Motors(master) would be an instance of the class Motors that you can call with its functions, e.g.
        #>>> AM.show_Simbad()
    
#        logger = log.get_logger("example1", log_stderr=True)
#        self.logger = logger
        
        super().__init__(master = master) 
        #super() recalls and includes the __init__() of the master class (tk.Topelevel), so one can use that stuff there without copying the code.

        self.title("Motor Setup")
        self.geometry("900x600")
        label = tk.Label(self, text ="This is the Motors Window")
        label.pack()
                
#        #reference to the master widget, which is the tk window                 
#        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        
        self.params = {'Host': '128.220.146.254', 'Port': 8889}

        #rename for convenience the imported class
#        PCM = Class_PCM_module()
        
#The above is really all we need to do to get a window instance started.
        
    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
 #       self.master.title("IDG - PCM module driver")

        # allowing the widget to take the full space of the root window
        #self.pack(fill=tk.BOTH, expand=1)

        self.Echo_String = tk.StringVar()         
        #self.check_if_power_is_on()  
        self.is_on = False
  
# =============================================================================
#         
#         #Get echo from Server 
# =============================================================================
        Button_Echo_From_Server = tk.Button(self, text="Echo from server",command=self.call_echo_PCM, relief=tk.RAISED)
        # placing the button on my window
        Button_Echo_From_Server.place(x=10,y=10)
        self.Echo_String = tk.StringVar()        
        Label_Echo_Text = tk.Label(self,textvariable=self.Echo_String,width=15,bg='white')
        Label_Echo_Text.place(x=160,y=13)
        
# =============================================================================
#         
#        # Power on/odd 
# =============================================================================
        if self.is_on == False:
            text = "Turn power ON"
            color = "green"
        else: 
            text = "Turn power OFF"
            color = "red"
        self.Button_Power_OnOff = tk.Button(self, text=text,command=self.power_switch, relief=tk.RAISED,fg = color)
        self.Button_Power_OnOff.place(x=10,y=40)

# =============================================================================
#         All port statusPower on/odd 
# =============================================================================
        self.Button_All_Ports_Status = tk.Button(self, text="All ports status",command=self.all_ports_status, relief=tk.RAISED)
        self.Button_All_Ports_Status.place(x=10,y=70)
  
# =============================================================================
#        Initialize
# =============================================================================
        self.Button_Initialize = tk.Button(self, text="Initialize",command=self.initialize, relief=tk.RAISED)
        self.Button_Initialize.place(x=10,y=100)
  
# =============================================================================
#        Query current step counts
# =============================================================================
        self.Button_Initialize =tk.Button(self, text="Current steps",command=self.query_current_step_counts, relief=tk.RAISED)
        self.Button_Initialize.place(x=200,y=100)

# =============================================================================
#       home
# =============================================================================
        self.Button_home = tk.Button(self, text="home",command=self.home, relief=tk.RAISED)
        self.Button_home.place(x=10,y=130)
    
# =============================================================================
#         
#         #Move to step.... 
# =============================================================================
        Button_Move_to_step = tk.Button(self, text="Move to step",command=self.move_to_step, relief=tk.RAISED)
        Button_Move_to_step.place(x=10,y=160)
        self.Target_step = tk.StringVar()        
        Label_Target_step = tk.Entry(self,textvariable=self.Target_step,width=6,bg='white')
        Label_Target_step.place(x=140,y=163)
        Button_Stop = tk.Button(self, text="Stop",command=self.stop, relief=tk.RAISED)
        Button_Stop.place(x=260,y=160)
    
# =============================================================================
#         
#         #Move to filter.... 
# =============================================================================
        filter_options = [
             "A1",
             "A2",
             "A3",
             "A4",
             "A5",
             "A6"
             ]
#        # datatype of menu text
        self.selected_filter = tk.StringVar()
#        # initial menu text
        self.selected_filter.set(filter_options[0])
#        # Create Dropdown menu
        self.menu_filters = tk.OptionMenu(self, self.selected_filter,  *filter_options)
        self.menu_filters.place(x=140, y=193)
        Button_Move_to_filter = tk.Button(self, text="Move to Filter",command=self.move_to_filter, relief=tk.RAISED)
        Button_Move_to_filter.place(x=10,y=190)

# =============================================================================
#         
#         #Enter command
# =============================================================================
        Button_Enter_Command = tk.Button(self, text="Enter Command: ",command=self.enter_command, relief=tk.RAISED)
        Button_Enter_Command.place(x=10,y=220)
        self.Command_string = tk.StringVar()        
        Text_Command_string = tk.Entry(self,textvariable=self.Command_string,width=15,bg='white')
        Text_Command_string.place(x=180,y=222)
        Label_Command_string_header = tk.Label(self,text=" '~@,9600_8N1T2000,'+")
        Label_Command_string_header.place(x=10,y=250)
        Label_Command_string_Example = tk.Label(self,text=" (e.g. '/1e1R\\n)'")
        Label_Command_string_Example.place(x=165,y=250)


# =============================================================================
# 
#         # Exit
# =============================================================================
        quitButton = tk.Button(self, text="Exit",command=self.client_exit)
        quitButton.place(x=280, y=270)


# =============================================================================
#      SHOW SIMBAD IMAGE
# 
# =============================================================================

 

#    
    def return_from_Motors(self):
        return "voila"


    def call_echo_PCM(self):       
        print('echo from server:')
        t = PCM.echo_client(self)
        self.Echo_String.set(t)
        print(t)

    def power_switch(self):     
    # Determine is on or off
        if self.is_on:  #True, power is on => turning off, prepare for turn on agaim
            t=PCM.power_off()
            self.is_on = False
            self.Button_Power_OnOff.config(text="Turn power On",fg = "green")
        else:            
            t=PCM.power_on()
            self.is_on = True
            self.Button_Power_OnOff.config(text="Turn power Off",fg = "red")
        self.Echo_String.set(t)
        print("Power switched to ", t)
    
    def all_ports_status(self):       
        print('all ports status:')
        t = PCM.all_ports_status()
        self.Echo_String.set(t)
        print(t)

    def initialize(self):       
        print('Initialize:')
        t = PCM.initialize_filter_wheel()
        self.Echo_String.set(t)
        print(t)

    def query_current_step_counts(self):       
        print('Current step counts:')
        t = PCM.query_current_step_counts()
        self.Echo_String.set(t)
        print(t)

    def home(self):       
        print('home:')
        t = PCM.home_filter_wheel()
        self.Echo_String.set(t)
        print(t)

    def move_to_step(self):       
        print('moving to step:')
        t = PCM.go_to_step(self.Target_step.get())
        self.Echo_String.set(t)
        print(t)

    def stop(self):       
        print('moving to step:')
        t = PCM.stop_filter_wheel()
        self.Echo_String.set(t)
        print(t)

    def move_to_filter(self):       
        print('moving to filter:') 
        filter = self.selected_filter.get()
        t = PCM.move_filter_wheel(filter)
        self.Echo_String.set(t)
        print(t)
        
    def enter_command(self):       
        print('command entered:') 
        t = PCM.send_command_string(self.Command_string.get()) #conbert StringVar to string
        self.Echo_String.set(t)
        print(t)
        
    def client_exit(self):
        print("destroy")
        root.destroy()  
            
    
 