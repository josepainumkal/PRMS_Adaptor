import os
from pyee import EventEmitter

ee = EventEmitter()

'''
@ee.on('progress')
def progress(**kwargs):
    print kwargs
'''

from prms.text_to_netcdf import dataToNetcdf
dataToNetcdf.data_to_netcdf(os.getcwd()+'/prms/input_files/LC.data', os.getcwd()+'/prms/outputs/data.nc', event_emitter=ee)

from prms.text_to_netcdf import parameterToNetcdf
parameterToNetcdf.parameter_to_netcdf(os.getcwd()+'/prms/input_files/LC.param', os.getcwd()+'/prms/XY.DAT', 4704, 49, 96, os.getcwd()+'/prms/outputs/parameter.nc', event_emitter=ee)

from prms.text_to_netcdf import controlToNetcdf
controlToNetcdf.control_to_netcdf(os.getcwd()+'/prms/input_files/LC.control', os.getcwd()+'/prms/outputs/control.nc')

from prms.text_to_netcdf import animationToNetcdf
animationToNetcdf.animation_to_netcdf(os.getcwd()+'/prms/output_files/animation.out.nhru', os.getcwd()+'/prms/outputs/parameter.nc', os.getcwd()+'/prms/outputs/animation.nc', event_emitter=ee)

# from prms.text_to_netcdf import animationToNetcdf
# animationToNetcdf.animation_to_netcdf(os.getcwd()+'/prms/output_files/animation.out.nhru', os.getcwd()+'/prms/XY.DAT', 4704, 49, 96, os.getcwd()+'/prms/outputs/animation.nc')

from prms.text_to_netcdf import prmsoutToNetcdf
prmsoutToNetcdf.prmsout_to_netcdf(os.getcwd()+'/prms/output_files/prms.out', os.getcwd()+'/prms/outputs/prmsout.nc', event_emitter=ee)

from prms.text_to_netcdf import statvarToNetcdf
statvarToNetcdf.statvar_to_netcdf(os.getcwd()+'/prms/output_files/statvar.dat', os.getcwd()+'/prms/outputs/statvar.nc', event_emitter=ee)

from prms.netcdf_to_text import netcdfToData
netcdfToData.netcdf_to_data(os.getcwd()+'/prms/outputs/data.nc', os.getcwd()+'/prms/input_files/LC.data', event_emitter=ee)

from prms.netcdf_to_text import netcdfToParameter
netcdfToParameter.netcdf_to_parameter(os.getcwd()+'/prms/outputs/parameter.nc', os.getcwd()+'/prms/input_files/LC.param', event_emitter=ee)

