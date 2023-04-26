# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:30:15 2023

@author: barbourm
"""


import cv2 as cv
import glob
import os
import shutil


image_dir1 =  "D:\\Barbour\\OneDrive - UW\\CFD SGS T32\\Patient Endoscopies\\Patient 09\\SfM_reconstruction\\Endoscopy_trachea\\"
new_image_dir =  "D:\\Barbour\\OneDrive - UW\\CFD SGS T32\\Patient Endoscopies\\Patient 09\\SfM_reconstruction\\Endoscopy_trachea_renumbered\\"

images = glob.glob(image_dir1 + "*.jpg")
print("Found {:d} images to renumber".format(len(images)))
#%%
n_padding = 5
new_start_num = 525

prefix = 'Patient009_endoscopy'
for count, filename in enumerate(images):
    
    image_num = count + new_start_num
    # prefix = filename.split("\\")[-1].split("_")[0]
    new_name = prefix + "_" + str(image_num).zfill(n_padding) + ".jpg"
    
    
    fullname = new_image_dir + new_name
    
    # os.rename(filename, fullname)
    shutil.copyfile(filename, fullname)
    
