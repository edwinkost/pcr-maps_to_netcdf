#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

import pcraster as pcr
from pcraster.framework import DynamicModel

from outputNetcdf import OutputNetcdf
import virtualOS as vos

class CalcFramework(DynamicModel):

    def __init__(self, cloneMapFileName,\
                       pcraster_files, \
                       output, \
                       modelTime):
        DynamicModel.__init__(self)           # 
        pcr.setclone(cloneMapFileName)
        
        self.modelTime = modelTime
        
        self.pcraster_files = pcraster_files
        
        # move to the input folder
        os.chdir(self.pcraster_files['directory'])
        
        self.output = output
        self.output['file_name'] = vos.getFullPath(self.output['file_name'], self.output['folder'])
        
        # object for reporting
        self.netcdf_report = OutputNetcdf(cloneMapFileName, self.output['description'])       

        print(self.output['long_name'])
        
        # make a netcdf file
        self.netcdf_report.createNetCDF(self.output['file_name'],\
                                        self.output['variable_name'],\
                                        self.output['unit'],\
                                        self.output['long_name'])
        
    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # open input data 
        if self.output['variable_name'] != "temperature":
            pcr_map_values = self.readmap(self.pcraster_files['file_name'])
        else:
            pcr_map_values = 0.50*(self.readmap("tn") + self.readmap("tx"))

        # reporting
        timeStamp = datetime.datetime(self.modelTime.year,\
                                      self.modelTime.month,\
                                      self.modelTime.day,0)
        self.netcdf_report.data2NetCDF(self.output['file_name'],\
                                       self.output['variable_name'],\
                                       pcr.pcr2numpy(pcr_map_values,vos.MV),\
                                       timeStamp)
