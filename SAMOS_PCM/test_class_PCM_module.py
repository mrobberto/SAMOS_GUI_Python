#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 18:11:10 2022

@author: robberto
"""

from Class_PCM_module import Class_PCM

PCM = Class_PCM()


#print('initialize:')
PCM.echo_client()

# print('\n _open:')
#PCM._open()
# 
# print('\npower on:')
#PCM._close()
# 
#print('\nall ports status:')
PCM.all_ports_status()
# 
# print('\n intitalize:')
#PCM.initialize_filter_wheel("FW1")
#PCM.initialize_filter_wheel("FW2")

#print('\n motors stop:')
#PCM.motors_stop("FW1")
#PCM.motors_stop("FW2")

## print('\n home:')
#PCM.home_filter_wheel("FW1") 
#PCM.home_filter_wheel("FW2") 
# 
# print('\n stored PCM procedures:')
#PCM.stored_filter_wheel_procedures()

# print('\n move to step 12345:')
#PCM.go_to_step("FW1","15555")
#PCM.go_to_step("FW2","12345")
# 
#print('\n move to position A1: (46667)')
#PCM.move_filter_wheel("A1")
#PCM.move_filter_wheel("A2")
#PCM.move_filter_wheel("A3") 
#PCM.move_filter_wheel("A4")
#PCM.move_filter_wheel("A5")
#PCM.move_filter_wheel("A6")
#PCM.move_filter_wheel("B1")
#PCM.move_filter_wheel("B2")
#PCM.move_filter_wheel("B3")
#PCM.move_filter_wheel("B4")
#PCM.move_filter_wheel("B5")
#PCM.move_filter_wheel("B6")
# 
#print('\n query step:')
#PCM.query_current_step_counts("FW1")
#PCM.query_current_step_counts("FW2")
# 
# =============================================================================
# GRISM RAILS
# =============================================================================
#
# print('\n initialize grism_rails:')
#PCM.initialize_grism_rails()
#
# print('\n home_grism_rails(GR)
#PCM.home_grism_rails("GR_A")
#PCM.home_grism_rails("GR_B")
#
# print('\n move_grism_rails(GR)
#PCM.move_grism_rails("1(A)")
#PCM.move_grism_rails("2(A)")
#PCM.move_grism_rails("1(B)")
#PCM.move_grism_rails("2(B)")
#
#print('\n Grism Rail query step:')
#PCM.GR_query_current_step_counts("GR_A")
#PCM.GR_query_current_step_counts("GR_B")
# 
# print('\n GR_move to step 12345:')
#PCM.GR_go_to_step("GR_A","12345")
#PCM.GR_go_to_step("GR_B","12345")
