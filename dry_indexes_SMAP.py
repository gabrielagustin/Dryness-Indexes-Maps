#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 07:02:59 2018

@author: gag
"""

import matplotlib.pyplot as plt
import functions
from mpl_toolkits.axes_grid1 import make_axes_locatable



### previamente se obtienen los maximos y minimos para la
### temperatura de superficie y la humedad de suelo
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
dir = "gag"
# dir = "stanza"

path = "/media/"+dir+"/Datos/Estancia_Italia_2018/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/Indices/"


for i in range(0,len(fechaSMAP)):

    print(fechaSMAP[i])

    nameFileTCI = "TCI_"+str(fechaSMAP[i])
    nameFileHSCI= "HSCI_"+str(fechaSMAP[i])
    ####------------------------------------------------------------------------
   
    ### humedad de suelo de SMAP 9km
    fileSmap = "/media/"+dir+"/Datos/Estancia_Italia_2018/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/"+fechaSMAP[i]+"/soil_moisture.img"
    src_ds_Smap, bandSmap, GeoTSmap, ProjectSmap = functions.openFileHDF(fileSmap, 1)

    ### temperatura de superficie de SMAP 9km
    fileTs = "/media/"+dir+"/Datos/Estancia_Italia_2018/Trabajo_Sentinel_NDVI_CONAE/SMAP/SMAP-10km/"+fechaSMAP[i]+"/surface_temperature.img"
    src_ds_Ts, bandTs, GeoTTs, ProjectTs = functions.openFileHDF(fileTs, 1)
    ####------------------------------------------------------------------------

    ##### SM recorte 
    fileSMAP_subset = "/media/"+dir+"/TOURO Mobile/SMAP/SMAP_L3_SM_P_E/subset_0_of_SMAP_L3_SM_P_E_20150414_R14010_001.data/soil_moisture.img"
    src_ds_Smap_subset, bandSmap_subset, GeoTSmap_subset, ProjectSmap_subset = functions.openFileHDF(fileSMAP_subset, 1)
    ####------------------------------------------------------------------------

    transform = GeoTSmap_subset
    xmin,xmax,ymin,ymax=transform[0],transform[0]+transform[1]*src_ds_Smap_subset.RasterXSize,transform[3]+transform[5]*src_ds_Smap_subset.RasterYSize,transform[3]
    print(xmin)
    print(xmax)





    nRow, nCol = bandSmap_subset.shape

    type = "Nearest"
    data_src = src_ds_Smap
    data_match = src_ds_Smap_subset
    match = functions.matchData(data_src, data_match, type, nRow, nCol)
    band_matchSM = match.ReadAsArray()

   
    data_src = src_ds_Ts
    data_match = src_ds_Smap_subset
    match = functions.matchData(data_src, data_match, type, nRow, nCol)
    band_matchTs = match.ReadAsArray()  


    ### Temperature Condition Index (TCI)
    TCI = (Ts_Max - band_matchTs) /(Ts_Max - Ts_Min)
    
    ### The normalized soil moisture indexes (HSCI)
    HSCI = (SM_Max - band_matchSM)/(SM_Max - SM_Min)


    fig, ax = plt.subplots()
    im0 = ax.imshow(TCI, extent=[xmin,xmax,ymin,ymax], interpolation='None',cmap='gray')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im0, cax=cax)
    ax.set_title('Temperature Condition Index (TCI)')
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    # ax.xaxis.tick_top()

    fig, ax = plt.subplots()
    im1 = ax.imshow(HSCI, extent=[xmin,xmax,ymin,ymax], interpolation='None',cmap='gray')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im1, cax=cax)
    ax.set_title('Normalized soil moisture indexes (HSCI)')
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))


    plt.show()


    functions.createHDFfile(path, nameFileTCI, 'ENVI', TCI, nCol, nRow, GeoTSmap_subset, ProjectSmap_subset)
    functions.createHDFfile(path, nameFileHSCI, 'ENVI', HSCI, nCol, nRow, GeoTSmap_subset, ProjectSmap_subset)


print("FIN")

