# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 11:09:47 2018

@author: Impresee
"""
from utils.Utilidades import ShowImTest,PlotTest
from skimage import filters
from skimage.morphology import thin, convex_hull_image, disk,binary_closing, binary_erosion,dilation#, binary_dilation, convex_hull_image,skeletonize
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border

""" Global and adaptative thresholding """
def Binarizar_Otsu(Im):
    global_thresh = filters.threshold_otsu(Im)
    Im_BW_global = (Im < global_thresh)
    return Im_BW_global

def th_otsu(Im):
    global_thresh = filters.threshold_otsu(Im)
    Im_BW_global = (Im < global_thresh)
    return Im_BW_global

def Binarizar_Sauvola(Im,win_size):
    if(win_size%2==0): #win_size must be odd
        win_size = win_size+1
    global_thresh = filters.threshold_sauvola(Im,win_size)
    Im_BW = (Im < global_thresh)
    return Im_BW

def th_sauvola(Im,win_size):
    if(win_size%2==0): #win_size must be odd
        win_size = win_size+1
    global_thresh = filters.threshold_sauvola(Im,win_size)
    Im_BW = (Im < global_thresh)
    return Im_BW

def padding(tight_im,padding_size=10,background_color=None):
    if(background_color is None):
        #otsu bin
        im_bw = th_otsu(tight_im)
        #mean value as background color
        background_color =  tight_im[np.logical_not(im_bw)].mean()
        
    padding_start = padding_size
    padding_shape = 2*padding_start
    padding_image = background_color*np.ones((tight_im.shape[0]+padding_shape,tight_im.shape[1]+padding_shape))
    padding_image[padding_start:tight_im.shape[0]+padding_start,padding_start:tight_im.shape[1]+padding_start ] = tight_im
    
    return padding_image

""" Vertical and horizontal sumatories to get image pixels profiles """
def profile_y(Im_BW):     
    return Im_BW.sum(axis=1)

def profile_x(Im_BW):
    return Im_BW.sum(axis=0)

def QuitarLineaRef(Im_BW,grosor_linea):
    suma_y = profile_y(thin(Im_BW))
    linea = np.argmax(suma_y)  
    Im_BW_sin_linea = 1*Im_BW
    Im_BW_sin_linea[linea-grosor_linea:linea+grosor_linea+1,0:Im_BW.shape[1]] = 0*Im_BW[linea-grosor_linea:linea+grosor_linea+1,0:Im_BW.shape[1]]
    return Im_BW_sin_linea

def one2two_dim(signal_1d):
    
    signal_2d = np.vstack((signal_1d,signal_1d))
    signal_2d = np.vstack((signal_1d*0,signal_2d))
    signal_2d = np.vstack((signal_2d,signal_1d*0))
    return signal_2d 

def convex_hull_bbox(Im_BW):
    
    if(Im_BW.shape[0]<2):
        return [0,Im_BW.shape[0],0,Im_BW.shape[1]]
    if(Im_BW.shape[1]<2):
        return [0,Im_BW.shape[0],0,Im_BW.shape[1]]
    else:
        #convex hull
        try: 
            hull = convex_hull_image(Im_BW)
        except ValueError:
            return [0,Im_BW.shape[0],0,Im_BW.shape[1]]
    
        label_hull = label(hull)
    
        for region in regionprops(label_hull):
            if(str(region.bbox)=='None'):
                return [0,Im_BW.shape[0],0,Im_BW.shape[1]]
            return region.bbox
        
        #x1=  region.bbox[0]
        #x2 = region.bbox[2]
        #y1 = region.bbox[1]
        #y2 = region.bbox[3]
    #how use it:
    #Im_clipped= Im_clip_v[x1:x2,y1:y2] 
    #or
    #Im_clipped= Im_clip_v[bb[0]:bb[2],bb[1]:bb[3]]

def getBWTiccWords(Im,EN,predicted_font=1):
    #binarizar
    Im_BW = Binarizar_Sauvola(Im,15)
    ShowImTest(Im_BW, EN)

    #closing
    Im_BW =binary_closing(Im_BW,disk(1))
      
    #quitar linea de referencia
    grosor_linea=3
    Im_BW = QuitarLineaRef(Im_BW,grosor_linea)
    
    #pequeño margen superior e inferior
    borde=5
    Im_BW[0:borde,0:Im_BW.shape[1]] = False    
    Im_BW[Im_BW.shape[0]-borde:Im_BW.shape[0],0:Im_BW.shape[1]] = False
    
 
    
    #dilatacion y closing exagerado para segmentar palabras
    if(predicted_font==1):
        Im_BW_grueso = Im_BW
        Im_BW_grueso =dilation(Im_BW_grueso ,disk(2))
        Im_BW_grueso =binary_erosion(Im_BW_grueso,disk(1))
        Im_BW_grueso =binary_closing(Im_BW_grueso,np.ones((8,1)))
        Im_BW_grueso =binary_closing(Im_BW_grueso,disk(13))
        #Im_BW_grueso =binary_closing(Im_BW_grueso,disk(8))
        ShowImTest(Im_BW_grueso, EN)
        
        Im_BW_grueso =dilation(Im_BW_grueso,disk(2))
        ShowImTest(Im_BW_grueso, EN)
    else:
        Im_BW_grueso = Im_BW
        #Im_BW_grueso =dilation(Im_BW_grueso ,disk(2))
        #Im_BW_grueso =binary_erosion(Im_BW_grueso,disk(1))
        #Im_BW_grueso =binary_closing(Im_BW_grueso,np.ones((8,1)))
        Im_BW_grueso =binary_closing(Im_BW_grueso,np.ones((1,5)))
        Im_BW_grueso =binary_closing(Im_BW_grueso,disk(3))
        #Im_BW_grueso =binary_closing(Im_BW_grueso,disk(8))
        ShowImTest(Im_BW_grueso, EN)
        
        Im_BW_grueso =dilation(Im_BW_grueso,disk(1))
        #ShowImTest(Im_BW_grueso, EN)
    return Im_BW_grueso
        
def getGapsIm(im_bw, EN):
    profile_x_1d = profile_x(im_bw)
    
    profile_x_1d = profile_x(im_bw)
    PlotTest(profile_x_1d, 'perfil x LAR', EN)

    puntos_criticos = (profile_x_1d==0 )
    PlotTest(puntos_criticos, 'perfil x LAR bin', EN)
    
    critic_points_2D = clear_border(one2two_dim(puntos_criticos))
    
    ShowImTest(critic_points_2D,EN)
    
    return critic_points_2D

def getGapsIm_v(im_bw, EN):
    profile_y_1d = profile_y(im_bw)
    
    profile_y_1d = profile_y(im_bw)
    PlotTest(profile_y_1d, 'perfil y', EN)

    puntos_criticos = (profile_y_1d==0 )
    PlotTest(puntos_criticos, 'perfil y bin', EN)
    
    critic_points_2D = clear_border(one2two_dim(puntos_criticos))
    
    ShowImTest(critic_points_2D,EN)
    
    return critic_points_2D

def SepararPalabras(Im,MinSize,QuitarLinea,EN,predicted_font=1):
    SplitPointsList = []
    
    ticc_im_bw= getBWTiccWords(Im,EN,predicted_font)    
    gaps = getGapsIm(ticc_im_bw,EN)
    label_gaps = label(gaps)
    
    #store gaps centroids also the start and end of the LAR image
    SplitPointsList.append(0) #start of LAR
    for gap_region in regionprops(label_gaps):
        SplitPointsList.append(int(gap_region.centroid[1]))
    SplitPointsList.append(Im.shape[1]-1) #end of LAR
    print('split points')
    print(SplitPointsList)
    
    #store the start and end of each word in LAR
    words_list =[]
    for split_i in range(0,len(SplitPointsList)-1):
        if( abs(SplitPointsList[split_i+1]-SplitPointsList[split_i])> MinSize): #the word must be greater than a minSize
            word = [SplitPointsList[split_i],SplitPointsList[split_i+1]]
            words_list.append(word)
    print('wordlist')
    print(words_list)
    return words_list


"""
from skimage import color,io
from skimage.transform import resize

image_path = 'C:\\Users\\Impresee\\Desktop\\check_recognition\\Datasets\\EscaneosMx8900SolicitadosPorJorgeVeliz20181012\\Top10.bmp'
check_image = color.rgb2gray(io.imread(image_path, as_gray=True))
check_image = resize(check_image,(510,1200))
io.imshow(check_image)
io.show()

Im = check_image[210:250, 80:1150]

io.imshow(Im)
io.show()
EN = 1
ticc_im_bw= getBWTiccWords(Im,EN)

getGapsIm(ticc_im_bw,EN)
"""
