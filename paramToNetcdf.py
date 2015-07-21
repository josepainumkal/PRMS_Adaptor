import numpy, gdal, osr, sys, os, shutil, glob, netCDF4

def findAverageResolution(XYDAT):

    """

        findAverageResolution finds out the average resolution of the dataset from the XT.DAT file. xmin, xmax, ymin and ymax are
        minimum and maximum resolution of the datset.

	Args:
            XYDAT: input file containing the resolution values

    """

    fileHandle = open(XYDAT, 'r')

    data = fileHandle.readline()
    words = data.split()
    latitude =  float(words[1])
    longitude = float(words[2])

    listOfXHRUCells = []
    listOfYHRUCells = []
    rows = (row.strip().split() for row in fileHandle)
    column = zip(*(row for row in rows if row))

    for i in column[1]:
        listOfXHRUCells.append(float(i))
        xmin = min(listOfXHRUCells)
        xmax = max(listOfXHRUCells)

    for j in column[-1]:
        listOfYHRUCells.append(float(j))
        ymin = min(listOfYHRUCells)
        ymax = max(listOfYHRUCells)

    xres = xmax - xmin
    yres = ymax - ymin
    xavg = xres/numberOfRows
    yavg = yres/numberOfColumns

    return latitude, longitude, xavg, yavg

def copyParameterSectionFromInputFile(fileHandle):

    """

    copyParameterSectionFromInputFile function copies the parameter section from the input file to a new file 'values.param'.

    Args:
        fileHandle: The input file

    """


    temporaryFileHandle = open("values.param", 'w')
    foundParameterSection = False
    lines = fileHandle.readlines()
    for line in lines:
        if foundParameterSection or "Parameters" in line:
            temporaryFileHandle.write(line)
            foundParameterSection = True

def readFile(numberOfRows, numberOfColumns, epsgValue, latitude, longitude, xavg, yavg):

    """

        readFile function reads the file 'values.param'. The parameter names are appended into a list. The
        parameter names are the names of output files. A numpy array is initialized with the number of hru
        cells and is reshaped into row and column size given by the user. The values are then passed over
        to storeValuesinArray function.

        Args:

	    numberOfROws (int): numberOfRows in the dataset
            numberOfColumns (int): numberOfColumns in the dataset
            epsgValue (int): EPSG code of the dataset. This is for projection information.
            latitude (float): Latitude origin of the dataset
            longitude (float): Longitude origin of the dataset
            xavg, yavg (float):  Average resolution of the dataset

    """

    index = 0
    monthIndex = 0
    parameterNames = []
    monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    fileHandle = open("values.param", 'r')
    for line in fileHandle:
        if "####" in line:
            nameOfParameter = fileHandle.next().strip()
            parameterNames.append(nameOfParameter)
            numberOfDimensions = int(fileHandle.next())
            for i in range(numberOfDimensions):
                fileHandle.next()
            numberOfValues = int(fileHandle.next())
            typeOfValues = int(fileHandle.next())

            if numberOfValues == 4704:
                parameterNames.append(nameOfParameter)
                parameterNames[index] = numpy.arange(4704).reshape(numberOfColumns, numberOfRows)
                nameOfOutputFile = nameOfParameter+".nc"
                storeValuesInArray(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xavg, yavg)

            if numberOfDimensions == 2:
                for i in range(12):
                    parameterNames.append(nameOfParameter)
                    parameterNames[index] = numpy.arange(4704).reshape(numberOfColumns, numberOfRows)
                    nameOfOutputFile = nameOfParameter+"_"+monthNames[monthIndex]+".nc"
                    storeValuesInArray(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xavg, yavg)
                    monthIndex = monthIndex + 1
                monthIndex = 0
            index = index + 1

def storeValuesInArray(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xavg, yavg):

    """

    storeValuesInArray stores the parameter values in a 2D array and is appended to a list. The list is
    then passed over to the writeRaster function

    """

    listOfArrays = []
    outputFormat = 'netcdf'

    for j in range(numberOfColumns):
        for k in range(numberOfRows):
            value = float(fileHandle.next().strip())
            parameterNames[index][j,k] = value
    listOfArrays.append(parameterNames[index])

    for elements in listOfArrays:
        if numberOfColumns != len(elements):
            print "Failure"
        for rows in elements:
            if numberOfRows != len(rows):
                print "Failure"
    writeRaster(nameOfOutputFile, listOfArrays, numberOfRows, numberOfColumns, xavg, yavg, latitude, longitude, epsgValue, driver = outputFormat)

