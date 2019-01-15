# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 11:47:31 2018

@author: Impresee
"""

"""

genera nombre escrito en palabras de un numero
input int entre 1 y 999999999999999
output string del int en palabras hasta cifras del orden de 'miles de billones'

"""

import math

def unidad(digito):
    Texto_unidad = ['','un','dos','tres','cuatro','cinco','seis','siete','ocho','nueve']
    return Texto_unidad[digito]

def decena(digito):
    Texto_decena = ['','diez','veinte','treinta','cuarenta','cincuenta','sesenta','setenta','ochenta','noventa']
    return Texto_decena[digito]

def veinti(unidad):
    Texto_veinti = ['','veintiun','veintidos','veintitres','veinticuatro','veinticinco','veintiseis','veintisiete','veintiocho','veintinueve']
    
    return Texto_veinti[unidad] 
def dieci(unidad):
    Texto_dieci = ['','once','doce','trece','catorce','quince','dieciseis','diecisiete','dieciocho','diecinueve']
    return Texto_dieci[unidad] 

def centena(digito):
    Texto_centena = ['','ciento','doscientos','trecientos','cuatrocientos','quinientos','seiscientos','setecientos','ochocientos','novecientos']
    return Texto_centena[digito] 
        
def mil(triplete):
    if(int(triplete)==0):
        return ''
    else:
        return 'mil'
    
def millon(digito):
    if(digito=='1'):
        return 'millon'
    else:
        return 'millones'
def billon(digito):
    if(digito==1):
        return 'un billon'
    else:
        return 'billones'
    
def Monto2Text(monto):
    #numero aletorio como entrada
    #monto = randint(0, 999999999999999)
    #monto = randint(0, 999999999)
    ##print(monto)
    monto_string = str(monto)
    #---------descomponer en tripletes--------
    num_dig = len(monto_string)
    #print(num_dig)
    
    #cuantos tripletes tiene?
    tripletes = math.ceil(num_dig/3) #division normal
    resto = num_dig%3 #resto
    
    if(resto==1):
        monto_string = '00' + monto_string
    if(resto==2):
        monto_string = '0' + monto_string
    TextList = []
    #print(monto_string)
    
    #dividir el numero en tripletes
    for triplete_i in range(1,tripletes+1):
        triplete = monto_string[0+(triplete_i-1)*3:(triplete_i-1)*3+3] 
        #print(triplete)
    #dado un triplete tenemos
        #triplete[2] unidad
        #triplete[1] decena
        #triplete[0] centena
        
        #partimos nombrando de la centena
        TextList.append(centena(int(triplete[0])))
        #seguimos con las decenas
        if((30> int(triplete[1]+triplete[2]) >20) | (20> int(triplete[1]+triplete[2]) >10)):
            if(20> int(triplete[1]+triplete[2]) >10): #para 11 12 13..19
                TextList.append(dieci(int(triplete[2])))
            else:
                if(30> int(triplete[1]+triplete[2]) >20): #para 21 22 23...29
                    TextList.append(veinti(int(triplete[2])))
        else: #si no es nada de lo anterior se sigue nombrando normalmente
            TextList.append(decena(int(triplete[1])))
            if(triplete[2]!='0'): 
                if(triplete[1]!='0'): #si la decena es distinta de 0
                    TextList.append('y')
                if((triplete[2]=='1') & ((tripletes-triplete_i)==0)):
                    TextList.append(unidad(int(triplete[2]))+'o' )#cambia 'un' por 'uno' si es el ultimo digito
                else:
                    TextList.append(unidad(int(triplete[2])))
            
        #dependiendo del numero de triplete
        if((tripletes-triplete_i)==1): #miles
            TextList.append(mil(triplete)) #se usa la unidad del triplete
        if((tripletes-triplete_i)==2): #millones
            TextList.append(millon(triplete[2])) #se usa la unidad del triplete
        #dependiendo del numero de triplete
        if((tripletes-triplete_i)==3): #mil millones
            TextList.append(mil(1))
        if((tripletes-triplete_i)==4): #billones
            TextList.append(billon(triplete[2])) #se usa la unidad del triplete
        if((tripletes-triplete_i)==5): #mil billones
            TextList.append(mil(1))
        
   
    TextListFiltered = [x for x in TextList if x]
    #print(TextListFiltered)       
    #List2String
    Result=''
    for x in TextListFiltered:
            Result = Result + ' ' + x
    #print(Result)
    
    return Result     
        
        
        
        