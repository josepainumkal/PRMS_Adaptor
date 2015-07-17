import unittest
import dataToNetcdf as d

class TestPrmsDataNetCDF(unittest.TestCase):
 
    def setUp(self):
        self.input_file = 'test.data'
 
    def test_find_number_of_days(self):
	fileHandle = open(self.input_file, 'r')
        assert (d.find_number_of_days(fileHandle) == 7)

    def test_find_first_date(self):
	fileHandle = open(self.input_file, 'r')
	assert (d.find_first_date(fileHandle) == ['1950', '1', '1', '0', '0', '0'])

    def test_find_variables(self):
	fileHandle = open(self.input_file, 'r')
        assert (d.find_variables(fileHandle) == (['runoff', 'precip', 'tmax', 'tmin'], 
        [1, 1, 1, 1]))

    def test_find_units(self):
	fileHandle = open(self.input_file, 'r')
	assert (d.find_units(fileHandle) == (['runoff', 'precip', 'temperature', 'elevation'], 
        ['ft3 per sec', 'in', 'deg F', 'meters']))

    def test_find_metadata(self):
	fileHandle = open(self.input_file, 'r')
	assert (d.find_metadata(fileHandle, 4) == (['ID', 'Type', 'Latitude', 'Longitude', 'Elevation'], 
        [['10243260', 'runoff', '39.0116', '-114.2144', '2042.16'], ['263340', 'precip', '39.0056', 
        '-114.2206', '2087.88'], ['263340', 'tmax', '39.0056', '-114.2206', '2087.88'], ['263340', 
        'tmin', '39.0056', '-114.2206', '2087.88']]))

    def test_find_column_values(self):
	fileHandle = open(self.input_file, 'r')
	assert (d.find_column_values(fileHandle, 7, 0) == ['1.6', '1.6', '1.6', '1.6', '1.6', '1.6', '1.6'])
 
if __name__ == '__main__':
    unittest.main()
