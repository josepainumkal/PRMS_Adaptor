import os
import inspect
import numpy as np
import gdal
from driver import *

def getParameters(fo):
    
    """
    Function: getParameters
    Description: The following function copies the parameter section from the input file to a new file
    """
    
    fw = open("parameterValues.param", 'w')
    always_print = False
    lines = fo.readlines()
    for line in lines:
        if always_print or "Parameters" in line:
            fw.write(line)
            always_print = True

def valueType(typeOfValues):

    value_1 = 4704
    value_2 = 4704.0

    if typeOfValues == 1:
        value = value_1
    elif typeOfValues == 2:
        value = value_2
    return value

def getValues():
    
    """
    Function: getValues
    Description: The following function stores parameter values in separate files
    """
 
    index = 0
    nameList = []
    #monthList = []
   
    def steps():
        for j in range(49): 
            for k in range(96):
                value = float(fr.next().strip())
                nameList[index][j,k] = value
               
    fr = open("parameterValues.param", 'r')
    for line in fr:
        if "####" in line:
            parameterName = fr.next().strip()
            nameList.append(parameterName)
            numberOfDimensions = int(fr.next())
            for i in range(numberOfDimensions):
                fr.next()
            numberOfValues = int(fr.next())
            typeOfValues = int(fr.next())
            value = valueType(typeOfValues)
            nameList[index] = np.zeros(value).reshape(49,96)
            
            if numberOfValues == 4704:
                steps()
            writeRaster(parameterName+".tif",nameList[index],96,49,100,100,108,101,4326,driver='gtiff')
               
            #elif numberOfValues == 56448:
                #for i in range(12):
                    #steps()
            index = index + 1
                   
f = raw_input("Please enter the file name: ")
fo = open(f, 'r')
getParameters(fo)
getValues()
