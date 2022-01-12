#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jann 11 17:31:32 2022

Module to simulate communication with SOAR TCS:

FOR TESTING TCP COMMUNICATION ON LOCALHOST (see instuction below)
> echo_server() 
> echo_client()

TCS procedures
> TCS_Focus()
> TCS_Guider()
> TCS_Info(FW)
> TCS_Offset()
> TCS_Way(FW)

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


class TCS():

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
    # Send TO TCS
    #
    # =============================================================================
    def send_to_TCS(self,string):
        import socket

        # '10.0.0.179'#127.0.0.1'  # The server's hostname or IP address
        HOST = self.params['Host']
        # 1000#65432        # The port used by the server
        PORT = self.params['Port']

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
    #
            s.sendall(string)
            data = s.recv(1024)

        print('Received', repr(data))

    # =============================================================================
    #
    # FOCUS
    #
    # =============================================================================


    def FOCUS(**kwargs):
        #v = FOCUS(first="MOVEREL", second="1230")
        v= kwargs.items() #this is a dict_items
        key = list(v)[0][0]
        value = list(v)[0][1]   
        if value == "INIT":
            string  = "FOCUS INIT"
        if value == "STATUS":
            string = "FOCUS STATUS"
        if value == "STOP":
            string = "FOCUS STOP"
        if value == "MOVEABS":
            string = "FOCUS MOVEABS " + list(v)[1][1]
        if value == "MOVEREL":
            string = "FOCUS MOVEREL " + list(v)[1][1]
        print(string)    
        send_to_TCS(string)

    # =============================================================================
    #
    # GUIDER
    #
    # =============================================================================

    def GUIDER(**kwargs):
        #v = GUIDERfirst="ENABLE")
        v= kwargs.items() #this is a dict_items
        key = list(v)[0][0]
        value = list(v)[0][1]   
        if value == "ENABLE":
            string  = "GUIDER ENABLE"
        if value == "DISABLE":
            string = "DONE ENABLE"
        if value == "STATUS":
            string = "GUIDER STATUS"
        print(string)    
        send_to_TCS(string)

    # =============================================================================
    #
    # INFO
    #
    # =============================================================================

    def INFO():
        string = "INFO"
        print(string)    
        send_to_TCS(string)

    # =============================================================================
    #
    # OFFSET
    #
    # =============================================================================

    def OFFSET(**kwargs):
        #v = GUIDERfirst="MOVE", second = "E 34.3 N 56.7") #units arcseconds
        v= kwargs.items() #this is a dict_items
        key = list(v)[0][0]
        value = list(v)[0][1]   
        if value == "MOVE":
            string  = "OFFSET MOVE" +  + list(v)[1][1]
        if value == "STATUS":
            string = "OFFSET STATUS"
        print(string)    
        send_to_TCS(string)
