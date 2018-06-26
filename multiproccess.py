#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 17:38:36 2018

@author: test
"""
import os
import sys
import multiprocessing
sys.path.append(os.path.abspath("/Users/janhavisavla/Desktop/Jio_cloud/"))
import videocode
from multiprocessing import Queue, Process, cpu_count


def myMultiprocessing(root_folder):
    '''
    Splits the source filelist into sublists according to the number of CPU cores and provides multiprocessing of them.
    '''
    files = os.listdir(root_folder)
    #q = Queue()
    procs = []
    for k in range(0,4):
        # Split the source filelist into several sublists.
        lst = [files[j] for j in range(1, len(files)) if j % 4 == k]
        print(lst)
        
        if len(lst)>0:
            p = Process(target=videocode.main, args=(lst, root_folder))
            p.start()
            procs += [p]
    
    #all_results = []
    p.join()
    #for i in range(0, len(procs)):
        # Save all results from the queue.
    #while(q):
        #all_results += q.get()

            
root_folder = "/Users/janhavisavla/Desktop/Image_test_data/Parent_dir/"

if __name__ == "__main__":
    myMultiprocessing(root_folder)
