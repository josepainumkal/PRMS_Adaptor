import gdal
import netCDF4   
import osr   
import sys
import os
import time
from netCDF4 import Dataset

def find_location_values(fileHandle, numberOfHruCells, position):

	values = []

	for i in range(numberOfHruCells):
		valuesInLine = fileHandle.next().strip().split()
		values.append(valuesInLine[position])

	return values

def find_column_values(fileHandle, totalNumberOfDataValues, numberOfMetadataLines, position):

	values = []

	for i in range(numberOfMetadataLines):
		fileHandle.next()
	
	for j in range(2):
		fileHandle.next()
	
	for k in range(totalNumberOfDataValues):
		valuesInLine = fileHandle.next().strip().split()[2:]
		values.append(valuesInLine[position])

	return values

def find_average_resolution(fileHandle, numberOfHruCells, numberOfRows, numberOfColumns):

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

def add_metadata(outputVariableName):

	projectRoot = os.path.dirname(os.path.dirname(__file__))
	fileLocation = os.path.join(projectRoot, 'variableDetails/outputVariables.txt')
	fileHandle = open(fileLocation, 'r')
	for line in fileHandle:
		if outputVariableName in line:
			outputVariableNameFromFile = line.strip()		
			lengthOfOutputVariableName = len(outputVariableNameFromFile)
			positionOfNameStart = outputVariableNameFromFile.index(':') + 2
			outputVariableName = outputVariableNameFromFile[positionOfNameStart:lengthOfOutputVariableName]

			outputVariableDescriptionFromFile = fileHandle.next().strip()
			lengthOfOutputVariableDescription = len(outputVariableDescriptionFromFile)
			positionOfDescriptionStart = outputVariableDescriptionFromFile.index(':') + 2
			outputVariableDescription = outputVariableDescriptionFromFile[positionOfDescriptionStart:lengthOfOutputVariableDescription]

			outputVariableUnitFromFile = fileHandle.next().strip()
			lengthOfOutputVariableUnit = len(outputVariableUnitFromFile)
			positionOfUnitStart = outputVariableUnitFromFile.index(':') + 2
			outputVariableUnit = outputVariableUnitFromFile[positionOfUnitStart:lengthOfOutputVariableUnit]

			break;

	return outputVariableName, outputVariableDescription, outputVariableUnit

def extract_row_column_hru_information(parameterFile):

	fileHandle = Dataset(parameterFile, 'r')
	attributes = fileHandle.ncattrs()    
	for attribute in attributes:
		if attribute == 'number_of_hrus':
			numberOfHruCells = int(repr(str(fileHandle.getncattr(attribute))).replace("'", ""))
		if attribute == 'number_of_rows':
			numberOfRows = int(repr(str(fileHandle.getncattr(attribute))).replace("'", ""))
		if attribute == 'number_of_columns':
			numberOfColumns = int(repr(str(fileHandle.getncattr(attribute))).replace("'", ""))

	return numberOfHruCells, numberOfRows, numberOfColumns

def extract_lat_and_lon_information(parameterFile):

	fileHandle = Dataset(parameterFile, 'r')
	latitude = 'lat'
	latitudeValues = fileHandle.variables[latitude][:]
	longitude = 'lon'
	longitudeValues = fileHandle.variables[longitude][:]

	return latitudeValues, longitudeValues


