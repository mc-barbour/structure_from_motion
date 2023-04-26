import glob

import numpy as np
import cv2 as cv


import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

from source.image_io import *

pio.renderers.default = "browser"


def truncate_filter(depth_map, upper_percentage=95, lower_percentage=5):
    "Apply high and low pass filter at 95th and 5th percentile of image"
    min_depth, max_depth = np.percentile(
        depth_map, [lower_percentage, upper_percentage])
    depth_map[depth_map < min_depth] = min_depth
    depth_map[depth_map > max_depth] = max_depth
    
    return depth_map

def mask_image(depth_map, mask):
    "Return masked image"
    return cv.bitwise_and(depth_map, depth_map, mask=mask)

def define_mask(img, radius, cx, cy):
    'Test different cirular mask parameters'
    
    a = np.linspace(0, 2*np.pi, 100)

    x_circ = cx + radius * np.cos(a)
    y_circ = cy + radius * np.sin(a)


    mask = np.zeros(img.shape, dtype="uint8")
    cv.circle(mask, (cx, cy), radius, 255, -1)
    masked = cv.bitwise_and(img, img, mask=mask)

    fig = px.imshow(img)
    fig.add_trace(go.Scatter(x=x_circ, y=y_circ, marker_color='red'))
    fig.show()

    fig = px.imshow(masked)
    fig.show()
    

def filter_depth_maps(photometric_depthmaps, geometric_depthmaps, filtered_depthmap_dir, radius, cx, cy):
    "Save filtered depthmaps in new stereo directory"
    
    if len(glob.glob(filtered_depthmap_dir + "*.photometric*")) != 0:
        raise Exception("depthmap directory is not empty. Breaking to not overwrite original images. Pleas make sure filtered depthmap directory is a new directry")
    
    depth_map = read_array(photometric_depthmaps[0])
    mask = np.zeros(depth_map.shape, dtype="uint8")
    cv.circle(mask, (cx, cy), radius, 255, -1)
    
    print("Saving filtered Geometric Depth maps")
    for img_name in geometric_depthmaps:
        
        
        depth_map = read_array(img_name)
        
        depth_map_filtered = truncate_filter(depth_map)
        depth_map_masked = mask_image(depth_map_filtered, mask)
        save_name = filtered_depthmap_dir + img_name.split("\\")[-1]
        write_array(depth_map_masked, save_name)
        
    print("Saving filtered Photometric Depth maps")
    for img_name in photometric_depthmaps:
        
        
        depth_map = read_array(img_name)
        
        depth_map_filtered = truncate_filter(depth_map)
        depth_map_masked = mask_image(depth_map_filtered, mask)
        save_name = filtered_depthmap_dir + img_name.split("\\")[-1]
        write_array(depth_map_masked, save_name)
