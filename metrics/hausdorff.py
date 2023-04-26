#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:18:42 2022

@author: mbarbour
"""

from .metric import surface_metric
import pyvista as pv
import numpy as np
from scipy.spatial.distance import directed_hausdorff
from scipy.spatial.distance import cdist


class hausdorff(surface_metric):
    
    _debug_show = False
    
    def __init__(self, debug_show=False):
        self._debug_show = debug_show   
        
    def getname(self):
        return "Hausdorff"
    
    def check_mesh_size(self, A, B, max_tets=50000):
        
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
    
    def compute(self, truthmesh, testmesh):
        opt = {}
        
        print("Computing {:s}".format(self.getname()))
        print("{:d} points in truthmesh and {:d} points in testmesh".format(truthmesh.number_of_points, testmesh.number_of_points))


        testcopy = testmesh.copy()
        truthcopy = truthmesh.copy()
        
        self.check_mesh_size(testcopy, truthcopy)
        

        # First compute euclidian distance
        A = truthcopy.points.copy()
        B = testcopy.points.copy()

        
        fwd, id_A_fwd, id_B_fwd = directed_hausdorff(A, B)
        bwd, id_B_bwd, id_A_bwd = directed_hausdorff(B, A)
        # fwd = np.max(np.min(cdist(A, B, 'euclidean'), axis=1))
        # bwd = np.max(np.min(cdist(B, A, 'euclidean'), axis=1))

        # take the max
        metric = max(fwd, bwd)
        
        print(fwd, bwd)
        
        opt["A"] = A
        opt["B"] = B
        opt["index A fwd"] = id_A_fwd
        opt["index B fwd"] = id_B_fwd
        opt["index A bwd"] = id_A_bwd
        opt["index B bwd"] = id_B_bwd
        
        self._update_vals(metric, opt)
        
        if self._debug_show:
            self.show(truthmesh, testmesh)
        
        return (metric, opt)
    
    def show(self, truthmesh, testmesh):
        
        A_fwd = self._last_opt["index A fwd"]
        B_fwd = self._last_opt["index B fwd"]
        
        A_bwd = self._last_opt["index A bwd"]
        B_bwd = self._last_opt["index B bwd"]
        
        p = pv.Plotter()
        p.add_mesh(truthmesh, color='cyan', opacity = 0.5, label='truth')
        p.add_mesh(testmesh, color='white', opacity = 0.5, label='test')
        p.add_mesh(pv.PolyData(truthmesh.points[A_fwd,:]), render_points_as_spheres=True, color='red', point_size=15)
        p.add_mesh(pv.PolyData(testmesh.points[B_fwd,:]), render_points_as_spheres=True, color='red', point_size=15)
        p.add_mesh(pv.PolyData(truthmesh.points[A_bwd,:]), render_points_as_spheres=True, color='blue', point_size=15)
        p.add_mesh(pv.PolyData(testmesh.points[B_bwd,:]), render_points_as_spheres=True, color='blue', point_size=15)

        p.add_text("{:s} value: {:f}".format(self.getname(), self._last_val))
        p.add_legend()
        p.show()
        