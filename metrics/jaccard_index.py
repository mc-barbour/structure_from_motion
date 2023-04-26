#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 16:06:53 2022

@author: mbarbour
"""


from .metric import surface_metric
import pyvista as pv
import numpy as np


class jaccard_index(surface_metric):
    
    _debug_show = False
    
    def __init__(self, debug_show=False):
        self._debug_show = debug_show   
        
    def getname(self):
        return "Jaccard Index"
    
    def check_mesh_size(self, A, B, max_tets=25000):
        
        if A.n_faces > max_tets:
            print("Warning, too many test, decimating mesh ...")

            reduction = 1. - float(max_tets/A.n_faces)
            print("Reducing by {:0.1f}%".format(reduction*100))
            A.decimate(reduction, volume_preservation=True, inplace=True)
            print("Now using {:d} points".format(A.n_points))
        
        if B.n_faces > max_tets:
            print("Warning, too many test, decimating mesh ...")

            reduction = 1. - float(max_tets/B.n_faces)
            print("Reducing by {:0.1f}%".format(reduction*100))
            B.decimate(reduction, volume_preservation=True, inplace=True)
            print("Now using {:d} points".format(B.n_points))
            
    def show(self, truthmesh, testmesh, intersection, union):
        
        p = pv.Plotter(shape=(3,1))
        p.subplot(0,0)
        p.add_mesh(truthmesh, color='cyan', opacity = 0.5, label='truth')
        p.add_mesh(testmesh, color='white', opacity = 0.5, label='test')
        p.add_text("{:s} value: {:f}".format(self.getname(), self._last_val))
        p.add_legend()
        
        p.subplot(1,0)
        p.add_mesh(intersection, color='cyan', opacity = 0.5, label='truth')
        p.add_text("Intersection")
        
        p.subplot(2,0)
        p.add_mesh(union, color='cyan', opacity = 0.5, label='truth')
        p.add_text("Union")

        p.show()
        
    
    def compute(self, truthmesh, testmesh):
       
        opt = {}
        
        testcopy = testmesh.copy()
        truthcopy = truthmesh.copy()
        
        self.check_mesh_size(testcopy, truthcopy)
        
        union = truthcopy.boolean_union(testcopy)
        intersection = truthcopy.boolean_intersection(testcopy)
        

        metric = intersection.volume / union.volume
        
        
        opt["Intersection Volume"] = intersection.volume
        opt["Union Volume"] = union.volume
        
        self._update_vals(metric, opt)

        
        if self._debug_show:
            self.show(truthmesh, testmesh, intersection, union)
            

        return (metric, opt)