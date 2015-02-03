import gdal
import numpy as np
import osr
def writeRaster(outfile,data,xsize,ysize,xres,yres,latitude,longitude,epsg,nbands=1,multibanded=False,multiDataset=False,driver="gtiff"):
   '''
   Function: write_dem
   Descrition: This function takes the data obtained from the ipw file and
   writes it out to a dem through gdal's dataset.
   gdal handles any fileio by itself.
   '''
   print "EPSG",epsg
   #print headers
   # Register all gdal drivers with gdal
   gdal.AllRegister()
   
   # Outputing my data as 32 bit floats
   datatype = gdal.GDT_Float32

   # Grab the specific driver need in this case the one for geotiffs.
   # This could be used with other formats!
   driver = gdal.GetDriverByName(driver)
   print driver
   try:
      if not multibanded:
         ds = driver.Create(outfile,xsize,ysize,nbands,datatype,[])
      else:
         ds = []
         for i in range(0,nbands):
            ds.append(driver.Create(outfile+"."+str(i)+".tif",xsize,ysize,1,datatype,[]))
   except:
      print "ERROR"
   
   # Here I am assuming that north is up in this projection
   # Some more bad apples here.
   if ysize > 0:
      ysize *= -1
   geoTransform = (longitude,xsize,0,latitude,0,ysize)
   print geoTransform

   if not multibanded:
      ds.SetGeoTransform(geoTransform)
   else:
      for i in ds:
         i.SetGeoTransform(geoTransform)

   #Write out datatype
   for i in xrange(0,nbands):
      #print len(ds)
      if nbands > 1 and multibanded:
         band = ds[i].GetRasterBand(i+1)
      else:
         band = ds.GetRasterBand(i+1)
      if multiDataset:
         band.WriteArray(np.array(data[i],dtype=np.float32),0,0)
      else:
         band.WriteArray(np.array(data,dtype=np.float32),0,0)
      
   # apply projection to data
   if epsg != -1:
     print "EPSG", epsg
     try:
         # First create a new spatial reference
         sr = osr.SpatialReference()

         # Second specify the EPSG map code to be used
         if 6 == sr.ImportFromEPSG(epsg):
            print "IGNORING EPSG VALUE TO SPECIFIED REASON"
            return

         # Third apply this projection to the dataset(s)
         if not multibanded:
            ds.SetProjection(sr.ExportToWkt())
         else:
            for i in ds:
               i.SetProjection(sr.ExportToWkt())
         print sr
     except:
         print "IGNORING EPSG VALUE"

#writeRaster("out.tif",[[1,2,3],[1,2,3]],3,2,1.0,1.0,108,101,4326,driver='gtiff')
