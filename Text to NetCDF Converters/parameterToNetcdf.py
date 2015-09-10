import netCDF4      
import sys

def find_dimensions(fileHandle):

    """

    Returns the names and lengths of the variables in the file. Two lists, 
    variableNames and variableLengths are created to append the names and 
    lengths respectively. 
    
    """
    
    dimensionNames = []
    dimensionLengths = []  
    
    for line in fileHandle:
        if 'Dimensions' in line:
	    nextLine = fileHandle.next()
	    while 'Parameters' not in nextLine:
                dimensionNames.append(fileHandle.next().strip())
		dimensionLengths.append(int(fileHandle.next().strip()))
		nextLine = fileHandle.next()
    return dimensionNames, dimensionLengths

def copyParameterSectionFromInputFile(fileHandle):
    
    """

    copyParameterSectionFromInputFile function copies the parameter section from the input file to a new file 'values.param'.

    Args:
        fileHandle: The input file
        
    """
    
    temporaryFileHandle = open('values.param', 'w')
    foundParameterSection = False
    lines = fileHandle.readlines()
    for line in lines:
        if foundParameterSection or 'Parameters' in line:
            temporaryFileHandle.write(line)
            foundParameterSection = True

def find_parameters(fileHandle, numberOfHruCells):
    
    spaceRelatedParameterDimensions = []
    spaceAndTimeRelatedParameterDimensions = []
    spaceRelatedParameterNames = []
    spaceRelatedParameterTypes = []
    spaceAndTimeRelatedParameterNames = []
    spaceAndTimeRelatedParameterTypes = []

    for line in fileHandle:
        if '####' in line:
            name = fileHandle.next().strip().split()[0]
	    numberOfDimensions = int(fileHandle.next().strip())
	    if numberOfDimensions == 1:
	        dimension = fileHandle.next().strip()
		numberOfValues = int(fileHandle.next().strip())
                if numberOfValues == numberOfHruCells:
		    spaceRelatedParameterDimensions.append(dimension)	
		    spaceRelatedParameterNames.append(name)	
		    typeOfValues = int(fileHandle.next().strip())
		    spaceRelatedParameterTypes.append(typeOfValues)

	    if numberOfDimensions == 2:
	        dimension = fileHandle.next().strip()
                fileHandle.next()
		numberOfValues = int(fileHandle.next().strip())
                if numberOfValues == numberOfHruCells * 12:
		    spaceAndTimeRelatedParameterDimensions.append(dimension)	
		    spaceAndTimeRelatedParameterNames.append(name)	
		    typeOfValues = int(fileHandle.next().strip())
		    spaceAndTimeRelatedParameterTypes.append(typeOfValues)
	
    return spaceRelatedParameterNames, spaceRelatedParameterTypes, \
	   spaceAndTimeRelatedParameterNames, spaceAndTimeRelatedParameterTypes, \
	   spaceRelatedParameterDimensions, spaceAndTimeRelatedParameterDimensions

def find_space_dependent_parameter_values(fileHandle, spaceRelatedParameterName, numberOfHruCells):
    
    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfDays (int): is the total number of values for the variable
	position (int): is the column position from where the values can be 
        retrieved
    
    """
    values = []

    for line in fileHandle:
	if spaceRelatedParameterName in line:
            for i in range(4):
		fileHandle.next()
	    for j in range(numberOfHruCells):
		values.append(fileHandle.next().strip())
    return values

def find_space_and_time_dependent_parameter_values(fileHandle, spaceAndTimeRelatedParameterName, numberOfHruCells, position):
    
    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfDays (int): is the total number of values for the variable
	position (int): is the column position from where the values can be 
        retrieved
    
    """
    values = []

    for line in fileHandle:
	if spaceAndTimeRelatedParameterName in line:
            for i in range(5):
		fileHandle.next()
	    for j in range(numberOfHruCells * position):
		fileHandle.next()
	    for k in range(numberOfHruCells):
		values.append(fileHandle.next().strip())
    return values

