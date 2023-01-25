#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 22:00:03 2022

import SAMOS_Functions

@author: robberto

to use:
> import SAMOS_Functions
> SF = SAMOS_Functions.Class_SAMOS_Functions()

"""
import csv
from pathlib import Path
#define the local directory, absolute so it is not messed up when this is called
path = Path(__file__).parent.absolute()
local_dir = str(path.absolute())

class Class_SAMOS_Functions:
    def __init__(self):
        self.system_files = local_dir 
    
# =============================================================================
#     def read_IP_default(self):
# =============================================================================
    def read_IP_default():
        dict_from_csv = {}

        with open(local_dir+"/IP_addresses_default.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}

        return dict_from_csv
    
     
    
# =============================================================================
#     def read_IP_user(self):
# =============================================================================
    def read_IP_user():
        dict_from_csv = {}

        with open(local_dir+"/IP_addresses_user.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}

        return dict_from_csv   
      
# =============================================================================
#     def read_dir_default(self):
# =============================================================================
    def read_dir_default():
        dict_from_csv = {}

        with open(local_dir+"/dirlist_default.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}

        return dict_from_csv   

# =============================================================================
#     def read_dir_user(self):
# =============================================================================
    def read_dir_user():
        dict_from_csv = {}

        with open(local_dir+"/dirlist_user.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}

        return dict_from_csv   
    
# =============================================================================
#     def read_IP_status(self):
# =============================================================================
    def read_IP_initial_status():
        dict_from_csv = {}

        with open(local_dir+"/IP_initial_status_dict.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}
            
        return dict_from_csv       

    def read_IP_status():
        dict_from_csv = {}

        with open(local_dir+"/IP_status_dict.csv", mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}
            
        return dict_from_csv       
    
#print(SF.read_IP_user())    