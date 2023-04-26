#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:04:48 2022

@author: mbarbour
"""

from .metric import surface_metric
import pyvista as pv
import numpy as np



class volume_ratio(surface_metric):
    
    _debug_show = False
    
    def __init__(self, debug_show=False):
        self._debug_show = debug_show   
        
    def getname(self):
        return "Volume Ratio"
    
    def compute(self, truthmesh, testmesh):
        opt = {}
        
        print("Computing {:s}".format(self.getname()))
        print("{:d} points in truthmesh and {:d} points in testmesh".format(truthmesh.number_of_points, testmesh.number_of_points))
        
        # First compute euclidian distance
        A = truthmesh.volume
        B = testmesh.volume
        
        metric = B/A
        opt = {'voltest':testmesh.volume,'voltruth':truthmesh.volume}
        
        return (metric, opt)
    
    

        
        