# -*- coding: utf-8 -*-
# @Time    : 2019/7/21 15:35
# @Author  : zhoumaneo
# @Blog    ：https://zhoumaneo.github.io/
import cv2
import numpy as np
import os
workspace = "D://ArcGIS_Project//site_2_split"
imgs = os.listdir(workspace+"//rs_img//clip")
for img in imgs:
    mask = cv2.imread(workspace+"//rs_img//site2_clip//"+img)
    cv2.imwrite(workspace + "//rs_img//mask//" + "mask_" + img.split('.')[0]+'.jpg', mask, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
