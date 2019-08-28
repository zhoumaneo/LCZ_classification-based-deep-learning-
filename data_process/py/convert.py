import cv2
import os
import numpy as np
workspace = "C://Users//lsgi//Desktop//site_2_split"
imgs = os.listdir(workspace+"//rs_img//clip")
print(imgs)
rasters = {}
for img in imgs:
    rasters[img.split('.')[0]] = np.array(cv2.imread(workspace+"//rs_img//clip//"+img))
#for index,value in rasters.items():
#    print(index,value.shape)
test = cv2.imread(workspace+"//rs_img//clip//"+"tux-r.jpg")
print(test)
cv2.imshow('show',test)

'''
            h,w = raster.shape[0],raster.shape[1]
            myimg = np.zeros((size,size,3),np.uint8)
            img_x,img_y = 0,0
            for now_y in range(0,size):
                for now_x in range(0,size):
                    if (raster[img_y, img_x, 0] or raster[img_y,img_x,1] or raster[img_y,img_x,2])and:
                        myimg[now_y, now_x, 0] = raster[img_y, img_x, 0]
                        myimg[now_y, now_x, 1] = raster[img_y, img_x, 1]
                        myimg[now_y, now_x, 2] = raster[img_y, img_x, 2]
                        img_x += 1

                    if img_x >= w:
                        img_x = 0
                img_y += 1
                if img_y >= h:
                    img_y = 0
'''