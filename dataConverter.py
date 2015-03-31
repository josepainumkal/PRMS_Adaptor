import numpy
import gdal
import gdalDriver
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

def passArraytoGdal(nameOfOuputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows):

    """
    Function: passArraytoGdal
    Description: passArraytoGdal function passes the arrays containing parameter values to GDAL
    """

    xMin = -114.323106
    yMax = 39.028019

    epsgValue = 4326

    xres = -114.215175 - -114.323106 
    yres = 39.028019 - 38.982247 
    xavg = xres/96.0
    yavg = yres/49.0

    outputFormat = 'netcdf'
    
    for j in range(49): 
        for k in range(96):
            value = float(fileHandle.next().strip())
            parameterNames[index][j,k] = value
    gdalDriver.writeRaster(nameOfOuputFile, parameterNames[index], numberOfRows, numberOfColumns, xavg, yavg, xMin, yMax, epsgValue, driver = outputFormat)

def parameterValuesToAnArray():
    
    """
    Function: parameterValuesToAnArray
    Description: parameterValuesToAnArray function stores the parameterValues to an array with parameter name as the array name
    """
    
    index = 0
    monthIndex = 0
    parameterNames = []
    monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    numberOfRows = 96
    numberOfColumns = 49
   
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
                nameOfOuputFile = nameOfParameter+".nc"
                passArraytoGdal(nameOfOuputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows)
                
            elif numberOfValues == 56448:
                for i in range(12):
                    parameterNames.append(nameOfParameter)
                    parameterNames[index] = numpy.arange(4704).reshape(numberOfColumns, numberOfRows)
                    nameOfOuputFile = nameOfParameter+"_"+monthNames[monthIndex]+".nc"
                    passArraytoGdal(nameOfOuputFile, fileHandle, parameterNames, index, numberOfColumns, numberOfRows)
                    monthIndex = monthIndex + 1
                monthIndex = 0
            index = index + 1        
           
if __name__ == "__main__":
    
    nameOfFile = sys.argv[1]
    fileHandle = open(nameOfFile, 'r')
    copyParameterSectionFromInputFile(fileHandle)
    parameterValuesToAnArray()