def find_average_resolution(fileHandle, numberOfHruCells, numberOfRows, numberOfColumns):

    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfDays (int): is the total number of values for the variable
	position (int): is the column position from where the values can be 
        retrieved
    
    """

    latitudeValues = []
    longitudeValues = []
   
    for i in range(numberOfHruCells):
	valuesInLine = fileHandle.next().strip().split()
        longitudeValues.append(float(valuesInLine[1]))
	latitudeValues.append(float(valuesInLine[2]))

    minimumLatitudeValue = min(latitudeValues)
    maximumLatitudeValue = max(latitudeValues)

    minimumLongitudeValue = min(longitudeValues)
    maximumLongitudeValue = max(longitudeValues)

    averageOfLatitudeValues = (maximumLatitudeValue-minimumLatitudeValue)/numberOfRows
    averageOfLongitudeValues = (maximumLongitudeValue-minimumLongitudeValue)/numberOfColumns
 
    latitudeOfFirstHru = latitudeValues[0]
    longitudeOfFirstHru = longitudeValues[0]

    return averageOfLatitudeValues, averageOfLongitudeValues, latitudeOfFirstHru, longitudeOfFirstHru

def add_metadata(parameterName):

    fileHandle = open('parameterDetails.txt', 'r')
    for line in fileHandle:
        if parameterName in line:
	    parameterNameFromFile = line.strip()		
	    lengthOfParameterName = len(parameterNameFromFile)
	    positionOfNameStart = parameterNameFromFile.index(':') + 2
 	    parameterName = parameterNameFromFile[positionOfNameStart:lengthOfParameterName]
		
	    parameterDescriptionFromFile = fileHandle.next().strip()
	    lengthOfParameterDescription = len(parameterDescriptionFromFile)
	    positionOfDescriptionStart = parameterDescriptionFromFile.index(':') + 2
	    parameterDescription = parameterDescriptionFromFile[positionOfDescriptionStart:lengthOfParameterDescription]
		
	    parameterUnitFromFile = fileHandle.next().strip()
	    lengthOfParameterUnit = len(parameterUnitFromFile)
	    positionOfUnitStart = parameterUnitFromFile.index(':') + 2
	    parameterUnit = parameterUnitFromFile[positionOfUnitStart:lengthOfParameterUnit]
		
	    break;

    return parameterName, parameterDescription, parameterUnit

def find_variable_type(parameterType):

    if parameterType == 1:
	value = 'i4'
    elif parameterType == 2:
	value = 'f8'

    return value


def parameter_to_netcdf(inputs, outputFileName):

    numberOfArgs = len(inputs)
    for i in range(numberOfArgs):

        if sys.argv[i] == "-data":
	    parameterFile = sys.argv[i+1]

	elif sys.argv[i] == "-loc":
	    locationFile = sys.argv[i+1]

        elif sys.argv[i] ==  "-nhru":
	    numberOfHruCells = int(sys.argv[i+1])

        elif sys.argv[i] ==  "-nrows":
	    numberOfRows = int(sys.argv[i+1])

	elif sys.argv[i] ==  "-ncols":
	    numberOfColumns = int(sys.argv[i+1])

    fileHandle = open(parameterFile, 'r')
    dimensions = find_dimensions(fileHandle)
    dimensionNames = dimensions[0]
    dimensionLengths = dimensions[1]
   
    fileHandle = open(parameterFile, 'r')
    copyParameterSectionFromInputFile(fileHandle)

    fileHandle = open('values.param', 'r')
    parameters = find_parameters(fileHandle, numberOfHruCells)
    spaceRelatedParameterNames = parameters[0]
    spaceRelatedParameterTypes = parameters[1]
    spaceAndTimeRelatedParameterNames = parameters[2]
    spaceAndTimeRelatedParameterTypes = parameters[3]
    spaceRelatedParameterDimensions = parameters[4]
    spaceAndTimeRelatedParameterDimensions = parameters[5]
        
    if spaceAndTimeRelatedParameterNames:
	monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
       
    fileHandle = open(locationFile, 'r')
    values = find_average_resolution(fileHandle, numberOfHruCells, numberOfRows, numberOfColumns)
    averageOfLatitudeValues = values[0]
    averageOfLongitudeValues = values[1]
    latitudeOfFirstHru = values[2]
    longitudeOfFirstHru = values[3]

    # Initialize new dataset
    ncfile = netCDF4.Dataset(outputFileName, mode='w')

    # Initialize dimensions
    lat_dim = ncfile.createDimension('lat', numberOfRows)
    lon_dim = ncfile.createDimension('lon', numberOfColumns)

    for index in range(len(dimensionNames)):
	dimensionNames[index] = ncfile.createDimension(dimensionNames[index], dimensionLengths[index])

    latList = []
    latList.append(latitudeOfFirstHru)
    previousValue = latitudeOfFirstHru
    lat = ncfile.createVariable('lat', 'f8', ('lat',))
    lat.long_name = 'latitude'  
    lat.units = 'degrees_north'
    for i in range(numberOfRows - 1):
	newValue = previousValue - averageOfLatitudeValues
	latList.append(newValue)
	previousValue = newValue
    lat[:] = latList

    lonList = []
    lonList.append(longitudeOfFirstHru)
    previousValue = longitudeOfFirstHru
    lon = ncfile.createVariable('lon', 'f8', ('lon',))
    lon.long_name = 'longitude'  
    lon.units = 'degrees_east'
    for i in range(numberOfColumns - 1):
	newValue = previousValue + averageOfLongitudeValues
	lonList.append(newValue)
	previousValue = newValue
    lon[:] = lonList
   
    for index in range(len(spaceRelatedParameterNames)):
        value = find_variable_type(spaceRelatedParameterTypes[index])
	metadata = add_metadata(spaceRelatedParameterNames[index])
        parameterName = metadata[0]
	parameterDescription = metadata[1]
	parameterUnit = metadata[2]

        var = ncfile.createVariable(spaceRelatedParameterNames[index], value, ('lat', 'lon')) 
	var.layer_name = parameterName
	var.dimension = spaceRelatedParameterDimensions[index]
	var.layer_desc = parameterDescription
	var.layer_units = parameterUnit

        fileHandle = open('values.param', 'r')
        values = find_space_dependent_parameter_values(fileHandle, spaceRelatedParameterNames[index], numberOfHruCells)		
	var[:] = values

    for index in range(len(spaceAndTimeRelatedParameterNames)):
	value = find_variable_type(spaceAndTimeRelatedParameterTypes[index])
        metadata = add_metadata(spaceAndTimeRelatedParameterNames[index])
        parameterName = metadata[0]
	parameterDescription = metadata[1]
	parameterUnit = metadata[2]

	for monthIndex in range(len(monthNames)):
	    var = ncfile.createVariable(spaceAndTimeRelatedParameterNames[index]+'_'+monthNames[monthIndex], value, ('lat', 'lon'))
	    var.layer_name = parameterName+'_'+monthNames[monthIndex]
	    var.dimension = spaceAndTimeRelatedParameterDimensions[index]+', '+'nmonths'
	    var.layer_desc = parameterDescription
            var.layer_units = parameterUnit

	    fileHandle = open('values.param', 'r')
            values = find_space_and_time_dependent_parameter_values(fileHandle, spaceAndTimeRelatedParameterNames[index], numberOfHruCells, monthIndex)		
	    var[:] = values
    
    # Global attributes
    ncfile.title = open(parameterFile, 'r').readline().strip()
    ncfile.bands = 1
    ncfile.bands_name = 'bands'
    ncfile.bands_desc = 'Parameter information for ' + parameterFile

    # Close the 'ncfile' object
    ncfile.close()

if __name__ == "__main__":
       
    parameter_to_netcdf(sys.argv, 'parameter.nc')

    

