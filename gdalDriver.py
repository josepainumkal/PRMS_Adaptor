import gdal
import numpy
import osr

def writeRaster(outfile,data,xsize,ysize,xres,yres,longitude,latitude, epsg,nbands=1,multibanded=False,multiDataset=False,driver="netcdf"):
   
   """
   Function: writeRaster
   Descrition: This function takes the data obtained from the ipw file 
   and writes it out to a dem through gdal's dataset. gdal handles any 
   fileio by itself.
   """

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
            ds.append(driver.Create(outfile+"."+str(i)+".nc",xsize,ysize,1,datatype,[]))
   except:
      print "ERROR"
   
   # Here I am assuming that north is up in this projection
   # Some more bad apples here.
   if yres > 0:
      yres *= -1
   geoTransform = (longitude,xres,0,latitude,0,yres)
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
         band.WriteArray(numpy.array(data[i],dtype=numpy.float32),0,0)
      else:
         band.WriteArray(numpy.array(data,dtype=numpy.float32),0,0)
      
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


