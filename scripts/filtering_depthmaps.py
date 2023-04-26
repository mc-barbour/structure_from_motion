# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:54:55 2023

@author: barbourm
"""


import numpy as np
import glob
import struct
import plotly.graph_objects as go
import plotly.express as px
import cv2 as cv

import plotly.io as pio
from plotly.subplots import make_subplots

from source.image_filters import *
from source.image_io import *

pio.renderers.default = "browser"

#%% Load files

dense_recon_dir = "D:\\Barbour\\OneDrive - UW\\CFD SGS T32\\SurfaceReconstruction\\3DPrinted_models_20221221\\2.7mm_0.25turn_Model4_wet_freehand\\laryngascope_dense_reconstruction\\"
depth_maps_photometric = glob.glob(dense_recon_dir + "stereo\\depth_maps\\*.photometric*")
depth_maps_geometric = glob.glob(dense_recon_dir + "stereo\\depth_maps\\*.geometric*")

#%% define the circular mask
depth_map = read_array(depth_maps_photometric[15])
truncated_map = truncate_filter(depth_map)

radius = 580
cx = 740
cy = 560

define_mask(truncated_map, radius, cx, cy)

#%% Apply filters to all depth maps
new_dir = "D:\\Barbour\\OneDrive - UW\\CFD SGS T32\\SurfaceReconstruction\\3DPrinted_models_20221221\\2.7mm_0.25turn_Model4_wet_freehand\\laryngascope_dense_reconstruction_filtered\\stereo\\depth_maps\\"
filter_depth_maps(depth_maps_photometric, depth_maps_geometric, new_dir, radius, cx, cy)