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
        self.params = {'Host': '128.220.146.254', 'Port': 8889}
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
            
  #          s.sendall(b'~se,1,on\n')
            data = s.recv(1024)

        print("Sent: b'~se,all,on\\n'  - Received", repr(data))
        return(repr(data))

    # =============================================================================
    #
    # enable switch
    #
    # =============================================================================
    def enable_switch(self):
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
            s.sendall(b'~@,9600_8N1T2000,/1n2R\n')
  #          s.sendall(b'~se,1,on\n')
            data = s.recv(1024)

        print("Sent: b'~@,9600_8N1T2000,/1n2R\\n'  - Received", repr(data))
 #       print('Received', repr(data))
        return(repr(data))

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

        print("Sent: b'~se,all,off\\n'  - Received", repr(data))
        return(repr(data))


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

        print("Sent: b'~ge,all\\n'  - Received", repr(data))
        return(repr(data))


    # =============================================================================
    #
    # initialize_filter_wheel
    #
    # =============================================================================
    def initialize_filter_wheel(self):
        import socket

   
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
            s.sendall(
                    b'~@,9600_8N1T2000,/1s0m23l23h0j32V4000v2500n0P0P100z0M500e1R\n')


            data = s.recv(1024)
    #
    # Initial drive settings (velocity, steps ratio, current), plus homing routine — this runs automatically on power up.
    # ~@,9600_8N1T2000,/2s0m23l23h0j32V4000v2500n0P0P100z0M500e1R

        print("Sent: b'~@,9600_8N1T2000,/1s0m23l23h0j32V4000v2500n0P0P100z0M500e1R\\n'  - Received", repr(data))
        return(repr(data))


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
 
        data = s.recv(1024)

        print("Sent: b'~@,9600_8N1T2000,/1s1A46667R\\n'  - Received", repr(data))
        return(repr(data))

    #
    # OPERATING COMMANDS:
    #
    # =============================================================================
    #
    # home_filter_wheel(FW)
    #
    # =============================================================================
    def home_filter_wheel(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # Homing occurs automatically on power up…. Or it can be forced using:
    #
    # ~@,9600_8N1T2000,/1e0R  (wheel 1)
    # ~@,9600_8N1T2000,/2e0R  (wheel 2)
            s.sendall(b'~@,9600_8N1T2000,/1e0R\n')

            data = s.recv(1024)

        print("Sent: b'~@,9600_8N1T2000,/1e0R\\n'  - Received", repr(data))
        return(repr(data))


    #
    # =============================================================================
    #
    # stopl(FW)
    #
    # =============================================================================
    def stop_filter_wheel(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

    # Homing occurs automatically on power up…. Or it can be forced using:
    #
    # ~@,9600_8N1T2000,/1e0R  (wheel 1)
    # ~@,9600_8N1T2000,/2e0R  (wheel 2)
            s.sendall(b'~@,9600_8N1T2000,/1T\n')
 #           s.sendall(b'1e0R\\n')

            data = s.recv(1024)

        print("Sent: '~@,9600_8N1T2000,/1T\\n' - Received", repr(data))
        return(repr(data))


    # =============================================================================
    #
    # move_filter_wheel
    #
    # =============================================================================
    def go_to_step(self, step):
        import socket
#        import threading

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
#                string = '~@,9600_8N1T2000,/1A'+step+'R\n'
            string = '~@,9600_8N1T2000,/1A'+step+'R\n'
            bstring = bytes(string, 'utf-8')
            print('     sending ',bstring)
            s.sendall(bstring)

            data = s.recv(1024)

        print("Sent:  '~@,9600_8N1T2000,/1A"+step+"R\\n'' - Received", repr(data))
        return(repr(data))


    # =============================================================================
    #
    # move_filter_wheel
    #
    # =============================================================================
    def move_filter_wheel(self, Aposition):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        #self.stop_timer = False

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
            print(Aposition)
            if Aposition == 'A1':
                counts = "46667"
                command = "e1"
            if Aposition == 'A2':
                counts = "62222"
                command = "e2"
            if Aposition == 'A3':
                counts = "77778"
                command = "e3"
            if Aposition == 'A4':
                counts = "0"
                command = "e4"
            if Aposition == 'A5':
                counts = "15555"
                command = "e5"
            if Aposition == 'A6':
                counts = "31111"
                command = "e6"
            self.current_steps = self.query_current_step_counts()
            if self.current_steps != counts:
#                s.sendall(b'~@,9600_8N1T2000,/1e1R\n')
                string = '~@,9600_8N1T2000,/1'+command+'R\n'
                bstring = bytes(string, 'utf-8')
                print('     sending ',bstring)
                s.sendall(bstring)

                while self.current_steps != counts:
                    self.timed_query_current_count_monitor()
                    s.sendall(b'~@,9600_8N1T2000,/1?0\n')
                    answer = str(s.recv(1024))
                    print('answer = ',answer, answer[5:-1])
                    self.current_steps = answer[5:-1] #removing "Received b'/0`"
                    print("current_steps",self.current_steps)
            self.t.cancel()
            answer = s.sendall(b'~@,9600_8N1T2000,/1?0\n')
#                if ( (current_steps == counts) ):#& (sensor_status == "/0'14") ):
#                    return Aposition,current_steps

 
            data = s.recv(1024)

            print("Sent:  b'~@,9600_8N1T2000,/1?0\\n' - Received", repr(data))
            return(repr(data))



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
    def query_current_step_counts(self):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

                # return s.sendall(b'~@,9600_8N1T2000,/1?0\n')
            s.sendall(b'~@,9600_8N1T2000,/1?0\n')


            data = s.recv(1024)

        print('Received', repr(data))
        return(repr(data))


    def timed_query_current_count_monitor(self):
        import threading
        
        self.t  = threading.Timer(2.,self.do_nothing)
        self.t.start()

    def do_nothing(self):
        pass

    def send_command_string(self,Command_string):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
#            print('Cs = ',Command_string)
#            string = '~@,9600_8N1T2000,"+Command_string+"'
            string = '~@,9600_8N1T2000,'+Command_string
 #           string = '~@,9600_8N1T2000,/1s1A46667R\n'
#            print(string)
            bstring = bytes(string, 'utf-8')
            print('     sending ',bstring)
  #          s.sendall(b'~@,9600_8N1T2000,/1s1A46667R\n')
            s.sendall(bstring)
 
            data = s.recv(1024)

        print("Sent:  '~@,9600_8N1T2000,'"+Command_string+" - Received", repr(data))
        return(repr(data))

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
