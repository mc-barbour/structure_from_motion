#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:23:08 2022

@author: mbarbour

Main class for surface metrics

"""

import pyvista as pv

class surface_metric():
    
    _last_val = None
    _last_opt = None
    
    def compute(self, truthmesh: pv.PolyData, testmesh: pv.PolyData):
        """
        This is the main compute function
        
        Input: test and truth surfaces, both in PolyData format
        
        Output: metric value
        """
        
        raise NotImplementedError
        
    def getname(self):
        raise NotImplementedError 
        
    def _update_vals(self, val, opt):
        self._last_val = val
        self._last_opt = opt
        
        

