#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 18:11:10 2022

@author: robberto
"""

from Class_DMD import Class_DMD

DMD = Class_DMD()


#print('initialize:')
DMD.initialize()

# print('\n _open:')
#DMD._open()
# 
# print('\npower on:')
#DMD._close()
# 
#print('\nall ports status:')
DMD.all_ports_status()
# 
# print('\n intitalize:')
#DMD.initialize_filter_wheel("FW1")
#DMD.initialize_filter_wheel("FW2")

#print('\n motors stop:')
#DMD.motors_stop("FW1")
#DMD.motors_stop("FW2")

## print('\n home:')
#DMD.home_filter_wheel("FW1") 
#DMD.home_filter_wheel("FW2") 
# 
# print('\n stored DMD procedures:')
#DMD.stored_filter_wheel_procedures()

# print('\n move to step 12345:')
#DMD.go_to_step("FW1","15555")
#DMD.go_to_step("FW2","12345")
# 
#print('\n move to position A1: (46667)')
#DMD.move_filter_wheel("A1")
#DMD.move_filter_wheel("A2")
#DMD.move_filter_wheel("A3") 
#DMD.move_filter_wheel("A4")
#DMD.move_filter_wheel("A5")
#DMD.move_filter_wheel("A6")
#DMD.move_filter_wheel("B1")
#DMD.move_filter_wheel("B2")
#DMD.move_filter_wheel("B3")
#DMD.move_filter_wheel("B4")
#DMD.move_filter_wheel("B5")
#DMD.move_filter_wheel("B6")
# 
#print('\n query step:')
#DMD.query_current_step_counts("FW1")
#DMD.query_current_step_counts("FW2")
# 
# =============================================================================
# GRISM RAILS
# =============================================================================
#
# print('\n initialize grism_rails:')
#DMD.initialize_grism_rails()
#
# print('\n home_grism_rails(GR)
#DMD.home_grism_rails("GR_A")
#DMD.home_grism_rails("GR_B")
#
# print('\n move_grism_rails(GR)
#DMD.move_grism_rails("1(A)")
#DMD.move_grism_rails("2(A)")
#DMD.move_grism_rails("1(B)")
#DMD.move_grism_rails("2(B)")
#
#print('\n Grism Rail query step:')
#DMD.GR_query_current_step_counts("GR_A")
#DMD.GR_query_current_step_counts("GR_B")
# 
# print('\n GR_move to step 12345:')
#DMD.GR_go_to_step("GR_A","12345")
#DMD.GR_go_to_step("GR_B","12345")
