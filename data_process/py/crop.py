# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 21:17
# @Author  : zhoumaneo
# @Blog    ：https://zhoumaneo.github.io/
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gdal
import os
import math

workspace = "D://ArcGIS_Project//site_2_split"
imgs = os.listdir(workspace+"//rs_img//clip")
for img in imgs:
    try:
        raster = gdal.Open(workspace + "//rs_img//clip//" + img)
        rb = raster.GetRasterBand(3)
        gb = raster.GetRasterBand(2)
        bb = raster.GetRasterBand(1)
        rb_array = rb.ReadAsArray()
        gb_array = gb.ReadAsArray()
        bb_array = bb.ReadAsArray()
        raster = np.dstack((rb_array, gb_array, bb_array))
        gray = cv2.cvtColor(raster,cv2.COLOR_BGR2GRAY)
        ret,img2 = cv2.threshold(gray,254,255,cv2.THRESH_BINARY)
        img2[img2 == 0] = 1
        img2[img2 == 255] = 0
        contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda k: len(k), reverse=True)
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        y0,y1,x0,x1 = min(box[0][1],box[2][1]),max(box[0][1],box[2][1]),min(box[0][0],box[2][0]),max(box[0][0],box[2][0])
        crop_rota_img = raster[y0:y1,x0:x1]
        cv2.imwrite(workspace+"//rs_img//clip//"+"crop_"+img,crop_rota_img,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    except:
        print(img + "----------->rotate_clip_fail")