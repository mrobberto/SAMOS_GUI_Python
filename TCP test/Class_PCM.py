#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 08:11:18 2021

Module to work with the IDG PCM controller and EZHR Stepper module controller:

FOR TESTING TCP COMMUNICATION ON LOCALHOST (see instuction below)
> echo_server() 
> echo_client()

PCM procedures
> PCM_power_on()
> all_port_status()
> initialize_filter_wheel(FW)
> stored_filter_wheel_procedures()
> home_filter_wheel(FW)
> move_filter_wheel(position)
> query_current_step_counts(FW)
> timed_query_current_count_monitor(FW)
> initialize_grism_rails()
> stored_grism_rails_procedures()
> home_grism_rails(GR)
> fast_home_grism_rails(GR)
> move_grism_rails(position)

To use/test
>>> from Class_PCM import Class_PCM
>>> PCM = Class_PCM()
>>> PCM.echo_client()
>>>     Received b'NL11111111'
>>> PCM.params()
>>>     {'Host': '10.0.0.179', 'PORT': 1000}
>>> PCM.params['Host']
@author: m. robberto
"""
# =============================================================================
#
# echo_server
#
# =============================================================================
# 1) open an xterm
# 2) move to the local directory of this file
# 3) only once, create an empty __init__.py file (>touch __init__.py) to
#    to the python interpreter that the developer intends this directory
#     to be an importable package.
#     See https://stackoverflow.com/questions/2349991/how-to-import-other-python-files
# 4) start >python
# 5) import this file: >import PCM
# 6) run this procedure >PCM.echo_server()). The terminal hangs...
# 7) go to the instructions for the following echo_client() procedure)


class Class_PCM():

    def __init__(self):
        self.params = {'Host': '10.0.0.179', 'Port': 1000}

# =============================================================================
#     def echo_server():
#         import socket
#
#         HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#         PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((HOST, PORT))
#             s.listen()
#             conn, addr = s.accept()
#             with conn:
#                 print('Connected by', addr)
#                 while True:
#                     data = conn.recv(1024)
#                     if not data:
#                         break
#                     conn.sendall(data)
#
# =============================================================================

    # =============================================================================
    #
    # echo client()
    #
    # =============================================================================
    # 1) open an(other) xterm
    # 2) move to this local directory
    # 3) start >python
    # 4) import this file: >import PCM
    # 5) run this procedure >PCM.echo_client())
    # 6) the server gives you the anser and closes
    def echo_client(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
        #    s.sendall(b'Hello, world')
        #    s.sendall(b'~Hello, world\n')
            s.sendall(b'~se,all,on\n')
            data = s.recv(1024)

        print('Received', repr(data))

    # =============================================================================
    #
    # PCM_power_on
    #
    # =============================================================================
    def power_on(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # To talk to the motor controller, you will first need to power the controller power port.
    # The command for that is “~se,1,on\n” This means set enable for power port 1 on.
            s.sendall(b'~se,all,on\n')
            data = s.recv(1024)

        print('Received', repr(data))

    # =============================================================================
    #
    # PCM_power_off
    #
    # =============================================================================

    def power_off(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # To talk to the motor controller, you will first need to power the controller power port.
    # The command for that is “~se,1,on\n” This means set enable for power port 1 on.
            s.sendall(b'~se,all,off\n')
            data = s.recv(1024)

        print('Received', repr(data))

    # =============================================================================
    #
    # PCM_all_port_status
    #
    # =============================================================================
    def all_ports_status(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # you can send "~ge,all\n” and it will return the status of all power ports
            s.sendall(b'~ge,all\n')
            data = s.recv(1024)

        print('Received', repr(data))

    # =============================================================================
    #
    # initialize_filter_wheel
    #
    # =============================================================================
    def initialize_filter_wheel(self, FW):
        import socket

    #    assign 0 value to FW just to avoid errors while testing w/o FW in input
#        if FW == None:
#            FW1 = "0"
#            FW2 = "0"

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # Here are filter wheel commands to send to the PCM…. The stored procedures only need to be sent once in the lifetime of the drive… You should have the ability to send these, but will not have to unless we replaced a drive.
    # The operating commands allow you to choose a particular filter by asking the drive to execute a stored procedure. This should be integrated into your code. You also ought to query the wheels to make sure they are where you think they are….
    # Note: all procedures include the command to route the drive packet via the PCM so it should be really simple to integrate.
    # BTW the camera is no facing the filter wheel.
    #
    #
    # FILTER WHEEL STORED PROCEDURES - These need to be sent to the motor controllers the first time they are used… i.e if you replace a motor controller you should reinitialize with these commands…
    # WHEEL 1
    # Initial drive settings (velocity, steps ratio, current), plus homing routine — this runs automatically on power up.
    # ~@,9600_8N1T2000,/1s0m23l23h0j32V4000v2500n0P0P100z0M500e1R
            if FW == "FW1":
                s.sendall(
                    b'~@,9600_8N1T2000,/1s0m23l23h0j32V4000v2500n0P0P100z0M500e1R\n')

    # WHEEL 2
    # Initial drive settings (velocity, steps ratio, current), plus homing routine — this runs automatically on power up.
    # ~@,9600_8N1T2000,/2s0m23l23h0j32V4000v2500n0P0P100z0M500e1R
            if FW == "FW2":
                s.sendall(
                    b'~@,9600_8N1T2000,/2s0m23l23h0j32V4000v2500n0P0P100z0M500e1R\n')

            data = s.recv(1024)
    #
    # Initial drive settings (velocity, steps ratio, current), plus homing routine — this runs automatically on power up.
    # ~@,9600_8N1T2000,/2s0m23l23h0j32V4000v2500n0P0P100z0M500e1R

            print('Received', repr(data))

    # =============================================================================
    #
    # stored_filter_wheel_procedures
    #
    # =============================================================================
    """
     FILTER WHEEL STORED PROCEDURES - These need to be sent to the motor controllers the first 
     time they are used… i.e if you replace a motor controller you should reinitialize with these commands…
    """

    def stored_filter_wheel_procedures(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # Position A1
    # ~@,9600_8N1T2000,/1s1A46667R
            s.sendall(b'~@,9600_8N1T2000,/1s1A46667R\n')
    #
    # Position A2
    # ~@,9600_8N1T2000,/1s2A62222R
            s.sendall(b'~@,9600_8N1T2000,/1s2A62222R\n')
    #
    # Position A3
    # ~@,9600_8N1T2000,/1s3A77778R
            s.sendall(b'~@,9600_8N1T2000,/1s3A77778R\n')
    #
    # Position A4
    # ~@,9600_8N1T2000,/1s4A0R
            s.sendall(b'~@,9600_8N1T2000,/1s4A0R\n')
    #
    # Position A5
    # ~@,9600_8N1T2000,/1s5A15555R
            s.sendall(b'~@,9600_8N1T2000,/1s5A15555R\n')
    #
    # Position A6
    # ~@,9600_8N1T2000,/1s6A31111R
            s.sendall(b'~@,9600_8N1T2000,/1s6A31111R\n')
    #
    # WHEEL 2
    # #
    # Position B1
    # ~@,9600_8N1T2000,/2s1A46667R
            s.sendall(b'~@,9600_8N1T2000,/2s1A46667R\n')
    #
    # Position B2
    # ~@,9600_8N1T2000,/2s2A62222R
            s.sendall(b'~@,9600_8N1T2000,/2s2A62222R\n')
    #
    # Position B3
    # ~@,9600_8N1T2000,/2s3A77778R
            s.sendall(b'~@,9600_8N1T2000,/2s3A77778R\n')
    #
    # Position B4
    # ~@,9600_8N1T2000,/2s4A0R
            s.sendall(b'~@,9600_8N1T2000,/2s4A0R\n')
    #
    # Position B5
    # ~@,9600_8N1T2000,/2s5A15555R
            s.sendall(b'~@,9600_8N1T2000,/2s5A15555R\n')
    #
    # Position B6
    # ~@,9600_8N1T2000,/2s6A31111R
            s.sendall(b'~@,9600_8N1T2000,/2s6A31111R\n')

        data = s.recv(1024)

        print('Received', repr(data))

    #
    # OPERATING COMMANDS:
    #
    # =============================================================================
    #
    # home_filter_wheel(FW)
    #
    # =============================================================================
    def home_filter_wheel(self, FW):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    #    assign 0 value to FW just to avoid errors while testing w/o FW in input
            if FW == None:
                FW1 = "0"
                FW2 = "0"

    # Homing occurs automatically on power up…. Or it can be forced using:
    #
    # ~@,9600_8N1T2000,/1e0R  (wheel 1)
    # ~@,9600_8N1T2000,/2e0R  (wheel 2)
            if FW == "FW1":
#                s.sendall(b'~@,9600_8N1T2000,/1e0R\n')
                s.sendall(b'1e0R\n')
            if FW == "FW2":
                s.sendall(b'~@,9600_8N1T2000,/2e0R\n')

            data = s.recv(1024)

            print('Received', repr(data))

    # =============================================================================
    #
    # move_filter_wheel
    #
    # =============================================================================
    def go_to_step(self, FW, step):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            if FW == "FW1":
#                string = '~@,9600_8N1T2000,/1A'+step+'R\n'
                string = '/1A'+step+'R\n'
                bstring = bytes(string, 'utf-8')
                print('     sending ',bstring)
                s.sendall(bstring)
            if FW == "FW2":
                s.sendall(b'~@,9600_8N1T2000,/2e1R\n')

            data = s.recv(1024)

            print('Received', repr(data))
            threading.Timer(5.0, self.query_current_step_counts(FW)).start()


    # =============================================================================
    #
    # move_filter_wheel
    #
    # =============================================================================
    def move_filter_wheel(self, position):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        self.stop_timer = False

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    # =============================================================================
    # Positions 1 through six are commanded as follows:
    #
    # ~@,9600_8N1T2000,/1e1R  (Position A1)
    # ~@,9600_8N1T2000,/2e1R  (Position B1)
    #
    # ~@,9600_8N1T2000,/1e2R  (Position A2)
    # ~@,9600_8N1T2000,/2e2R  (Position B2)
    #
    # ~@,9600_8N1T2000,/1e3R  (Position A3)
    # ~@,9600_8N1T2000,/2e3R  (Position B3)
    #
    # ~@,9600_8N1T2000,/1e4R  (Position A4)
    # ~@,9600_8N1T2000,/2e4R  (Position B4)
    #
    # ~@,9600_8N1T2000,/1e5R  (Position A5)
    # ~@,9600_8N1T2000,/2e5R  (Position B5)
    #
    # ~@,9600_8N1T2000,/1e6R  (Position A6)
    # ~@,9600_8N1T2000,/2e6R  (Position B6)
    # =============================================================================
    #
    # Position A1
            if position == 'A1':
#                print(position)
                current_steps = self.query_current_step_counts('FW1')
 #               print(current_steps)
                if current_steps != 46667:
  #                  print(current_steps)
                    s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
                    while current_steps != 46667:
                          current_steps = self.timed_query_current_count_monitor('FW1')
                          print(current_steps)
                # check sensor status
                self.stop_timer = True
                sensor_status = s.sendall(b'~@,9600_8N1T2000,/1?0\n')
                if ( (current_steps == 46667) ):#& (sensor_status == "/0'14") ):
                    return position,current_steps

    # Position A2
            if position == 'A2':
                s.sendall(b'~@,9600_8N1T2000,/1e2R\n')
    #
    # Position A3
            if position == 'A3':
                s.sendall(b'~@,9600_8N1T2000,/1e3R\n')
    #
    # Position A4
            if position == 'A4':
                s.sendall(b'~@,9600_8N1T2000,/1e4R\n')
    #
    # Position A5
            if position == 'A5':
                s.sendall(b'~@,9600_8N1T2000,/1e5R\n')
    #
    # Position A6
            if position == 'A6':
                s.sendall(b'~@,9600_8N1T2000,/1e6R\n')
    #
    # WHEEL 2
    # #
    # Position B1
            if position == 'B1':
                current_steps = self.query_current_step_counts('FW2')
                if current_steps != 46667:
                    s.sendall(b'~@,9600_8N1T2000,/2e1R\n')
                    while current_steps != 46667:
                        current_steps = self.timed_query_current_count_monitor(
                            'FW2')
                return position, current_steps
    #
    # Position B2
            if position == 'B2':
                s.sendall(b'~@,9600_8N1T2000,/2e2R\n')
    #
    # Position B3
            if position == 'B3':
                s.sendall(b'~@,9600_8N1T2000,/2e3R\n')
    #
    # Position B4
            if position == 'B4':
                s.sendall(b'~@,9600_8N1T2000,/2e4R\n')
    #
    # Position B5
            if position == 'B5':
                s.sendall(b'~@,9600_8N1T2000,/2e5R\n')
    #
    # Position B6
            if position == 'B6':
                s.sendall(b'~@,9600_8N1T2000,/2e6R\n')

            data = s.recv(1024)

        print('Received', repr(data))


    # =============================================================================
    # #
    # # QUERY COMMANDS:
    # #
    # # ~@,9600_8N1T2000,1/?0  (returns wheel 1, current step count)
    # # ~@,9600_8N1T2000,/2?0  (returns wheel 2, current step count)
    # #
    # # Example response: /0`15555
    # #
    # # When the wheel is in position (i.e. not moving) the step count should be:
    # # Position 1: 46667
    # # Position 2: 62222
    # # Position 3: 77778
    # # Position 4: 0
    # # Position 5: 15555
    # # Position 6: 31111
    # #
    # #
    # # ~@,9600_8N1T2000,1/?0  (returns wheel 1, sensor status)
    # # ~@,9600_8N1T2000,/2?0  (returns wheel 2, sensor status)
    # #
    # # Example Response: /0'14
    # #
    # # When the wheel is in position (i.e. not moving) the sensor status should be:
    # # Position 1: 14
    # # Position 2: 14
    # # Position 3: 14
    # # Position 4: 13
    # # Position 5: 14
    # # Position 6: 14
    # # =============================================================================
    #
    # =============================================================================

    # =============================================================================
    #
    # return_current_step_counts
    #
    # =============================================================================
    def query_current_step_counts(self, FW):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    #    assign 0 value to FW just to avoid errors while testing w/o FW in input
#           if FW == None:
#               FW1 = "0"
#                FW2 = "0"

            if FW == "FW1":
                # return s.sendall(b'~@,9600_8N1T2000,/1?0\n')
                s.sendall(b'~@,9600_8N1T2000,/1?0\n')

            if FW == "FW2":
                return s.sendall(b'~@,9600_8N1T2000,/2?0\n')

            data = s.recv(1024)

 #       print(FW)
        print('Received', repr(data))

    def timed_query_current_count_monitor(self, FW):
        import threading
        while self.stop_timer == False:
            threading.Timer(30.0, self.query_current_step_counts(FW)).start()

    ######

    def initialize_grism_rails(self):

        # =============================================================================
        # # =============================================================================
        # # Initialization settings for Grism Drives
        # #
        # # Notes:
        # # I set these already, and they only need to be programmed once. However, we need to be able to send these commands in the event a drive is replaced.
        # #
        # # ~@,9600_8N1T2000,/3s0m23l23h0j4V7000v2500n2f1Z100000000R ; init (A)
        # # ~@,9600_8N1T2000,/4s0m23l23h0j4V7000v2500n2f1Z100000000R ; init (B)
        # #
        # # ~@,9600_8N1T2000,/3s1S12A69000R
        # # ; position 1 (A)
        # # ~@,9600_8N1T2000,/4s1S12A173000R
        # # ; position 1 (B))
        # #
        # # ~@,9600_8N1T2000,/3s2S12A103300R
        # # ; position 2 (A)
        # # ~@,9600_8N1T2000,/4s2S12A207300R
        # # ; position 2 (B)
        # #
        # # ~@,9600_8N1T2000,/3s10A0R
        # # ; stowed position (A)
        # # ~@,9600_8N1T2000,/4s10A0R
        # # ; stowed stowed (B)
        # #
        # =============================================================================
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # Init (A)
            s.sendall(
                b'~@,9600_8N1T2000,/3s0m23l23h0j4V7000v2500n2f1Z100000000R\n')

    # Init (B)
            s.sendall(
                b'~@,9600_8N1T2000,/4s0m23l23h0j4V7000v2500n2f1Z100000000R\n')

            data = s.recv(1024)

            print('Received', repr(data))

    def stored_grism_rails_procedures(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
    # Position 1 (A)
    # # ~@,9600_8N1T2000,/3s1S12A69000R
            s.sendall(b'~@,9600_8N1T2000,/3s1S12A69000R\n')
    #
    # # ; position 1 (B))
    # # ~@,9600_8N1T2000,/4s1S12A173000R
            s.sendall(b'~@,9600_8N1T2000,/4s1S12A173000R\n')
    # #
    # # ; position 2 (A)
    # # ~@,9600_8N1T2000,/3s2S12A103300R
            s.sendall(b'~@,9600_8N1T2000,/3s2S12A103300R\n')
    #
    # # ; position 2 (B)
    # # ~@,9600_8N1T2000,/4s2S12A207300R
            s.sendall(b'~@,9600_8N1T2000,/4s2S12A207300R\n')
    #
    # # ; stowed position (A)
    # # ~@,9600_8N1T2000,/3s10A0R
            s.sendall(b'~@,9600_8N1T2000,/3s10A0R\n')
    #
    # # ; stowed stowed (B)
    # # ~@,9600_8N1T2000,/4s10A0R
            s.sendall(b'~@,9600_8N1T2000,/4s10A0R\n')

            data = s.recv(1024)

            print('Received', repr(data))

    def home_grism_rails(self, GR):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # # ~@,9600_8N1T2000,/3e0R
    # # ; Initialization/ homing (A)
    # # ~@,9600_8N1T2000,/4e0R
    # # ; Initialization/ homing (B)

            if GR == "GR_A":
                s.sendall(b'~@,9600_8N1T2000,/3e0R\n')
            if GR == "GR_B":
                s.sendall(b'~@,9600_8N1T2000,/4e0R\n')

            data = s.recv(1024)

            print('Received', repr(data))

    def fast_home_grism_rails(self, GR):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # #
    # # ~@,9600_8N1T2000,/3e10R
    # # ; fast move to home
    # # ~@,9600_8N1T2000,/4e10R
    # # ; fast move to home
    #
            if GR == "GR_A":
                s.sendall(b'~@,9600_8N1T2000,/3e10R\n')
            if GR == "GR_B":
                s.sendall(b'~@,9600_8N1T2000,/4e10R\n')

            data = s.recv(1024)

            print('Received', repr(data))

    def move_grism_rails(self, position):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # =============================================================================
    # #
    # # Commands to execute in your code are as follows:
    # #
    # # Notes:
    # # Homing will happen automatically when the drive is powered up.
    # # Sled A must me home before sled B can move away from home
    # # Sled B must be home before sled A cam move away from home
    # #
    # #
    # # ~@,9600_8N1T2000,/3e0R
    # # ; Initialization/ homing (A)
    # # ~@,9600_8N1T2000,/4e0R
    # # ; Initialization/ homing (B)
    # #
    # # ~@,9600_8N1T2000,/3e1R
    # # ; position 1(A)
    # # ~@,9600_8N1T2000,/4e1R
    # # ; position 1(B)
    # #
    # # ~@,9600_8N1T2000,/3e2R
    # # ; position 2 (A)
    # # ~@,9600_8N1T2000,/4e2R
    # # ; position 2 (B)
    # #
    # # ~@,9600_8N1T2000,/3e10R
    # # ; fast move to home
    # # ~@,9600_8N1T2000,/4e10R
    # # ; fast move to home
    #
    # =============================================================================
    #
    # Position 1(A)
    # # Sled B must be home before sled A cam move away from home
            if position == '1(A)':
               # ; Initialization/ homing (B)
               # ~@,9600_8N1T2000,/4e0R
                s.sendall(b'~@,9600_8N1T2000,/4e0R\n')
                railA_counts = s.sendall(b'~@,9600_8N1T2000,/4?0\n')
               #current_steps = return_current_step_counts(FW)
               # if current_steps != 46667:
               #     s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
               #     while current_steps != 46667:
               #         current_steps = step_count_monitor(FW)
               # return position,current_steps
                # ; position 1(A)
                # ~@,9600_8N1T2000,/3e1R
                s.sendall(b'~@,9600_8N1T2000,/3e1R\n')

            if position == '2(A)':
               # ; Initialization/ homing (B)
               # ~@,9600_8N1T2000,/4e0R
                s.sendall(b'~@,9600_8N1T2000,/4e0R\n')
                railA_counts = s.sendall(b'~@,9600_8N1T2000,/4?0\n')
               #current_steps = return_current_step_counts(FW)
               # if current_steps != 46667:
               #     s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
               #     while current_steps != 46667:
               #         current_steps = step_count_monitor(FW)
               # return position,current_steps
                # ; position 2 (A)
                # ~@,9600_8N1T2000,/3e2R
                s.sendall(b'~@,9600_8N1T2000,/3e2R\n')

            if position == '1(B)':
                # ; Initialization/ homing (A)
                # ~@,9600_8N1T2000,/3e0R
                s.sendall(b'~@,9600_8N1T2000,/3e0R\n')
                railB_counts = s.sendall(b'~@,9600_8N1T2000,/3?0\n')
               #current_steps = return_current_step_counts(FW)
               # if current_steps != 46667:
               #     s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
               #     while current_steps != 46667:
               #         current_steps = step_count_monitor(FW)
               # return position,current_steps
                # ; position 1(B)
                # ~@,9600_8N1T2000,/4e1R
                s.sendall(b'~@,9600_8N1T2000,/4e1R\n')

            if position == '2(B)':
                # ; Initialization/ homing (A)
                # ~@,9600_8N1T2000,/3e0R
                s.sendall(b'~@,9600_8N1T2000,/3e0R\n')
                railB_counts = s.sendall(b'~@,9600_8N1T2000,/3?0\n')
               #current_steps = return_current_step_counts(FW)
               # if current_steps != 46667:
               #     s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
               #     while current_steps != 46667:
               #         current_steps = step_count_monitor(FW)
               # return position,current_steps
                # ; position 2 (B)
                # ~@,9600_8N1T2000,/4e2R
                s.sendall(b'~@,9600_8N1T2000,/4e2R\n')

    #
    # AND NOW FOR SOMETHING NEW….
    #
    # All commands that you want to send to the EZHR motor controllers must be preceded with: ~@,9600_8N1T2000,
    #
    # ~ is the character that all messages to the PCM start with. @ means push the message to the RS485 bus. 9600_8N1T2000 means use 9600 baud, 8 data bits, no parity, 1 stop bit, with a 2000 millisecond timeout for a response message.
    #
    # All the commands you send to the EZHR start with a drive number: /1, /2, /3 etc.
    #
    # When you send a command like ~@,9600_8N1T2000,/3e1R you are asking drive 3 (/3) to execute stored procedure 1 (e1). The R last the end tells it to run the command
    #
    # Every command returns a response packet. The format of the packet is detailed in the EZHR instructions. See page 23 of the EZHR manual.
    #
    # You can also query the drive at anytime. Query commands start with a ? and do not need an R at the end. The command to query the current step count is ?0, and the command to query the limit switches is ?4. For example: ~@,9600_8N1T2000,/3?4… This asks drive 3 (/3) to return the position switch status (?4). Query commands are on page 9 of the manual.
    #
    # You should query the status of the motor controller to see if it has stopped moving, then query the step count, and the position sensor status, to make sure it went to where you thought it should go to.
    #
    # With the grisms you must send one drive home, and make sure it is home by checking its status before  moving the other drive…
    #
    # AND FOR SUPPORT...
    #
    # CALL ME from 8AM to 10PM +1(443) 299 7810
    # TEXT ME anytime +1(443) 299 7810
    # FB MESSENGER ME… Facebook.com/limey.steve.5 ...Use the video or audio chat option - it rings on my cell.
    # FACETIME ME +1(443)299 7810
    #
    # OK, I leave for the UK on Saturday for 2 weeks… I will have my cell phone and it should work… I will also have my computer… The UK is 5 hours ahead… I will be available from 10AM to 10PM UK time. This equates to 5AM to 5PM eastern standard time.
    #
    # Feel free to call anytime… If I can’t speak I will tell you, but I won’t be offended or annoyed…
    #
    # REMEMBER… It’s the squeaky wheel that get oiled first… Squeak loudly, and don’t feel sorry!
    #
    # Regards,
    # =============================================================================
