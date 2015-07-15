import netCDF4      
import sys

def find_number_of_days(fileHandle):

    count = -1
 
    foundParameterSection = False
    lines = fileHandle.readlines()
    for line in lines:
        if foundParameterSection or "#" in line:
            count += 1
            foundParameterSection = True
    return count
    
def find_first_date(fileHandle):
   
    for line in fileHandle:
        # Finding the number of variables
        if "#" in line:
            firstLine = fileHandle.next().strip().split()[:6]
    return firstLine

def insert_variables_to_list(variableNames, variableLengths, line):

    # Appending variable name and length into lists
    words = line.split()
    variableNames.append(words[0])
    variableLengths.append(int(words[1]))

def find_variables(fileHandle):
    
    variableNames = []
    variableLengths = []  
    
    for line in fileHandle:
        # Finding the variables and their length
        if "///" in line:
            firstLine = fileHandle.next().strip()
            if not "//" in firstLine:
		insert_variables_to_list(variableNames, variableLengths, firstLine)
		nextLine = fileHandle.next().strip()
		while '#' not in nextLine:
		    insert_variables_to_list(variableNames, variableLengths, nextLine)
		    nextLine = fileHandle.next().strip()

    return variableNames, variableLengths

def find_units(fileHandle):

    variableNames = []
    variableUnits = [] 

    for line in fileHandle:

        # Finding the variables and their length
        if '///' in line:
            firstLine = fileHandle.next().strip()
            nextLine = fileHandle.next().strip()
            if '///' in nextLine:
	        l = firstLine.rsplit(':')[1].strip()
	        words = l.rsplit(',')
                for word in words:
		    variableNames.append(word.rsplit('=')[0].strip())
		    variableUnits.append(word.rsplit('=')[1].strip())

    return variableNames, variableUnits

def find_metadata(fileHandle, s):
    
    dValues = []

    for line in fileHandle:
        if '///' in line:
            fileHandle.next().strip()
            header = fileHandle.next().rsplit('//')[1].strip()
	    headerValues = header.split()
            
	    for i in range(s):
                nextLine = fileHandle.next().rsplit('//')[1].strip()    
		dataValues = nextLine.split()[:len(headerValues)]
		dValues.append(dataValues)	       
	    break

    return headerValues, dValues

def find_column_values(fileHandle, numberOfDays, i):

    values = []

    for line in fileHandle:
        if '#' in line:
	    for j in range(numberOfDays):
	        valuesInLine = fileHandle.next().strip().split()[6:]
                values.append(valuesInLine[i])
    
    return values

def find_time_values(fileHandle, numberOfDays):

    values = []

    for line in fileHandle:
        if '#' in line:
	    for j in range(numberOfDays):
	        valuesInLine = fileHandle.next().strip().split()[:6]
                values.append(int(valuesInLine[2]))
    
    return values

def find_tmax_tmin_units(i, variableNames, varNames, variableUnits):

    if variableNames[i] == 'tmax':
        p = varNames.index('temperature')
	var.units = variableUnits[p]
    elif variableNames[i] == 'tmin':
	p = varNames.index('temperature')
	var.units = variableUnits[p]
    else:
	var.units = variableUnits[i]

def add_metadata(var, dataValues, position, headerValues):
  
    var.ID = dataValues[position][headerValues.index('ID')]
    var.latitude = dataValues[position][headerValues.index('Latitude')]
    var.longitude = dataValues[position][headerValues.index('Longitude')]
    var.elevation = dataValues[position][headerValues.index('Elevation')]
	        
if __name__ == "__main__":
   
    fileHandle = open(sys.argv[1], 'r')
    numberOfDays = find_number_of_days(fileHandle)
    print numberOfDays

    no = []
    for i in range(numberOfDays):
	no.append(i)

    fileHandle = open(sys.argv[1], 'r')
    firstDate = find_first_date(fileHandle)
    year = firstDate[0]
    month = firstDate[1]
    day = firstDate[2]
    hour = firstDate[3]
    minute = firstDate[4]
    second = firstDate[5]

    # Finding the variables and their length
    fileHandle = open(sys.argv[1], 'r')
    variables = find_variables(fileHandle)
    variableNames = variables[0]
    variableLengths = variables[1]
    sumValues = []
    s = 0
    for i in range(len(variableLengths)):
	s = s + variableLengths[i]
	sumValues.append(s)
        
    # Finding the variable units
    fileHandle = open(sys.argv[1], 'r')
    units = find_units(fileHandle)
    varNames = units[0]
    variableUnits = units[1]

    # Finding the metadata
    fileHandle = open(sys.argv[1], 'r')
    metadata = find_metadata(fileHandle, s)
    headerValues = metadata[0]
    dataValues = metadata[1]
    #print headerValues


    # Initialize new dataset
    ncfile = netCDF4.Dataset('data.nc', mode='w')

    # Initialize dimensions
    time = ncfile.createDimension('time', numberOfDays)  
    #time = ncfile.createDimension('time', 5)  

    # Define variables
    time = ncfile.createVariable('time', 'i4', ('time',))
    time.long_name = 'time'  
    time.units = 'days since '+year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second
  
    fileHandle = open(sys.argv[1], 'r')
    timeValues = find_time_values(fileHandle, numberOfDays)
    time[:] = no

    for i in range(len(variableNames)):
        if variableLengths[i] > 1:
	    v = sumValues[i] - variableLengths[i]
	    for j in range(variableLengths[i]):
	        
		var = ncfile.createVariable(variableNames[i]+'_'+str(j+1), 'f4', ('time',))
		add_metadata(var, dataValues, v+j, headerValues)
		find_tmax_tmin_units(i, variableNames, varNames, variableUnits)

		fileHandle = open(sys.argv[1], 'r')
    	        columnValues = find_column_values(fileHandle, numberOfDays, v+j)		
		var[:] = columnValues
    	else:
	    var = ncfile.createVariable(variableNames[i], 'f4', ('time',)) 
	    position = sumValues[i] - 1
	    add_metadata(var, dataValues, position, headerValues)
	    find_tmax_tmin_units(i, variableNames, varNames, variableUnits)
	    
	    fileHandle = open(sys.argv[1], 'r')
    	    columnValues = find_column_values(fileHandle, numberOfDays, position)
            var[:] = columnValues
    
    # Close the 'ncfile' object
    ncfile.close()
    
   
    

    
   

