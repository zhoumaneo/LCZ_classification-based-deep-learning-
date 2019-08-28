# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 14:18
# @Author  : zhoumaneo
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gdal
import os
import math

workspace = "D://ArcGIS_Project//site_2_split"
path = workspace + "//rs_img//site2_clip//"
def rotate(path):
    imgs = os.listdir(path)
    for img in imgs:
        try:
            raster = gdal.Open(path + img)
            rb = raster.GetRasterBand(3)
            gb = raster.GetRasterBand(2)
            bb = raster.GetRasterBand(1)
            rb_array = rb.ReadAsArray()
            gb_array = gb.ReadAsArray()
            bb_array = bb.ReadAsArray()
            raster = np.dstack((rb_array, gb_array, bb_array))
# ================== make a mask for raster =================
            gray = cv2.cvtColor(raster,cv2.COLOR_BGR2GRAY)
            gray[gray != 65535] = 1
            gray[gray == 65535] = 0
# ================== rotate the raw img =====================
            ret1,img1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
            img1 = np.uint8(img1)
            contours1, hierarchy1 = cv2.findContours(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rect1 = cv2.minAreaRect(contours1[0])
            (h, w) = raster.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, rect1[2], scale=1.0)
            rotated = cv2.warpAffine(raster, M, (w, h), borderValue=(255, 255, 255))
# ================== rotate mask ============================
            rotate_mask = cv2.warpAffine(img1,M,(w,h))
            contours2, hierarchy2 = cv2.findContours(rotate_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rect2 = cv2.minAreaRect(contours2[0])
            box = cv2.boxPoints(rect2)
            box = np.int0(box)
            y0, y1, x0, x1 = min(box[0][1], box[2][1]), max(box[0][1], box[2][1]), min(box[0][0], box[2][0]), max(box[0][0], box[2][0])
            crop_rota_img = rotated[y0:y1, x0:x1]
            crop_rota_img = np.uint8(crop_rota_img)
            rotate_mask_clip = rotate_mask[y0:y1,x0:x1]
            cv2.imwrite(workspace + "//rs_img//mask//"+"mask_"+img,rotate_mask_clip,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])
#           cv2.imwrite(workspace + "//rs_img//rotate_clip//" + "rota_clip_" + img, crop_rota_img,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        except:
            print(img + "----------->rotate_clip_fail")
rotate(path=path)