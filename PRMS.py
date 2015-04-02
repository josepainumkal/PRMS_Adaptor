import sys

def PRMSConverter():
	numberOfArgs = len(sys.argv)
	PRMSDataDirectory = "."
	PRMSXYDAT = "./XY.dat"
	OutputDirectory = "."
	for i in range(numberOfArgs):
		if sys.argv[i] == "-r":
			row = sys.argv[i+1]
			print "Number of rows: " + row
		elif sys.argv[i] ==  "-c":
			col = sys.argv[i+1]
			print "Number of cols: " + col
		# This sets the PRMS data directory where PRMS files are located.
		elif sys.argv[i] == "-data":
			PRMSDataDirectory = sys.argv[i+1]
			print "Setting PRMS Data Directory to: " + sys.argv[i+1]
		# This sets where the XY.dat that contains information about the HRU cells lat long coordinates.
		elif sys.argv[i] == "-hru_cells":
			PRMSXYDAT = sys.argv[i+1]
			print "Setting PRMS XY.DAT file to: " + sys.argv[i+1]
		elif sys.argv[i] == "-output":
			OutputDirectory = sys.argv[i+1]
			print "Setting output directory to: " + sys.argv[i+1]
	# Call PRMS to tiff or PRMS to netcdf converter
	print "Converting PRMS files"
	
	# 
	print "Success files are in: " +  OutputDirectory
	
PRMSConverter()