#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 18:11:10 2022

@author: robberto
"""

from Class_PCM_module import Class_PCM_module

PCM = Class_PCM_module()

print('echo from server:')
PCM.echo_client()

print('\npower off:')
#PCM.power_off()

print('\npower on:')
#PCM.power_on()

print('\nall ports status:')
#PCM.all_ports_status()

print('\n intitalize:')
#PCM.initialize_filter_wheel()

print('\n home:')
#PCM.home_filter_wheel()

print('\n move to step 12345:')
#PCM.go_to_step("12345")

print('\n move to position A1: (46667)')
PCM.move_filter_wheel("A2")

print('\n query step:')
#PCM.query_current_step_counts()

#PCM.stop_filter_wheel()

#n1 :enable limits switches