def writeRaster(nameOfOutputFile, data, numberOfRows, numberOfColumns, xavg, yavg, latitude, longitude, epsgValue, multipleFiles = False, driver = 'netcdf', datatype = gdal.GDT_Float32):

    """ writeRaster function takes the list containing array of parameter values obtained from storeValuesInArray function and creates a gdal dataset and netcdf files based on the array.

        Args:
            nameOfOutputFile (string): Name of generated NetCDF file. Each output file will have the name of parameter.
            data (array): A numpy array with parameter values
            numberOfRows (int): Number of rows
            numberOfColumns (int): Number of columns
            xavg, yavg (float): average resolution of the dataset
            latitude (float): Latitude origin of the dataset
            longitude (float): Longitude origin of the dataset
	    epsgValue (int): EPSG code of the dataset. This is for projection information.
	    multipleFiles: Determines whether or not a single file or multiple file for multiple datsets that are passed in.
            		   For example, if multipleFiles = True, output name for the parameter rain_adj will be rain_adj_0...rain_adj_n for n 				   files. If multipleFile = False, output name for the parameter will be rain_adj_January...rain_adj_December for 12 				   files.
	    driver (string): Calls netcdf driver
            datatype: GDAL datatype

    """
    # Determining amount of bands to use based on number of items in data
    numberOfBands = len(data)

    # Determining whether multiple files need to be used or not.
    multipleFiles = (numberOfBands > 1) and multipleFiles

    print "EPSG", epsgValue
    #print headers
    # Register all gdal drivers with gdal
    gdal.AllRegister()

    # Grab the specific driver need in this case the one for geotiffs.
    # This could be used with other formats!
    driver = gdal.GetDriverByName(driver)
    print driver
    try:
        if not multipleFiles:
            ds = driver.Create(nameOfOutputFile, numberOfRows, numberOfColumns, numberOfBands, datatype, [])
        else:
            ds = []
            for i in range(0,numberOfBands):
                ds.append(driver.Create(nameOfOutputFile+"."+str(i)+".nc", numberOfRows, numberOfColumns, 1, datatype, []))
    except Exception as e:
        print "ERROR:"
        print e

    # Here I am assuming that north is up in this projection
    # Some more bad apples here.
    if yavg > 0:
        yavg *= -1
    geoTransform = (longitude, xavg, 0, latitude, 0, yavg)
    print geoTransform

    if not multipleFiles:
        ds.SetGeoTransform(geoTransform)
    else:
        for i in ds:
            i.SetGeoTransform(geoTransform)

    #Write out datatype
    for i in xrange(0,numberOfBands):
        if multipleFiles:
            band = ds[i].GetRasterBand(i+1)
        else:
            band = ds.GetRasterBand(i+1)
        band.WriteArray(numpy.array(data[i],dtype=numpy.float32),0,0)

    # apply projection to data
    if epsgValue != -1:
        print "EPSG", epsgValue
        try:
            # First create a new spatial reference
            sr = osr.SpatialReference()

            # Second specify the EPSG map code to be used
            if 6 == sr.ImportFromEPSG(epsgValue):
                print "IGNORING EPSG VALUE TO SPECIFIED REASON"
                return

            # Third apply this projection to the dataset(s)
            if not multipleFiles:
                ds.SetProjection(sr.ExportToWkt())
            else:
                for i in ds:
                    i.SetProjection(sr.ExportToWkt())
            print sr
        except:
            print "IGNORING EPSG VALUE"
            
def generateMetaData():
    
    """ 
        generateMetaData function generates metadata to the output NetCDF files.
    """
    source = os.listdir(os.getcwd())
    for files in source:
        if files.endswith(".nc"):
            
            # initialize new dataset
            ncfile = netCDF4.Dataset(files, mode='r+', format='NETCDF4_CLASSIC')
            
            # add attributes, all global; see CF standards
	    ncfile.title = files
            ncfile.source = 'PRMS Parameter File for Lehman Creek'
	    
            # to save the file to disk, close the `ncfile` object
	    ncfile.close()

def moveFilesToANewDirectory():

    """
        moveFilesToANewDirectory function moves the NetCDF files in the current working directory to a new
        directory.
    """
    directoryName = "NetCDF Files"

    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

    if os.path.exists(directoryName):
        shutil.rmtree(directoryName)
        os.makedirs(directoryName)

    source = os.listdir(os.getcwd())
    for files in source:
        if files.endswith(".nc"):
            shutil.move(files, directoryName)

if __name__ == "__main__":

    numberOfArgs = len(sys.argv)
    for i in range(numberOfArgs):
        if sys.argv[i] == "-r":
	    numberOfRows = int(sys.argv[i+1])

        elif sys.argv[i] ==  "-c":
	    numberOfColumns = int(sys.argv[i+1])

        elif sys.argv[i] == "-data":
	    PRMSDataDirectory = sys.argv[i+1]

        elif sys.argv[i] == "-epsg":
	    epsgValue = int(sys.argv[i+1])

	elif sys.argv[i] == "-hru_cells":
	    XYDAT = sys.argv[i+1]

    values = findAverageResolution(XYDAT)
    fileHandle = open(PRMSDataDirectory, 'r')
    copyParameterSectionFromInputFile(fileHandle)
    readFile(numberOfRows, numberOfColumns, epsgValue, values[0], values[1], values[2], values[3])
    generateMetaData()
    moveFilesToANewDirectory()
