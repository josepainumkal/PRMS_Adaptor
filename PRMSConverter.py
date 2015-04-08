import numpy
import gdal
import drivertiff
import sys

def copyParameterSectionFromInputFile(fileHandle):
    
    """
    Function: copyParameterSectionFromInputFile
    Description: copyParameterSectionFromInputFile function copies the parameter section from the input file to a new file
    """
    
    temporaryFileHandle = open("values.param", 'w')
    foundParameterSection = False
    lines = fileHandle.readlines()
    for line in lines:
        if foundParameterSection or "Parameters" in line:
            temporaryFileHandle.write(line)
            foundParameterSection = True

def passArraytoGdal(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xmin, xmax, ymin, ymax):

    """
    Function: passArraytoGdal
    Description: passArraytoGdal function passes the arrays containing parameter values to GDAL
    """

    xres = xmax - xmin 
    yres = ymax - ymin 
    xavg = xres/numberOfRows
    yavg = yres/numberOfColumns

    outputFormat = 'gtiff'
    
    for j in range(numberOfColumns): 
        for k in range(numberOfRows):
            value = float(fileHandle.next().strip())
            parameterNames[index][j,k] = value
    drivertiff.writeRaster(nameOfOutputFile, parameterNames[index], numberOfRows, numberOfColumns, xavg, yavg, latitude, longitude, epsgValue, driver = outputFormat)

def parameterValuesToAnArray(numberOfRows, numberOfColumns, epsgValue, latitude, longitude, xmin, xmax, ymin, ymax):
    
    """
    Function: parameterValuesToAnArray
    Description: parameterValuesToAnArray function stores the parameter values to an array with parameter name as the array name
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
                nameOfOutputFile = nameOfParameter+".tif"
                passArraytoGdal(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xmin, xmax, ymin, ymax)
                
            elif numberOfValues == 56448:
                for i in range(12):
                    parameterNames.append(nameOfParameter)
                    parameterNames[index] = numpy.arange(4704).reshape(numberOfColumns, numberOfRows)
                    nameOfOutputFile = nameOfParameter+"_"+monthNames[monthIndex]+".tif"
                    passArraytoGdal(nameOfOutputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows, epsgValue, latitude, longitude, xmin, xmax, ymin, ymax)
                    monthIndex = monthIndex + 1
                monthIndex = 0
            index = index + 1        
           
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
	    fileHandle = open(XYDAT, 'r')
            f = open('XY.DAT')
	   
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
            
    fileHandle = open(PRMSDataDirectory, 'r')
    copyParameterSectionFromInputFile(fileHandle)
    parameterValuesToAnArray(numberOfRows, numberOfColumns, epsgValue, latitude, longitude, xmin, xmax, ymin, ymax)









