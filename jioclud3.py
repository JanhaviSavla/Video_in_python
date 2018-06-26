#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:31:37 2018

@author: janhavisavla
"""

import os
import cv2

path = "/Users/janhavisavla/Desktop/Jio_cloud/attachments/"
ext = '.jpg'
output = 'VID.mp4'
fps = 1
images = [img for img in os.listdir(path) if img.endswith(ext)] #Collect all images
width = 900
height = 900
color = [255, 255, 255]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter(output, fourcc, fps, (width,height)) #Create VideoWriter object

for image in images:
    frame = cv2.imread(os.path.join(path, image))
    prev_y = frame.shape[1]
    prev_x = frame.shape[0]
    if abs(prev_x-width)< abs(height-prev_y): #Resize the image according aspect ratio
        x = width
        r = x / prev_y
        y = int(prev_x * r)
        dim = (x,y)
        if y<=height: #If height is less than video frame height, add border to image
            resized = cv2.resize(frame,dim,interpolation = cv2.INTER_AREA)
            if y%2==0 :  
                img_with_border = cv2.copyMakeBorder(resized,int((height/2)-(y/2)) ,int((height/2)-(y/2)), 0, 0, cv2.BORDER_CONSTANT, value=color)
            else:   
                img_with_border = cv2.copyMakeBorder(resized,int((height/2)-(y+1)/2)+1,int((height/2)-(y+1)/2), 0, 0, cv2.BORDER_CONSTANT, value=color)
            video.write(img_with_border) 
        else: #Resize image using normal frame size
            resized = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
            video.write(resized)
    else:
        y = width
        r = y/prev_x
        x = int(prev_y * r)
        dim = (x,y)
        if x<=width:
            resized = cv2.resize(frame,dim,interpolation = cv2.INTER_AREA)
            if x%2==0:
                img_with_border = cv2.copyMakeBorder(resized,0, 0,int((width/2)-x/2) ,int((width/2)-x/2), cv2.BORDER_CONSTANT, value=color)
            else:   
                img_with_border = cv2.copyMakeBorder(resized,0,0,int((width/2)-(x+1)/2)+1 ,int((width/2)-(x+1)/2), cv2.BORDER_CONSTANT, value=color)
            video.write(img_with_border)
        else:
            resized = cv2.resize(frame,(width,height),interpolation = cv2.INTER_AREA)
            video.write(resized)
                
video.release()
            
