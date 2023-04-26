# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:56:38 2023

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

cal_image_dir = "D:/Barbour/OneDrive - UW/CFD SGS T32/Patient Endoscopies/Patient 09/Calibration_process/"
cal_image_files = glob.glob(cal_image_dir + "\\*.JPG")


#%% compute calibration 7/10

filter_params = {"erode kernel size": 1,
                 "threshold constant": 45,
                 "threshold window size": 13,
                 "erode iterations": 2,
                 "dilate iterations": 2}

ret, mtx, dist, rvecs, tvecs = checkerboard_calibration(cal_image_files, 14, 14, 1, filter_params, plot_fail=True, plot_success=True)