def animation_to_netcdf(animationFile, parameterFile, outputFileName, event_emitter=None, **kwargs):

	kwargs['event_name'] = 'animation_to_nc'
	kwargs['event_description'] = 'creating netcdf file from output animation file'
	kwargs['progress_value'] = 0.00
	if event_emitter:
		event_emitter.emit('progress',**kwargs)

	values = extract_row_column_hru_information(parameterFile)    
	numberOfHruCells = values[0]
	numberOfRows = values[1]
	numberOfColumns = values[2]

	values = extract_lat_and_lon_information(parameterFile)
	latitudeValues = values[0]
	longitudeValues = values[1]

	numberOfMetadataLines = 0
	timeValues = []
	numberOfHRUValues = [] 

	fileHandle = open(animationFile, 'r')
	totalNumberOfLines = sum(1 for _ in fileHandle)

	fileHandle = open(animationFile, 'r')
	for line in fileHandle:
		if '#' in line:
			numberOfMetadataLines = numberOfMetadataLines + 1

	totalNumberOfDataValues = totalNumberOfLines-(numberOfMetadataLines+2)
	numberOfTimeSteps = totalNumberOfDataValues/(numberOfRows*numberOfColumns)

	fileHandle = open(animationFile, 'r')
	for i in range(numberOfMetadataLines):
		fileHandle.next()
	outputVariableNames = fileHandle.next().strip().split()[2:]
	fileHandle.next()
	firstDate = fileHandle.next().strip().split()[0]     

	# Initialize new dataset
	ncfile = netCDF4.Dataset(outputFileName, mode='w')

	# Initialize dimensions
	time_dim = ncfile.createDimension('time', 1)  
	nrows_dim = ncfile.createDimension('lat', numberOfRows)
	ncols_dim = ncfile.createDimension('lon', numberOfColumns)

	time = ncfile.createVariable('time', 'i4', ('time',))
	time.long_name = 'time'  
	time.units = 'days since '+firstDate
	for index in range(1):
		timeValues.append(index+1)	
	time[:] = timeValues

	lat = ncfile.createVariable('lat', 'f8', ('lat',))
	lat.long_name = 'latitude'  
	lat.units = 'degrees_north'
	lat[:] = latitudeValues

	lon = ncfile.createVariable('lon', 'f8', ('lon',))
	lon.long_name = 'longitude'  
	lon.units = 'degrees_east'
	lon[:] = longitudeValues

	sr = osr.SpatialReference()
	sr.ImportFromEPSG(4326)
	crs = ncfile.createVariable('crs', 'S1',)
	crs.spatial_ref = sr.ExportToWkt()

	kwargs['event_name'] = 'animation_to_nc'
	kwargs['event_description'] = 'creating netcdf file from output animation file'
	kwargs['progress_value'] = 0.05
	if event_emitter:
		event_emitter.emit('progress',**kwargs)

	prg = 0.10
	length = len(outputVariableNames)

	for index in range(length):
		metadata = add_metadata(outputVariableNames[index])
		outputVariableName = metadata[0]
		outputVariableDescription = metadata[1]
		outputVariableUnit = metadata[2]

		var = ncfile.createVariable(outputVariableNames[index], 'f8', ('time', 'lat', 'lon')) 
		var.layer_name = outputVariableName
		var.layer_desc = outputVariableDescription
		var.layer_units = outputVariableUnit
		var.grid_mapping = "crs" 

		fileHandle = open(animationFile, 'r')
		columnValues = find_column_values(fileHandle, totalNumberOfDataValues/numberOfTimeSteps, numberOfMetadataLines, index)		
		var[:] = columnValues

		if int(prg % 2) == 0:	
			progress_value = prg/length * 100
			kwargs['event_name'] = 'animation_to_nc'
			kwargs['event_description'] = 'creating netcdf file from output animation file'
			kwargs['progress_value'] = format(progress_value, '.2f')
			if event_emitter:
				event_emitter.emit('progress',**kwargs)
		prg += 1

	# Global attributes
	ncfile.title = 'PRMS Animation File'
	ncfile.nsteps = 1
	ncfile.bands_name = 'nsteps'
	ncfile.bands_desc = 'Variable information for ' + animationFile

	# Close the 'ncfile' object
	ncfile.close()

	kwargs['event_name'] = 'animation_to_nc'
	kwargs['event_description'] = 'creating netcdf file from output animation file'
	kwargs['progress_value'] = 100
	if event_emitter:
		event_emitter.emit('progress',**kwargs)
    





