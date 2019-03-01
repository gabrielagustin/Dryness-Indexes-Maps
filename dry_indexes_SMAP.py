#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 07:02:59 2018

@author: gag
"""

import gdal
import matplotlib.pyplot as plt
import numpy.ma as np
from matplotlib import cm

from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance

from osgeo import gdal, ogr
import sys
#from scipy.stats import threshold
from scipy import stats
import pandas as pd
import functions
import seaborn as sns

#from mpl_toolkits.basemap import Basemap
from numpy import linspace
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma



SM_Max = 0.499 
SM_Min = 0.1236

Ts_Max = 299.64
Ts_Min = 279.68


fechaSMAP = []

fechaSMAP.append("2015-04-19")

fechaSMAP.append("2015-05-02")

fechaSMAP.append("2015-05-10")

fechaSMAP.append("2015-05-26")

fechaSMAP.append("2015-06-19")

fechaSMAP.append("2015-06-30")

fechaSMAP.append("2015-07-24")

fechaSMAP.append("2015-08-17")

fechaSMAP.append("2015-08-30")

fechaSMAP.append("2015-09-10")

fechaSMAP.append("2015-09-23")

fechaSMAP.append("2015-10-04")

fechaSMAP.append("2015-10-28")

fechaSMAP.append("2015-11-13")

fechaSMAP.append("2015-11-21")

fechaSMAP.append("2015-12-18")

fechaSMAP.append("2015-12-28")

fechaSMAP.append("2016-01-08")

fechaSMAP.append("2016-01-19")

fechaSMAP.append("2016-02-14")

fechaSMAP.append("2016-03-12")

fechaSMAP.append("2016-03-20")

fechaSMAP.append("2016-04-02")

fechaSMAP.append("2016-04-24")

fechaSMAP.append("2016-05-20")


print(len(fechaSMAP))


#dir = "ggarcia"
#dir = "gag"
dir = "stanza"

path = "/media/"+dir+"/TOURO Mobile/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/Indices/"

for i in range(0,len(fechaSMAP)):

    print(fechaSMAP[i])

    nameFileTCI = "TCI_"+str(fechaSMAP[i])
    nameFileHSCI= "HSCI_"+str(fechaSMAP[i])
    ####------------------------------------------------------------------------
   
    ### humedad de suelo de SMAP 9km
    fileSmap = "/media/"+dir+"/TOURO Mobile/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/"+fechaSMAP[i]+"/soil_moisture.img"
    src_ds_Smap, bandSmap, GeoTSmap, ProjectSmap = functions.openFileHDF(fileSmap, 1)

    ### temperatura de superficie de SMAP 9km
    fileTs = "/media/"+dir+"/TOURO Mobile/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/"+fechaSMAP[i]+"/surface_temperature.img"
    src_ds_Ts, bandTs, GeoTTs, ProjectTs = functions.openFileHDF(fileTs, 1)
    ####------------------------------------------------------------------------

    ##### SM recorte 
    fileSMAP_subset = "/media/"+dir+"/TOURO Mobile/SMAP/SMAP_L3_SM_P_E/subset_0_of_SMAP_L3_SM_P_E_20150414_R14010_001.data/soil_moisture.img"
    src_ds_Smap_subset, bandSmap_subset, GeoTSmap_subset, ProjectSmap_subset = functions.openFileHDF(fileSMAP_subset, 1)
    ####------------------------------------------------------------------------

    nRow, nCol = bandSmap_subset.shape

    type = "Nearest"
    data_src = src_ds_Smap
    data_match = src_ds_Smap_subset
    match = functions.matchData(data_src, data_match, type, nRow, nCol)
    band_matchSM = match.ReadAsArray()#  

#    fig, ax = plt.subplots()
#    im0 = ax.imshow(band_matchSM, interpolation='None',cmap='gray')
#    
    data_src = src_ds_Ts
    data_match = src_ds_Smap_subset
    match = functions.matchData(data_src, data_match, type, nRow, nCol)
    band_matchTs = match.ReadAsArray()#  

    TCI = (Ts_Max - band_matchTs) /(Ts_Max - Ts_Min)
    
    HSCI = (SM_Max - band_matchSM)/(SM_Max - SM_Min)


    functions.createHDFfile(path, nameFileTCI, 'ENVI', TCI, nCol, nRow, GeoTSmap_subset, ProjectSmap_subset)
    functions.createHDFfile(path, nameFileHSCI, 'ENVI', HSCI, nCol, nRow, GeoTSmap_subset, ProjectSmap_subset)


print("FIN")
