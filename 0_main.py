#!/usr/bin/python
# -*- coding: utf-8 -*-

# EHS (24 September 2014): This is the main script for converting 
#                          a set of pcraster time series maps  
#                          into a single netcdf time series file. 
#
# EHS (27 November 2014): I use this script for converting EFAS-Meteo pcraster files to netcdf format

import os
import sys

# pcraster dynamic framework is used.
from pcraster.framework import DynamicFramework

# The calculation script (engine) is imported from the following module.
from dynamic_calc_framework import CalcFramework

# time object
from currTimeStep import ModelTime

# utility module:
import virtualOS as vos

# variable dictionaries:
import efas_variable_list as varDict

# obtain efas_variable_code from the system argurment
efas_variable_name = sys.argv[1]

# file name of the clone map defining the scope of output
cloneMapFileName = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/clone_maps/RhineMeuse03min.clone.map"

# directory where the original pcraster files are stored
pcraster_files = {}
pcraster_files['directory'] = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/source/pcraster/03min/"
pcraster_files['file_name'] = efas_variable_name # "pr"

# output folder
output = {}
output['folder']        = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/netcdf/"
output['variable_name'] = varDict.netcdf_short_name[efas_variable_name] 
output['file_name']     = output['variable_name']+"_efas_rhine-meuse"+".nc"
output['unit']          = varDict.netcdf_unit[efas_variable_name]
output['long_name']     = varDict.netcdf_long_name[efas_variable_name] 
output['description']   = varDict.description[efas_variable_name]      

# prepare output directory
try:
    os.makedirs(output['folder'])
except:
    pass

startDate     = "1990-01-01" # YYYY-MM-DD
endDate       = None
nrOfTimeSteps = 9070         # based on the last file provided by Ad 

# projection/coordinate sy
inputEPSG  = "EPSG:3035" 
outputEPSG = "EPSG:4326"

def main():
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate,nrOfTimeSteps)
    
    calculationModel = CalcFramework(cloneMapFileName,\
                                     pcraster_files, \
                                     output, tmpDir, inputEPSG, outputEPSG, \
                                     modelTime)
    dynamic_framework = DynamicFramework(calculationModel,modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
