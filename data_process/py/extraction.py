import arcpy
import os
path = os.getcwd()
print(path)
arcpy.CheckOutExtension("spatial")
arcpy.gp.overwriteOutput=1
arcpy.env.workspace = "vectors"
raster = "rs_img\\site2_remote_img_clip.tif"
masks= arcpy.ListFeatureClasses("*","polygon")
for mask in masks:
    print(mask)
    out = "rs_img\\"+"site2_"+mask.split('.')[0]+".tif"
    arcpy.gp.ExtractByMask_sa(raster, mask, out)
    print("site2_" + mask.split('.')[0] + "  has done")

