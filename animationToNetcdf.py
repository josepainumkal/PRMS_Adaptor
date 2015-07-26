import netCDF4      
import sys

def find_location_values(fileHandle, numberOfHruCells, position):

    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfDays (int): is the total number of values for the variable
	position (int): is the column position from where the values can be 
        retrieved
    
    """

    values = []
   
    for i in range(numberOfHruCells):
	valuesInLine = fileHandle.next().strip().split()
        values.append(valuesInLine[position])
    
    return values

def find_column_values(fileHandle, totalNumberOfDataValues, numberOfMetadataLines, position):
    
    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfDays (int): is the total number of values for the variable
	position (int): is the column position from where the values can be 
        retrieved
    
    """

    values = []

    for i in range(numberOfMetadataLines):
	fileHandle.next()
    
    for j in range(2):
	fileHandle.next()
    
    for k in range(totalNumberOfDataValues):
	valuesInLine = fileHandle.next().strip().split()[2:]
        values.append(valuesInLine[position])
    
    return values

if __name__ == "__main__":
   
    numberOfMetadataLines = 0
    timeValues = []
    numberOfHRUValues = [] 
    
    numberOfArgs = len(sys.argv)

    for i in range(numberOfArgs):

        if sys.argv[i] == "-data":
	    animationFile = sys.argv[i+1]

	elif sys.argv[i] == "-loc":
	    locationFile = sys.argv[i+1]

        elif sys.argv[i] ==  "-nhru":
	    numberOfHruCells = int(sys.argv[i+1])

        elif sys.argv[i] ==  "-nrows":
	    numberOfRows = int(sys.argv[i+1])

	elif sys.argv[i] ==  "-ncols":
	    numberOfColumns = int(sys.argv[i+1])

    fileHandle = open(animationFile, 'r')
    totalNumberOfLines = sum(1 for _ in fileHandle)

    fileHandle = open(animationFile, 'r')
    for line in fileHandle:
	if '#' in line:
            numberOfMetadataLines = numberOfMetadataLines + 1
    
    totalNumberOfDataValues = totalNumberOfLines-(numberOfMetadataLines+2)
    numberOfTimestamps = totalNumberOfDataValues/(numberOfRows*numberOfColumns)
    
    fileHandle = open(animationFile, 'r')
    for i in range(numberOfMetadataLines):
	fileHandle.next()
    outputVariableNames = fileHandle.next().strip().split()[2:]
    fileHandle.next()
    firstDate = fileHandle.next().strip().split()[0]

    # Initialize new dataset
    ncfile = netCDF4.Dataset('animation.nc', mode='w')

    # Initialize dimensions
    time_dim = ncfile.createDimension('time', numberOfTimestamps)  
    nrows_dim = ncfile.createDimension('nrows', numberOfRows)
    ncols_dim = ncfile.createDimension('ncols', numberOfColumns)

    time = ncfile.createVariable('time', 'i4', ('time',))
    time.long_name = 'time'  
    time.units = 'days since '+firstDate
    for index in range(numberOfTimestamps):
	timeValues.append(index+1)	
    time[:] = timeValues

    lat = ncfile.createVariable('lat', 'f8', ('ncols', 'nrows'))
    lat.long_name = 'latitude'  
    lat.units = 'degrees_north'
    position = 1
    fileHandle = open(locationFile, 'r')
    columnValues = find_location_values(fileHandle, numberOfHruCells, position)		
    lat[:] = columnValues

    lon = ncfile.createVariable('lon', 'f8', ('ncols', 'nrows'))
    lon.long_name = 'longitude'  
    lon.units = 'degrees_east'
    position = 2
    fileHandle = open(locationFile, 'r')
    columnValues = find_location_values(fileHandle, numberOfHruCells, position)		
    lon[:] = columnValues

    for index in range(len(outputVariableNames)):
	var = ncfile.createVariable(outputVariableNames[index], 'f8', ('time', 'ncols', 'nrows')) 
        fileHandle = open(animationFile, 'r')
        columnValues = find_column_values(fileHandle, totalNumberOfDataValues, numberOfMetadataLines, index)		
	var[:] = columnValues

    # Close the 'ncfile' object
    ncfile.close()


