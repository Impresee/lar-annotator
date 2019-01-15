# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 10:33:19 2018

@author: Impresee
"""
from utils.Utilidades import ShowImTest, CrearCarpeta
from utils.Num2Text import Monto2Text
from skimage import io
import os
import cv2
from skimage.transform import resize

from utils.testing import GetMetadataValue

def read_check_im(image_path):
    check_image = io.imread(image_path,as_gray=True)
    check_image = resize(check_image, (580, 1200))
    
    return check_image

def get_word_list(im_filename):   
    predicted_CAR = GetMetadataValue(im_filename)
    LAR_expected = Monto2Text(int(predicted_CAR))

    banned_words = ['ruido','y','portador','pesos','']

    LAR_expected_split = LAR_expected.split(' ')
    LAR_expected_list = []
    for word in LAR_expected_split:
        if word in banned_words:
            pass
        else:
            LAR_expected_list.append(word)
    
    return LAR_expected_list

def userROIclass(path_dataset,path_output):    
    #path_dataset = 'C:\\Users\\Impresee\\Desktop\\check_recognition\\Datasets\\ecuador_png'
    #path_output = 'C:\\Users\\Impresee\\Desktop\\LAR_user_input'
    
    CrearCarpeta(path_output,'LAR_output')
    path_output = path_output + '\\LAR_output'
    
        
    #leer imagenes en la carpeta
    file_names =os.listdir(path_dataset)
    
    ThisPath = os.path.realpath(__file__).split('\\userROIclass.py')[0]
    
    
    try:
        file_state_txt = open(ThisPath+'\\'+'LAR_state'+'.txt','r')
        LAR_start = int(file_state_txt.read())
    except FileNotFoundError:
        file_state_txt = open(ThisPath+'\\'+'LAR_state'+'.txt','w')
        LAR_start = 0
    
  
    LAR_end =len(file_names)  
    
    for LAR_i in range(LAR_start,LAR_end):
    
        
        LAR_filename=file_names[LAR_i] #nombre imagen con extension
        check_filename = LAR_filename.split('.')[0] #nombre imagen sin extension
    
        print('imagen n° '+str(LAR_i+1)+' de '+str(LAR_end))
        print('nombre imagen: '+LAR_filename)    
        
        file_state_txt = open(ThisPath+'\\'+'LAR_state'+'.txt','w')
        file_state_txt.write(str(LAR_i))
        file_state_txt.close()
        #leer imagen
        image_path =  path_dataset+'\\'+LAR_filename
        check_image = read_check_im(image_path)
        #check_image = (io.imread( path_dataset+'\\'+LAR_filename, as_gray=True))
        
        #dimensiones de la imagen
        check_H = check_image.shape[0]
        check_W = check_image.shape[1]
        
        #el lar deberia estar en el segundo tercio de la img del cheque
        LAR_X = 0
        LAR_Y = int(0.25*check_H)
        LAR_H = int(0.4*check_H)
        LAR_W = check_W
        LAR_im = check_image[LAR_Y:LAR_Y+LAR_H,LAR_X:LAR_X+LAR_W]
        
    
        txt_data = ''
        carpeta_output = ''
        
        LAR_expected_list = get_word_list(LAR_filename)

        contador_palabras = 0
        for lar_word in LAR_expected_list:
            contador_palabras = contador_palabras +1
            window_text =lar_word +'      palabra = '+str(contador_palabras)+' de '+str(len(LAR_expected_list))+'        cheque = '+str(LAR_i)+' de '+str(LAR_end)
            r= cv2.selectROI(window_text,LAR_im)
            
            if(r[0]+r[1]+r[2]+r[3]==0): #next check
               cv2.destroyAllWindows()
               break
            # Crop image
            Palabra = LAR_im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            cv2.destroyAllWindows()
            
            carpeta_output = lar_word#LARpredict(my_cnn, configuration, Palabra)
            
            # Display cropped image
            ShowImTest(Palabra,1)

            
            if(carpeta_output != 'Borrar'):       
                #crear carpeta para guadar las imagenes de las palabras recortadas
                CrearCarpeta(path_output,carpeta_output)
                #guardar imagen palabra recortada
                io.imsave(path_output +'\\'+carpeta_output+'\\'+LAR_filename.split('-')[0]+'_'+str(LAR_i)+'.png',Palabra)
                
                #guadar bounding box en un txt
                #formato
                # clase:x,y,w,h
                palabra_x = int(LAR_X+r[0])
                palabra_y = int(LAR_Y+r[1])
                palabra_w = int(r[2])
                palabra_h = int(r[3])
                txt_data = txt_data+ carpeta_output+':'+str(palabra_x)+','+str(palabra_y)+','+str(palabra_w)+','+str(palabra_h) + '\n'
                
        #guardar imagen de LAR
        io.imsave(path_output +'\\'+ LAR_filename,LAR_im)
        #crear txt
        file_LAR_txt = open(path_output+'\\'+check_filename+'.txt',"w")
        #escribir data en el txt
        file_LAR_txt.write(txt_data)
        file_LAR_txt.close()
        