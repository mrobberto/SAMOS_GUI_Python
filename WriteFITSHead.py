#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:34:16 2023

@author: danakoeppe
"""

import numpy as np
import pandas as pd
import os

from astropy.io import fits


class FITSHead():
    """
    Obtain instrument configurations, WCS, etc. and
        keep track of them with a dictionary.
    After exposure, write the contents of dictionary to FITS header
        using header.set(key,val,comment)
    
    """
    
    def __init__():
        
        pass