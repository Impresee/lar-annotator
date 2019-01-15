#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:45:54 2018

@author: jsaavedr
"""
import sys

cnn_lib_location = 'C:\\Users\\Impresee\\Desktop\\CAR_LARrecognition\\TF_LAR\\ConvolutionalNetwork'
#cnn_lib_location = '/home/recognition/sources/git/ConvolutionalNetwork'
  
configuration_file = cnn_lib_location +'\\configuration.config'
#configuration_file = cnn_lib_location +'/configuration.config'


sys.path.append(cnn_lib_location)
