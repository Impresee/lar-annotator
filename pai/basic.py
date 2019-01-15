#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pai.basic module
A set of basic functions to operate on gray-scale images
@author: jsaavedr
"""
import numpy as np

#get histogram of an image
def getHistogram(gray_im):
    h=np.zeros(256, dtype=np.float32)
    for i in range(gray_im.shape[0]):
        for j in range(gray_im.shape[1]):
            h[gray_im[i,j]]+=1.0
    return h
#----------------------------------------------
def threshold(gray_im, th):
    bin_im = np.zeros(gray_im.shape, np.uint8)
    bin_im[gray_im>=th]=1
    return bin_im
#----------------------------------------------
#compute accum
def getAccum(histogram, length=256):
    accum=np.zeros(length)
    accum[0]=histogram[0]
    for i in range(1,length):
        accum[i]=accum[i-1]+histogram[i]
    return accum    
#det otsu
def getOtsu(gray_im):    
    h = getHistogram(gray_im)
    h = h / np.sum(h)    
    accum = getAccum(h)
    media_t = np.zeros(256,  np.float32)
    #compute media for each t in [0..255]
    for i in range(0,256):
        media_t[i] = media_t[i-1] + i*h[i] 
    mu = media_t[255]
    best_t = 0
    best_val = 0
    eps = 0.0001
    for t in range(1,256):
        w0 = accum[t]
        w1 = 1.0 - w0        
        mu_0 = media_t[t] / (w0 + eps)
        mu_1 = (mu - media_t[t]) / (w1 + eps)
        val = w0*(mu_0 - mu)*(mu_0 - mu) + w1*(mu_1 - mu)*(mu_1 - mu)
        if val > best_val:
            best_val = val
            best_t = t
    return best_t

#to uint8
def toUINT8(image):
    image[image<0]=0
    image[image>255]=255
    image = image.astype(np.uint8, copy=False)
    return image

#equalization
def imequalize(gray_im):
    h=getHistogram(gray_im)
    accum=getAccum(h/np.float(gray_im.shape[0]*gray_im.shape[1]))
    imeq=np.zeros(gray_im.shape)
    for i in range(imeq.shape[0]):
        for j in range(imeq.shape[1]):
            imeq[i,j]=255*accum[gray_im[i,j]]
    return toUINT8(imeq)



#get vertical profile
def getVerticalProfile(image) :    
    return np.sum(image, 1)

#get vertical profile
def getHorizontalProfile(image) :    
    return np.sum(image, 0)        




