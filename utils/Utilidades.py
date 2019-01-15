# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:07:40 2018

@author: Impresee
"""

import time
from skimage import io, color
from skimage.transform import resize
import matplotlib.pyplot as plt
import os,sys

""" Utilidades para manejar carpetas """        
def CrearCarpeta(Path,FolderName):    
    path_a_crear = os.path.join(Path,FolderName)
    
    try: 
        os.makedirs( path_a_crear)
    except OSError:
        print('')
        #print("el path "+path_a_crear+" ya existe")  
def getThisPath(ThisScriptName):
    ThisPath = os.path.realpath(__file__).split(os.path.join(' ',ThisScriptName).split(' ')[1])[0] 
    return ThisPath

""" Enabble/Disable print """
# Disable
def blockPrint():
   sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
   sys.stdout = sys.__stdout__

""" Funciones para visualizar datos con enable """        
#Imshow con enable
def ShowImTest(Im, mostrar_EN):
    if(mostrar_EN==1):
      plt.figure()
      io.imshow(Im)
      io.show()

#Plot discreto con enable
def StemPlotTest(signal2plot, mostrar_EN):
    if(mostrar_EN==1):
       plt.figure()
       baseline = plt.stem(signal2plot, '-.')
       plt.setp(baseline, color='b', linewidth=2)
       plt.show()  

#Plot continuo con enable
def PlotTest(signal2plot, ylabel, mostrar_EN):
    if(mostrar_EN==1):
       plt.figure()
       plt.plot(signal2plot)
       plt.ylabel(ylabel)
       plt.show()
       
#Plot continuo con enable
def plot_snake(snake_x,snake_y,img, ylabel, mostrar_EN):
    if(mostrar_EN==1):
       plt.figure()
       plt.imshow(img, cmap=plt.cm.gray)
       plt.plot(snake_x, snake_y)
       plt.ylabel(ylabel)
       plt.axis([0, img.shape[1], img.shape[0], 0])
       plt.show()


#Print con enable 
def PrintTest(mensaje,mostrar_EN):
    if(mostrar_EN==1):
        print(mensaje)

#equivalent to max(0,value)
def ReLU(x):
    return x * (x > 0)

def EstandarizarImCheque(image):
    dimH=816
    dimW=1880
    image = color.rgb2gray(image) #rgb to grayscale
    image = resize(image, (dimH,dimW) ) #standar size
    return image

""" Funciones Matlab """        
#funciones tic y toc para medir el tiempo
    #referencia: https://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
def tic():
    #python version of matlab tic and toc functions
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    if 'startTime_for_tictoc' in globals():
        Elapsed_time = time.time() - startTime_for_tictoc
        print ("Elapsed time is " + str(Elapsed_time) + " seconds.")
    else:
        print ("Toc: start time not set")
        Elapsed_time = 0

    return Elapsed_time
