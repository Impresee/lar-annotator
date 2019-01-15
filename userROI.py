# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 10:33:19 2018

@author: Impresee
"""
from userROIclass import userROIclass

import argparse
 
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dataset', type=str, default=None, required = True) #path donde esta el dataset
    parser.add_argument('-output', type=str, default=None, required = True) #path donde se guardan los resultados
    args = parser.parse_args()
    userROIclass(args.dataset,args.output)
    
#if __name__=="__main__":
main()