# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:46:13 2023

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

pio.renderers.default = "browser"


def filter_image(img, filter_params, board_size_row=9, board_size_col=9):
    
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    median = cv.medianBlur(gray, 5)
    kernel = np.ones((filter_params["erode kernel size"], filter_params["erode kernel size"]), np.uint8)
    
    adaptive_thresh = cv.adaptiveThreshold(median, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                           cv.THRESH_BINARY, filter_params["threshold constant"], filter_params["threshold window size"])

    img_erode = cv.erode(adaptive_thresh, kernel, iterations=filter_params["erode iterations"])
    img_dilate = cv.dilate(img_erode, kernel, iterations=filter_params["dilate iterations"])

    return img_dilate






def checkerboard_calibration(cal_image_files, board_size_row, board_size_col, board_size, filter_params, plot_fail=False, plot_success=False):
    
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    img_points = []

    for count, img_file in enumerate(cal_image_files):
        
        img = cv.imread(img_file)
        # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # median = cv.medianBlur(gray, 5)
        # kernel = np.ones((5, 5), np.uint8)

        # adaptive_thresh = cv.adaptiveThreshold(median, 255, cv.ADAPTIVE_THRESH_MEAN_C,
        #                                        cv.THRESH_BINARY, 145, 10)

        # img_erode = cv.erode(adaptive_thresh, kernel, iterations=2)
        # img_dilate = cv.dilate(img_erode, kernel, iterations=2)
        filtered_image = filter_image(img, filter_params, board_size_row=9, board_size_col=9)

        ret, corners = cv.findChessboardCorners(filtered_image, (board_size_row, board_size_col), cv.CALIB_CB_FILTER_QUADS)
        print("Found Checkerboard:" , ret, img_file.split("\\")[-1])
        
        if ret:
            corners_refined = cv.cornerSubPix(filtered_image, corners, (11,11), (-1,-1), criteria)
            
            img_points.append(corners_refined)
            
            corners_reshape = np.reshape(corners_refined, (board_size_row*board_size_col,2))
            X = corners_reshape[:,0]
            Y = corners_reshape[:,1]
        
            if plot_success:
                fig = px.imshow(filtered_image)
                fig.add_trace(go.Scatter(x=X, y=Y, mode='markers', marker_color='red'))
                fig.show()
            
        elif plot_fail:
            fig = px.imshow(filtered_image)
            fig.show()
        

            
    print("Corners detected in {:d} out of {:d} images".format(len(img_points), count+1))    
    # define object points
    object_points_grid = np.zeros((board_size_row*board_size_col,3), np.float32)
    object_points_grid[:,:2] = np.mgrid[0:board_size_row,0:board_size_col].T.reshape(-1,2)*board_size

    object_points = []

    for count in range(len(img_points)):
        object_points.append(object_points_grid)

    # perform image calibration

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_points, img_points, (img.shape[1],img.shape[0]), None, None)
    print("K Matrix:", mtx)
    print("Dstortion Params:", dist)
    print("ret:", ret)

    mean_error = 0
    for i in range(len(object_points)):
        imgpoints2, _ = cv.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(img_points[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(object_points)) )


    return ret, mtx, dist, rvecs, tvecs
