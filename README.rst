PRMS Adaptor
============

In order for PRMS data to be interoperable with the rest of the Virtual
Watershed (VW) ecosystem, we need to be able to convert to NetCDF format,
the reference data format of the VW. To do this we've developed the PRMS
adaptors as an element of the growing suite of VW adaptors. 

How to use them
---------------

.. code-block:: python 
    
    """
        In writeRaster function, gdal is used to convert PRMS to NetCDF format. 
        For this, PRMS data are passed as an array into the function.
    """
    import gdal
   
    # Register all gdal drivers with gdal
    gdal.AllRegister()
    #Grab the specific driver, NetCDF in this case
    driver = gdal.GetDriverByName(driver)
    print driver
    try:
       if not multiple_files:
          ds = driver.Create(outfile,xsize,ysize,nbands,datatype,[])
       else:
          ds = []
          for i in range(0,nbands):
             ds.append(driver.Create(outfile+"."+str(i)+".nc",xsize,ysize,1,datatype,[]))
    except:
       print "ERROR"
      

Module Documentation
--------------------

The input paramet file contains a set of parameters with a number of values for each hru (Hydrologic Response Unit). Some parameters are space related. There are 4704 grid cells that each cell represents one location of the watershed, 
and there is one value for each of the cell. These parameters do not have time features. Some parameters are time related. There are 12 months in a year, so there is a value for each of a month. These parameters do not have space features.
Other parameters are both space and time related. For each month, there is a value for each of the cell. These parameters have both space and time features. For now, only space related parameters with 4707 values, and space eand time related 
parameters with 56448 values are considered. The values are stored as a list and passed to the gdalDriver.

To convert a ``PRMS`` object to a ``NetCDF`` Dataset, just call
``writeRaster``, which can be found in the ``dataConverter.py`` module.
