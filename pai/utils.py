#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 13:20:00 2018

@author: jsaavedr
"""
from . import basic  
from . import bw
import skimage.measure as measure
import skimage.morphology as morph
import cv2
import numpy as np

#%%
def extractLAR(check_image):
    """
    check_image must come in grayscale format
    """
    image = cv2.resize(check_image, (1200, 510))
    #this values are estimating fromr real checks
    lar_image = image[210:300, 80:1150]
    #reduce noise by median filter
    lar_image = cv2.medianBlur(lar_image,3)
    bw_image= cv2.adaptiveThreshold(lar_image,1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,31,15)
        
    bw_image[0:20, :] = 0
    #estimating the beste row representing the center of the lar text
    #Computing profile using the 10% of the lar width    
    sub_width = int(0.10 * lar_image.shape[1])
    sub_image = bw_image[:, 0:sub_width]
    v_profile = basic.getVerticalProfile(sub_image)
    bin_v_profile = basic.threshold(v_profile, sub_width*0.4)
    bin_v_profile = np.reshape(bin_v_profile, (1, len(bin_v_profile)))
    cc_profile = bw.getCC(bin_v_profile)
    #
    list_comps = []
    for idx, comp in enumerate(cc_profile) :
        list_comps.append((idx, comp['size']))
    
    #max_comp = max (list_comps, key = lambda x : x[1])
    best_row = int(cc_profile[0]['center_x'])    
    
    lar_image = lar_image[max(0,best_row-40):best_row+20, sub_width-10::]
    return lar_image

#%%

def findCandidateWords(cc_gaps, minimum_gap_size = 2, minimum_word_size = 60):
    """
    This  function detect spliting points based on the separation between words that are called gaps
    input:  a list of gaps, each one represented as a ccomponent    
    output: a list of candidate regions in the form of (start, end)
    """
    #1. compose a list of gap_size
    list_of_gap_size = []
    for idx, gap in enumerate(cc_gaps) :
        list_of_gap_size.append((idx, gap['size']))    
    #2. looking for regions    
    stack=[(0,len(cc_gaps)-1)]
    candidate_words =  []
    while len(stack) > 0 :
        p=stack.pop()
        _start=p[0]
        _end=p[1]
        print(p)
        if (cc_gaps[_end]['center_x'] - cc_gaps[_start]['center_x']) > minimum_word_size and (_end - _start) > 0 :
             p_max=max(list_of_gap_size[_start:_end+1], key = lambda x: x[1])             
             split_gap_id = p_max[0]
             split_gap_size = p_max[1]             
             if split_gap_size > minimum_gap_size :                                   
                 if split_gap_id - _start > 1 :
                     stack.append((_start, split_gap_id-1))
                     candidate_words.append((cc_gaps[_start]['center_x'],cc_gaps[split_gap_id]['min_x']))
                 if _end - split_gap_id > 1 :
                     stack.append((split_gap_id+1,_end))
                     candidate_words.append((cc_gaps[split_gap_id]['max_x'], cc_gaps[_end]['center_x']))
         
    return candidate_words
#%%
def createSetOfGaps(lar_image) :
    """
    This is based on  the horizontal profile of the binary lar_image 
    we compute the gap components using ccomponentes function from basic
    We consider as a non-gap component that with height > 0.1 of the lar's height
    """
    th_otsu = basic.getOtsu(lar_image)
    bw_image = 1 - basic.threshold(lar_image, th_otsu)
    
    bw_image[0:10, :] = 0
    #bw_image[-10::, :] = 0
    
    for i in range(1) :
        bw_image = morph.dilation(bw_image, morph.square(3))
        
    labels = measure.label(bw_image)
    regionprops = measure.regionprops(labels)
    for ccomp in regionprops :
        if ccomp['area'] < 30 :
            rows, cols = zip(*ccomp['coords'])
            bw_image[rows, cols] = 0
    
    #cv2.imshow("binaria", bw_image*255)                
    h_profile = basic.getHorizontalProfile(bw_image)
    h_profile = 1 - basic.threshold(h_profile, 0.1*bw_image.shape[0])
    #reshap h_profile in order it be a 2D array
    h_profile = np.reshape(h_profile, [1, -1])            
    cc_profile = bw.getCC(h_profile)            
    return cc_profile

#%%
def filterCandidateWords(candidate_words, minimum_size, maximum_size) :
    """
    filtered candidate words with respect to the size,
    we can also incorporate constraints about the content
    like the proportion of text in each word. In that case we will need the lar_image
    """
    filtered_list = []
    for word in candidate_words:
        word_size = word[1] - word[0]
        if word_size > minimum_size and word_size < maximum_size :
            filtered_list.append(word)
    return filtered_list
                            

def getCandidateWordsFromLAR(check_image):
    """
    check_image must come in grayscale format
    output 1: lar_image
    output 2: tuples (start, end) defining each candidate word in lar_image
    """    
    lar_image = extractLAR(check_image)
    cc_gaps = createSetOfGaps(lar_image)
    candidate_words = findCandidateWords(cc_gaps)
    candidate_words = filterCandidateWords(candidate_words,  minimum_size = lar_image.shape[1]*0.05, maximum_size = lar_image.shape[1]*0.5)
    return lar_image, candidate_words
    