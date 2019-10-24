# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Created on Mon Sep 10 14:37:54 2018

@author: gag
"""



import numpy as np
from osgeo import gdal, ogr, gdalconst
import sys
import matplotlib.pyplot as plt


def openFileHDF(file, nroBand):
    """Function that opens a raster image

    Parameters:
    -----------
    file : full path of the raster image
    nroBand: number of the band to read

    Returns:
    --------
    src_ds: raster
    band: raster as arrays
    GeoT: raster georeference info
    Project: projections
    """

    try:
        src_ds = gdal.Open(file)
    except (RuntimeError, e):
        print('Unable to open File')
        print(e)
        sys.exit(1)

    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    #print cols
    #print rows
    bands = src_ds.RasterCount
    #print bands

    # se obtienen las caracteristicas de las imagen HDR
    GeoT = src_ds.GetGeoTransform()
    #print GeoT
    Project = src_ds.GetProjection()

    try:
        srcband = src_ds.GetRasterBand(nroBand)
    except(RuntimeError, e):
        # for example, try GetRasterBand(10)
        print('Band ( %i ) not found' % band_num)
        print(e)
        sys.exit(1)
    band = srcband.ReadAsArray()

    return src_ds, band, GeoT, Project



def createHDFfile(nameFileOut, driver, GeoT, Projection, img, nRow, nCol):
    """Function that creates an HDF file based on the Geotransform and Projection 
       data from an original image

    Parameters:
    -----------
    nameFileOut: full path of the raster image to be created
    driver: "GTiff", "netCDF", "MEM",...
    GeoT: raster georeference info
    Project: projections
    img: raster as arrays
    nRow, nCol: number of rows and columns of the image

    Returns:
    --------

    """
    
    print("archivo creado:" + str(nameFileOut))
    driver = gdal.GetDriverByName(driver)
    ds = driver.Create(path + nameFileOut, xsize, ysize, 1, gdal.GDT_Float64)
    ds.SetProjection(Projection)
    geotransform = GeoT
    ds.SetGeoTransform(geotransform)
    ds.GetRasterBand(1).WriteArray(np.array(img))

    return

  
def matchData(data_src, data_src_match, type, nRow, nCol):
    """Function that modifies a raster image based on a source raster. 
       Applies geo-transformation and projection from source raster 
       and modifies the size.
    Parameters:
    -----------
    data_src: source raster
    data_src_match: raster to match
    type: interpolation method to apply. "Nearest", "Bilinear", "Cubic", "Average"
    nRow, nCol: number of rows and columns of the image
    Returns:
    --------
    data_result: raster
    """

    #data_result = gdal.GetDriverByName('MEM').Create('', data_match.RasterXSize, data_match.RasterYSize, 1, gdalconst.GDT_Float64)

    data_result = gdal.GetDriverByName('MEM').Create('', nCol, nRow, 1, gdalconst.GDT_Float64)

    # Se establece el tipo de proyección y transfomcion en resultado  qye va ser coincidente con data_match
    data_result.SetGeoTransform(data_match.GetGeoTransform())
    data_result.SetProjection(data_match.GetProjection())

    # se cambia la proyeccion de data_src, con los datos de data_match y se guarda en data_result
    if (type == "Nearest"):
        gdal.ReprojectImage(data_src,data_result,data_src.GetProjection(),data_match.GetProjection(), gdalconst.GRA_NearestNeighbour)
    if (type == "Bilinear"):
        gdal.ReprojectImage(data_src, data_result, data_src.GetProjection(), data_match.GetProjection(), gdalconst.GRA_Bilinear)
    if (type == "Cubic"):
        gdal.ReprojectImage(data_src, data_result, data_src.GetProjection(), data_match.GetProjection(), gdalconst.GRA_Cubic)
    if (type == "Average"):
        gdal.ReprojectImage(data_src, data_result, data_src.GetProjection(), data_match.GetProjection(), gdal.GRA_Average)

    return data_result


