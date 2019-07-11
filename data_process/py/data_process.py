# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 14:31
# @Author  : zhoumaneo
# @Blog    ：https://zhoumaneo.github.io/

import arcpy
import os

workspace = "C://Users//lsgi//Desktop//data_process"
shp_file = "C://Users//lsgi//Desktop//data_process//shp"

# convert network to polygon return a list of polygons
def features_to_polygon(shp_file,clusTol):
    site_poly = []
    arcpy.env.workspace = shp_file + "//line"
    features = arcpy.ListFeatureClasses("*","line")
    for feature in features:
        outFeature =".//polygon" + feature.split('.')[0]+".shp"
        arcpy.FeatureToPolygon_management(feature,outFeature,clusTol,"NO_ATTRIBUTES","")
        site_poly.append(outFeature)
    return site_poly

# add field for split
def add_field(shp_file,fieldname):
    arcpy.env.workspace = shp_file + "//polygon"
    sites = arcpy.ListFeatureClasses("*","polygon")
    for site in sites:
        try:
            arcpy.AddField_management(site,fieldname,"TEXT",field_length=50)
            arcpy.CalculateField_management(site,fieldname,'!FID!',"PYTHON3")
        except:
            print(site + 'add_field or field calculation fail')
            pass
# split polygon to subpolygons
def split_polygon(shp_file,fieldname):
    arcpy.env.workspace = shp_file + "//polygon"
    sites = arcpy.ListFeatureClasses("*", "polygon")
    for site in sites:
        try:
            os.mkdir(site.split('.')[0])
        except:
            print("split")

def extraction_by_mask(rs_img,vector):
    arcpy.CheckOutExtension("spatial")
    arcpy.gp.overwriteOutput = 1
    arcpy.env.workspace = vector
    raster = rs_img
    masks = arcpy.ListFeatureClasses("*","polygon")
    for mask in masks:
        out = workspace + "//rs_imgs//sites_clips//" + mask.split('.')[0]+".tif"
        arcpy.gp.ExtractByMask_sa(raster,mask,out)
    print("=====================extraction success!====================")
