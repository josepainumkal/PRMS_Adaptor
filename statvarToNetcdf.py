import netCDF4      
import sys

def find_output_variables(fileHandle, numberOfVariables):
    
    """
 
    Returns the names and array indices of the output variables in the file. 
    Two lists, outputVariableNames and outputVariableArrayIndices are created
    to append the names and indices respectively. 

    Args:
        numberOfVariables (int): is the total number of output variables. This
	value is indicated on the first line of the file.
    
    """
   
    outputVariableNames = []
    outputVariableArrayIndices = []  
    
    for index in range(numberOfVariables):    
	words = fileHandle.next().strip().split()
	outputVariableNames.append(words[0])
	outputVariableArrayIndices.append(words[1])	       

    return outputVariableNames, outputVariableArrayIndices

def find_column_values(numberOfVariables, numberOfDataValues, position):

    """
    
    Returns the values of variables in the file. 

    Args:
        numberOfVariables (int): is the total number of output variables. This
	value is indicated on the first line of the file.
	numberOfDataValues (int): is the number of values for each variable. This
        value is equal to the time-step value on the last line of the file.
	position (int): is the column position from where the values can be 
        retrieved.
    
    """

    values = []
    
    fileHandle = open(sys.argv[1], 'r')
    
    for i in range(numberOfVariables+1):
        fileHandle.next()
    
    for j in range(numberOfDataValues):
	valuesInLine = fileHandle.next().strip().split()[7:]
        values.append(valuesInLine[position])
   
    return values

if __name__ == "__main__":
   
    indexOfDataLine = []

    fileHandle = open(sys.argv[1], 'r')
    lastLine = fileHandle.readlines()[-1].split()
    lastTimeStepValue = int(lastLine[0])

    for index in range(1, lastTimeStepValue+1):
        indexOfDataLine.append(index)
    
    # Finding the number of variable values
    fileHandle = open(sys.argv[1], 'r')
    numberOfVariables = int(fileHandle.next().strip())
       
    # Finding the names and array indices of output variables
    outputVariables = find_output_variables(fileHandle, numberOfVariables)
    outputVariableNames = outputVariables[0]
    outputVariableArrayIndices = outputVariables[1]
   
    # Finding the first date
    firstDate = fileHandle.next().strip().split()[1:7]
    year = firstDate[0]
    month = firstDate[1]
    day = firstDate[2]
    hour = firstDate[3]
    minute = firstDate[4]
    second = firstDate[5]

    # Initialize new dataset
    ncfile = netCDF4.Dataset('statvar.nc', mode='w')

    # Initialize dimensions
    time = ncfile.createDimension('time', lastTimeStepValue)  

    # Define time variable
    time = ncfile.createVariable('time', 'i4', ('time',))
    time.long_name = 'time'  
    time.units = 'days since '+year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second
    time[:] = indexOfDataLine
    
    # Define other variables  
    for index in range(len(outputVariableNames)):
        var = ncfile.createVariable(outputVariableNames[index]+'_'+outputVariableArrayIndices[index], 'f4', ('time',))
        columnValues = find_column_values(numberOfVariables, lastTimeStepValue, index)
        var[:] = columnValues
    
    # Close the 'ncfile' object
    ncfile.close()


