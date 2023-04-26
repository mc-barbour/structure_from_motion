# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:55:47 2023

@author: barbourm
"""

"""
Created on Tue Jan 17 15:16:26 2023

@author: barbourm
"""

import numpy as np
import cv2 as cv
import pandas as pd
import pyvista as pv
import glob
import plotly.graph_objects as go
import plotly.express as px

import plotly.io as pio
from plotly.subplots import make_subplots

from source.camera_calibration import *

pio.renderers.default = "browser"


#%% Load images
# cal_image_dir = '/Users/mbarbour/OneDrive - UW/CFD SGS T32/SurfaceReconstruction/2.7mm__50%Light_Run2_Calibration_focus0.25turnclockwise'
# cal_image_dir = "D:\\Barbour\\OneDrive - UW\\CFD SGS T32\\SurfaceReconstruction\\2.7mm__50%Light_Run2_Calibration_focus0.25turnclockwise"
cal_image_dir = "D:/Barbour/OneDrive - UW/CFD SGS T32/Endoscopies/Endoscopy Day- Dec 21/2.7mm, 0.25 turn, 1mm target (Run 2)/"
cal_image_dir = "D:/Barbour/OneDrive - UW/CFD SGS T32/Patient Endoscopies/Patient 10/Calibration_stack/"
cal_image_files = glob.glob(cal_image_dir + "\\*.JPG")


#%% compute calibration 15/36

filter_params = {"erode kernel size": 5,
                 "threshold constant": 45,
                 "threshold window size": 13,
                 "erode iterations": 2,
                 "dilate iterations": 2}

ret, mtx, dist, rvecs, tvecs = checkerboard_calibration(cal_image_files, 14, 14, 1, filter_params, plot_fail=True, plot_success=True)


#%% - 24/36
filter_params = {"erode kernel size": 3,
                 "threshold constant": 45,
                 "threshold window size": 13,
                 "erode iterations": 2,
                 "dilate iterations": 2}

ret, mtx, dist, rvecs, tvecs = checkerboard_calibration(cal_image_files, 14, 14, 1, filter_params, plot_fail=False, plot_success=False)

#%%
filter_params = {"erode kernel size": 1
                 ,
                 "threshold constant": 45,
                 "threshold window size": 13,
                 "erode iterations": 2,
                 "dilate iterations": 2}

ret, mtx, dist, rvecs, tvecs = checkerboard_calibration(cal_image_files, 14, 14, 1, filter_params, plot_fail=False, plot_success=False)