from dateutil.rrule import rrule, DAILY
from netCDF4 import Dataset
import datetime
import os
import sys

fileHandle = Dataset(sys.argv[1], 'r')
temporaryFileHandle = open('LC.data', 'w')

count = 0
countOfVariables = []
variablesFromFile = [] 
variableUnitsFromFile = []
variables = []
variablesInMetaData = []
variableUnits = []
variableUnitsInMetaData = []
typeInMetaData = []
header = []

for variable in fileHandle.variables:
    variablesFromFile.append(variable)

for variable in fileHandle.variables:
    variableUnitsFromFile.append(fileHandle.variables[variable].units)

for index in range(len(variablesFromFile)):
    
    if '_' in variablesFromFile[index]:
        position = variablesFromFile[index].find('_')
        if variablesFromFile[index][0:position] not in variables:
            variables.append(str(variablesFromFile[index][0:position]))
    	    variableUnits.append(str(variableUnitsFromFile[index]))	

    elif variablesFromFile[index] != 'time':
        variables.append(str(variablesFromFile[index]))
	variableUnits.append(str(variableUnitsFromFile[index]))
 

for variable in variables:
    if variable == 'tmax' or variable == 'tmin':
	if 'temperature' not in  variablesInMetaData:
	    variablesInMetaData.append('temperature')
	    position = variables.index(variable)
    	    variableUnitsInMetaData.append(variableUnits[position])
    else:
	variablesInMetaData.append(variable)
        position = variables.index(variable)
        variableUnitsInMetaData.append(variableUnits[position])


for index in range(len(variables)):
    for variable in variablesFromFile:
	
	if '_' in variable:
	    position = variable.find('_')
	    variable = variable[0:position]
	
	if variables[index] == variable:
	    count = count + 1
    
    if(count > 0):
        countOfVariables.append(count)
    count = 0

for i in range(len(variables)):
    for j in range(countOfVariables[i]):
	typeInMetaData.append(variables[i])


for variable in fileHandle.variables:
    if variable != 'time':
        attributesOfAVariable = fileHandle.variables[variable].ncattrs()
	break

print attributesOfAVariable

header.append('Type')

for i in range(len(attributesOfAVariable)):
    if attributesOfAVariable[i] != 'units':
	header.append(str(attributesOfAVariable[i]))


temporaryFileHandle.write('/////////////////////////////////////////////////////////////////////////////////////////////\n// Station metadata:\n// ')
for value in header:
    temporaryFileHandle.write(value+' ')


for eachType in variablesFromFile:
    if eachType != 'time':
        var = fileHandle.variables[eachType]
        if '_' in eachType:
            position = eachType.find('_')
            temporaryFileHandle.write('\n// '+eachType[0:position]+' ')
	else:
	    temporaryFileHandle.write('\n// '+eachType+' ')
        for r in header:
            if r != 'Type':
                temporaryFileHandle.write(getattr(var, r)+' ')

temporaryFileHandle.write('\n/////////////////////////////////////////////////////////////////////////////////////////////\n// Unit: ')
for index in range(len(variablesInMetaData)):
    if index != len(variablesInMetaData)-1:
        temporaryFileHandle.write(variablesInMetaData[index]+' = '+ variableUnitsInMetaData[index]+", ")
    else:
	temporaryFileHandle.write(variablesInMetaData[index]+' = '+ variableUnitsInMetaData[index]+"\n")
temporaryFileHandle.write('/////////////////////////////////////////////////////////////////////////////////////////////\n')

for index in range(len(variables)):
    temporaryFileHandle.write(variables[index]+' '+str(countOfVariables[index])+'\n')

temporaryFileHandle.write('#######################################################################\n')

for variable in fileHandle.variables:
    if variable == 'time':
        units = str(fileHandle.variables[variable].units)
        startDate = units.rsplit(' ')[2]
        startYear = int(startDate.rsplit('-')[0].strip())
	startMonth = int(startDate.rsplit('-')[1].strip())
	startDay = int(startDate.rsplit('-')[2].strip())
        
	shape = str(fileHandle.variables[variable].shape)
	numberOfValues = int(shape.rsplit(',')[0].strip('('))
	
	endDate = str(datetime.date (startYear, startMonth, startDay) + datetime.timedelta (days = numberOfValues-1))
        endYear = int(endDate.rsplit('-')[0].strip())
	endMonth = int(endDate.rsplit('-')[1].strip())
	endDay = int(endDate.rsplit('-')[2].strip())

	startDate = datetime.date(startYear, startMonth, startDay)
	endDate = datetime.date(endYear, endMonth, endDay)

	for dt in rrule(DAILY, dtstart=startDate, until=endDate):
    	    temporaryFileHandle.write(dt.strftime("%Y %m %d 0 0 0")+" ")
	    for variable in fileHandle.variables:
		if variable != 'time':
		    temporaryFileHandle.write(str(fileHandle.variables[variable][count])+" ")
	    temporaryFileHandle.write("\n")
	    count = count+1

