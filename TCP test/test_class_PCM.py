#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 18:11:10 2022

@author: robberto
"""

from Class_PCM import Class_PCM

PCM = Class_PCM()

print('echo from server:')
PCM.echo_client()

print('\npower off:')
PCM.power_off()

print('\npower on:')
#PCM.power_on()

print('\n all ports status:')
#PCM.all_ports_status()

print('\n intitalize FW1:')
#PCM.initialize_filter_wheel("FW1")

print('\n home FW1:')
#PCM.home_filter_wheel( "FW1")

print('\n move FW1 to step 12345:')
#PCM.go_to_step("FW1", "12345")

print('\n move FW1 to position A1: (46667)')
#PCM.move_filter_wheel("A1")

print('\n query step of FW1:')
#PCM.query_current_step_counts("FW1")