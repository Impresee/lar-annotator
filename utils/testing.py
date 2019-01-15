# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:16:48 2018

@author: Impresee
"""
import pandas
import os
from skimage import io,color

def GetMetadataValue(image_filename,metadata_path=None):
    
    check_filename = (image_filename.split('.')[0])+'.tif'
    
    if(metadata_path is None):
        metadata_path = '.\\METADATA_CMS.xlsx'
        
    #leer metadata del xlsx
    
    df = pandas.read_excel(metadata_path)
    #print the column names
    #print(df.columns)
    #get the column values    
    lista_nombres = df['NOMBRE_ANVERSO'].values
    lista_montos = df['MONTO'].values
    lista_nombres=lista_nombres.tolist()

    check_index = lista_nombres.index(check_filename)
    gt_value = lista_montos[check_index]

    return gt_value

def GetMetadata(metadata_path=None):

    
    if(metadata_path is None):
        metadata_path = '.\\METADATA_CMS.xlsx'
        
    #leer metadata del xlsx
    
    df = pandas.read_excel(metadata_path)
    #print the column names
    #print(df.columns)
    #get the column values    
    lista_nombres = df['NOMBRE_ANVERSO'].values
    lista_montos = df['MONTO'].values
    lista_nombres=lista_nombres.tolist()

    #check_index = lista_nombres.index(check_filename)
    #gt_value = lista_montos[check_index]
    return lista_nombres,lista_montos
    
	
from random import randint

def read_random_im(dataset_path):
	
	#get a random check image form a dataset path
	file_names =os.listdir(dataset_path)
	num_files =len(file_names)
	file_i = randint(0,num_files-1)    
	image_filename=file_names[file_i]
	image_path = os.path.join(dataset_path,image_filename)
	image = io.imread(image_path)
	image = color.rgb2gray(image) #rgb to grayscale
	
	return image_path, image