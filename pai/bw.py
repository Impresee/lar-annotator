#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 22:18:24 2017

@author: jsaavedr
"""
import numpy as np

def isValid(shape, i,j):
    if (i>=0)  and (j>=0) and (i<shape[0]) and (j<shape[1]):
        return True
    else:
        return False
    
#---trace image
def bw_trace_image(bw_image, bw_sets, i, j, n_cc):    
    p_points=[(i,j)]
    while(len(p_points)>0):
        p=p_points.pop()
        i=p[0]
        j=p[1]
        bw_sets[i,j]=n_cc
        if (isValid(bw_image.shape, i-1,j) and 
            bw_image[i-1,j] == 1 and 
            bw_sets[i-1,j] == 0) :
            p_points.append((i-1,j))        
        #i+1, j
        if (isValid(bw_image.shape, i+1,j) and 
                  bw_image[i+1,j] == 1 and 
                          bw_sets[i+1,j] ==0) :
            p_points.append((i+1,j))
            
        #i, j-1
        if (isValid(bw_image.shape, i,j-1) and 
                  bw_image[i,j-1] == 1 and 
                          bw_sets[i,j-1] ==0) :
            p_points.append((i,j-1))                        
        #i, j+1        
        if (isValid(bw_image.shape, i,j+1) and 
                  bw_image[i,j+1] == 1 and 
                          bw_sets[i,j+1] ==0) :
            p_points.append((i,j+1))
            
        #i-1, j-1
        if (isValid(bw_image.shape, i-1,j-1) and 
                  bw_image[i-1,j-1] == 1 and 
                          bw_sets[i-1,j-1] ==0) :
            p_points.append((i-1,j-1))        
            
        #i-1, j+1
        if (isValid(bw_image.shape, i-1,j+1) and 
                  bw_image[i-1,j+1] == 1 and 
                          bw_sets[i-1,j+1] ==0) :
            p_points.append((i-1,j+1))        
            
        #i+1, j-1
        if (isValid(bw_image.shape, i+1,j-1) and 
                  bw_image[i+1,j-1] == 1 and 
                          bw_sets[i+1,j-1] ==0) :
            p_points.append((i+1,j-1))        
            
        #i+1, j+1
        if (isValid(bw_image.shape, i+1,j+1) and 
                  bw_image[i+1,j+1] == 1 and 
                          bw_sets[i+1,j+1] ==0) :
            p_points.append((i+1,j+1))         
            
    
#define connected-components
def labelComponents(bw_image):
    inds=np.where(bw_image == 1)
    bw_sets=np.zeros(bw_image.shape, dtype=np.uint32)
    n_points=len(inds[0])    
    n_cc=0    
    for p in range(n_points):
        i=inds[0][p]
        j=inds[1][p]
        if(bw_sets[i,j] == 0):
            n_cc=n_cc+1
            bw_trace_image(bw_image, bw_sets, i, j, n_cc)
    return bw_sets, n_cc    
        
#getCC
def getCC(bw_image):
    print("--labeling ")
    bw_sets, n_cc = labelComponents(bw_image)
    print("--labeling OK")
    cc_list = []
    for i_cc in range(1,n_cc+1):
        inds=np.where(bw_sets == i_cc)        
        points = list(zip(inds[0].tolist(), inds[1].tolist()))        
        boundary = [] # getBoundary(points)
        center_x = np.sum(inds[1]) / len(inds[1])
        center_y = np.sum(inds[0]) / len(inds[0])
        minx = min(inds[1])
        miny = min(inds[0])
        maxx = max(inds[1])
        maxy = max(inds[0])
        height = maxy - miny + 1
        width = maxx - minx + 1
        angle = np.arctan2(maxy - miny, maxx - minx)
        cc_list.append({'id': i_cc, 
                        'points' : points, 
                        'size': len(points), 
                        'boundary': boundary,
                        'bounding_box' : (minx, miny, height, width),
                        'angle' : angle,
                        'center_x' : center_x,
                        'center_y' : center_y,
                        'min_x' : minx,
                        'min_y' : miny,
                        'max_x' : maxx,
                        'max_y' : maxy                        
                        })
    return cc_list

# remove components with size < target_size
def removeSmallComponents(cc_list, target_size):
    to_keep = []
    for i, cc in enumerate(cc_list):        
        if (cc['size'] >= target_size):
            to_keep.append(i)    
    new_cc_list = [cc_list[index] for index in to_keep]
    return new_cc_list
    
        
# digital topology: getBoundary
def getBoundary(cc_points):
    print (cc_points)
    if len(cc_points) == 1:
        return cc_points
    rows = [p[0] for p in cc_points]
    cols = [p[1] for p in cc_points]
    
    min_x = np.min(cols)
    min_y = np.min(rows)
    max_x = np.max(cols)
    max_y = np.max(rows)
    
    height = max_y - min_y + 1 + 2
    width = max_x - min_x + 1 + 2        
    
    # creating a simple representation of the component
    cc_array = np.zeros([height, width], np.float32)
    # cc_rows and cc_cols with respect to the cc's size
    cc_rows = rows - min_y + 1
    cc_cols = cols - min_x + 1 
    cc_array[ cc_rows, cc_cols ] = 1
    print(cc_array)
    #neighbors
    l_r=[ 0, -1, -1, -1, 0, 1, 1,  1]
    l_c=[-1, -1,  0,  1, 1, 1, 0, -1]    
    i = cc_rows[0]    
    j = cc_cols[0]
    end = False    
    p1_set = False
    P = (i,j)    
    contour = [P]
    # first point is P
    # point at  right is Q
    idx_q = 0
    P0 = P 
    P1 = (-1,-1)
    #Q0 = (i + l_r[0], j + l_c[0])    
    while not end:        
        Pant = P
        i = P[0]
        j = P[1]        
        idx = idx_q
        print("{} {} {} ".format(i,j,idx))
        #-------------------------------------------------------
        # moving  Q  P until Q=0 and P=1        
        P = (i + l_r[idx], j + l_c[idx])
        Q = (i + l_r[ (idx -1 + 8) % 8], j + l_c[(idx -1 + 8) % 8])
        while cc_array[P] != 1  or cc_array[Q] != 0 :
            idx = (idx + 1 ) % 8
            Q = P
            P = (i + l_r[ idx ], j + l_c[ idx ])
        #-------------------------------------------------------
        #redefining the position of Q with respect to P        
        if P[0] - Q[0] > 0 : 
            idx_q = 2
        elif P[0] - Q[0] < 0 :
            idx_q = 6
        elif P[1] - Q[1] > 0: 
            idx_q = 0
        elif P[1] - Q[1] < 0: 
            idx_q = 4
        else:
            raise  ValueError("something wrong")                
        # stop condition
        if P == P1 and Pant == P0:
            end = True
        else:
            contour.append(P)            
        if not p1_set :
            P1 = P
            p1_set = True     
    
    # getting back to the real coordinates
    rows_p = [p[0] for p in contour ] 
    cols_p = [p[1] for p in contour ]    
    rows_p = rows_p + min_y - 1
    cols_p = cols_p + min_x - 1
    contour = list(zip(rows_p, cols_p))
    return contour            
 
       
#    bw_is_circle
#  we use x**2 + y**2 + Dx + Ey + F = 0
#  cx = -D/2 cy = -E/2 r = sqrt((D**2 + E**2) / 4  - F)    
def estimateCircle(cc):
    boundary = cc['boundary']
    n_points = len(boundary)    
    i_p1 = 0
    i_p2 = int(0.3 * float(n_points))
    i_p3 = int(0.9 * float(n_points))
    p1 = boundary[i_p1]
    p2 = boundary[i_p2]
    p3 = boundary[i_p3]
    print("{} {} {} {}".format(i_p1, i_p2, i_p3, n_points))    
    print("{} {} {} ".format(p1, p2, p3))
    A = np.array ([ [p1[1], p1[0], 1 ], 
                    [p2[1], p2[0], 1 ],    
                    [p3[1], p3[0], 1 ]])
    
    b = np.array([-(p1[1]*p1[1] + p1[0]*p1[0]), 
                  -(p2[1]*p2[1] + p2[0]*p2[0]),
                  -(p3[1]*p3[1] + p3[0]*p3[0])])
    
    x = np.linalg.solve(A,b)
    print(x)
    D = x[0]
    E = x[1]
    F = x[2]
    cx = - D /2
    cy = - E /2
    r =np.sqrt(float(D*D + E*E)/4.0 - F )
    #Compute error betweem estimation and real object
    error = 0
    for p in boundary:
        d = np.sqrt((p[1]-cx)**2 + (p[0]-cy)**2)
        error = error + np.abs(d-r)
    error = error / float(n_points) 
    return cx, cy, r, error    
    
  
    
        
    