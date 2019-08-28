# -*- coding: utf-8 -*-
# @Time    : 2019/7/21 14:18
# @Author  : zhoumaneo
# @Blog    ：https://zhoumaneo.github.io/
import cv2
import numpy as np
import gdal
import os

workspace = "D://ArcGIS_Project//site_2_split"
imgs = os.listdir(workspace+"//rs_img//rotate_clip")
mask = os.listdir(workspace+"//rs_img//mask")

for img in imgs:
    raster = gdal.Open(workspace + "//rs_img//rotate_clip//" + img)
    mask = gdal.Open(workspace+"//rs_img//mask//mask_site2_"+img.split('_')[3])
    rb = raster.GetRasterBand(3)
    gb = raster.GetRasterBand(2)
    bb = raster.GetRasterBand(1)
    rb_array = rb.ReadAsArray()
    gb_array = gb.ReadAsArray()
    bb_array = bb.ReadAsArray()
    raster = np.dstack((rb_array, gb_array, bb_array))
    mb = mask.GetRasterBand(1)
    mask = mb.ReadAsArray()
    (h,w) = raster.shape[:2]
# =========================== h,w <= 64 =========================
    if h <= 64 and w <= 64:
        newimg = np.zeros((h, w, 3), np.uint8)
        img_x, img_y = 0, 0
        try:
            for i in range(h):
                for j in range(w):
                    if mask[i, j] != 255:
                        if i <= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y += 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y -= 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j >= w / 2:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y -= 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                        else:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y += 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                    else:
                        newimg[i, j, 0] = raster[i, j, 0]
                        newimg[i, j, 1] = raster[i, j, 1]
                        newimg[i, j, 2] = raster[i, j, 2]
            a = cv2.copyMakeBorder(newimg, int((64 - h) / 2), int((64 - h) / 2), int((64 - w) / 2), int((64 - w) / 2),cv2.BORDER_REFLECT)
            cv2.imwrite(workspace + "//rs_img//nor_clip//" + "nor_" + img, a, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        except:
            print(img + "====================>nor fail")
            pass
# =========================== h > 64,w < 64 =========================
    elif h > 64 and w < 64:
        maxi = [0,0]
        for i in range(h):
            sub = mask[i:i+64]
            num = len(sub[sub==255])
            if num > maxi[0]:
                maxi[0] = num
                maxi[1] = i
        raster = raster[maxi[1]:maxi[1]+64]
        mask = mask[maxi[1]:maxi[1]+64]
        (h,w) = raster.shape[:2]
        newimg = np.zeros((h, w, 3), np.uint8)
        img_x, img_y = 0, 0
        try:
            for i in range(h):
                for j in range(w):
                    if mask[i, j] != 255:
                        if i <= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y += 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y -= 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j >= w / 2:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y -= 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                        else:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y += 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                    else:
                        newimg[i, j, 0] = raster[i, j, 0]
                        newimg[i, j, 1] = raster[i, j, 1]
                        newimg[i, j, 2] = raster[i, j, 2]
            a = cv2.copyMakeBorder(newimg, int((64 - h) / 2), int((64 - h) / 2), int((64 - w) / 2), int((64 - w) / 2),cv2.BORDER_REFLECT)
            cv2.imwrite(workspace + "//rs_img//nor_clip//" + "nor_" + img, a, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        except:
            print(img + "====================>nor fail")
            pass
# =========================== h < 64,w > 64 =========================
    elif h < 64 and w > 64:
        maxi = [0,0]
        for i in range(w):
            sub = mask[:,i:i+64]
            num = len(sub[sub==255])
            if num > maxi[0]:
                maxi[0] = num
                maxi[1] = i
        raster = raster[:,maxi[1]:maxi[1]+64]
        mask = mask[:,maxi[1]:maxi[1]+64]
        (h,w) = raster.shape[:2]
        newimg = np.zeros((h, w, 3), np.uint8)
        img_x, img_y = 0, 0
        try:
            for i in range(h):
                for j in range(w):
                    if mask[i, j] != 255:
                        if i <= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y += 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y -= 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j >= w / 2:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y -= 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                        else:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y += 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                    else:
                        newimg[i, j, 0] = raster[i, j, 0]
                        newimg[i, j, 1] = raster[i, j, 1]
                        newimg[i, j, 2] = raster[i, j, 2]
            a = cv2.copyMakeBorder(newimg, int((64 - h) / 2), int((64 - h) / 2), int((64 - w) / 2), int((64 - w) / 2),cv2.BORDER_REFLECT)
            cv2.imwrite(workspace + "//rs_img//nor_clip//" + "nor_" + img, a, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        except:
            print(img + "====================>nor fail")
            pass
# =========================== h > 64,w > 64 =========================
    else:
        maxi = [0,0,0]
        for i in range(h):
            for j in range(w):
                a = mask[i:i+64,j:j+64]
                num = len(a[a==255])
                if num > maxi[0]:
                    maxi[0] = num
                    maxi[1] = i
                    maxi[2] = j
        raster = raster[maxi[1]:maxi[1]+64,maxi[2]:maxi[2]+64]
        mask = mask[maxi[1]:maxi[1]+64,maxi[2]:maxi[2]+64]
        (h,w) = raster.shape[:2]
        newimg = np.zeros((h, w, 3), np.uint8)
        img_x, img_y = 0, 0
        try:
            for i in range(h):
                for j in range(w):
                    if mask[i, j] != 255:
                        if i <= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y += 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j <= w / 2:
                            if i != img_y:
                                img_x = 0
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x += 1
                                if img_x >= w:
                                    img_y -= 1
                                    img_x = 0
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x += 1
                            if img_x >= w:
                                img_x = 0
                        elif i >= h / 2 and j >= w / 2:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y -= 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                        else:
                            if i != img_y:
                                img_x = w - 1
                                img_y = i
                            while (mask[img_y, img_x] != 255):
                                img_x -= 1
                                if img_x <= 0:
                                    img_y += 1
                                    img_x = w - 1
                            newimg[i, j, 0] = raster[img_y, img_x, 0]
                            newimg[i, j, 1] = raster[img_y, img_x, 1]
                            newimg[i, j, 2] = raster[img_y, img_x, 2]
                            img_x -= 1
                            if img_x <= 0:
                                img_x = w - 1
                    else:
                        newimg[i, j, 0] = raster[i, j, 0]
                        newimg[i, j, 1] = raster[i, j, 1]
                        newimg[i, j, 2] = raster[i, j, 2]
            a = cv2.copyMakeBorder(newimg, int((64 - h) / 2), int((64 - h) / 2), int((64 - w) / 2), int((64 - w) / 2),cv2.BORDER_REFLECT)
            cv2.imwrite(workspace + "//rs_img//nor_clip//" + "nor_" + img, a, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        except:
            print(img + "====================>nor fail")
            pass

        cv2.imwrite(workspace + "//rs_img//nor_clip//" + "nor_" + img, raster, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])


