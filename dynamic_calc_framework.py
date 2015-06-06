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
                       modelTime, \
                       output, inputEPSG = None, outputEPSG = None):
        DynamicModel.__init__(self)           # 
        pcr.setclone(cloneMapFileName)
        
        # time variable/object
        self.modelTime = modelTime
        
        # output file name, folder name, etc. 
        self.output = output
        self.output['file_name'] = vos.getFullPath(self.output['file_name'], self.output['folder'])
        
        # input and output projection/ccordinate systems 
        self.inputEPSG  =  inputEPSG
        self.outputEPSG = outputEPSG

        # prepare temporary directory
        self.tmpDir = output['folder']+"/tmp/"
        try:
            os.makedirs(self.tmpDir)
            os.system('rm -r '+tmpDir+"/*")
        except:
            pass
        
        # the beginning part of name for pcraster files (e.g. pr000000.001)
        self.pcraster_files = pcraster_files

        # move to the output folder
        os.chdir(self.output['folder'])

        # object for reporting
        self.netcdf_report = OutputNetcdf(cloneMapFileName, self.output['description'])       

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
            if self.modelTime.timeStepPCR 
            
            
            pcr_map_values = vos.readPCRmapClone(v = self.pcraster_files['file_name'],\
                                                 cloneMapFileName = ,\
                                                 tmpDir = self.tmpDir,
                                                 absolutePath = None, isLddMap = False,
                                                 cover = pcr.scalar(0.0), 
                                                 isNomMap = False, 
                                                 inputEPSG = "EPSG:4326", 
                                                 outputEPSG = "EPSG:4326", 
                                                 method= " near")
            
            
            
            
            
            self.readmap()
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
