# PRMS Adaptor

In order for PRMS data to be interoperable with the rest of the Virtual
Watershed (VW) ecosystem, we need to be able to convert to NetCDF format,
the reference data format of the VW. To do this we've developed the PRMS
adaptors as an element of the growing suite of VW adaptors. 
  

Module Documentation
--------------------

PRMS model has three input files - Control File, Data File, and Parameter File. 
The Control File contains all of the control parameters that PRMS uses during the course of the simulation. 
It includes details such as input and output filenames, content of the output files, and simulation starting and ending dates. The Data File contains measured time-series data used in a PRMS simulation. 
The Parameter File contains the values of the parameters that do not change during a simulation. 
It contains a set of parameters with a number of values for each HRU (Hydrologic Response Unit). 
The file includes space dependent, time dependent, and space and time dependent parameters. 
After running the model, it generates three output files - Animation File and Statistic Variables File and Water Budget File.

Following is the command to convert `PRMS` files from `text` format to `NetCDF` format:


```bash

python example.py

```
   
