#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:32:11 2018

@author: janhavisavla
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:37:03 2018

@author: janhavisavla
"""

from moviepy.editor import *
import os
import json
import multiprocessing
from multiprocessing import Queue, Process, cpu_count
from PIL import Image

class Tobenamed:
    def __init__(self):
        filename="/Users/janhavisavla/Desktop/Jio_cloud/data.json"
        if filename:
            with open(filename, 'r') as f:
                self.datastore = json.load(f)
                
    def getWidth(self):
        return self.datastore['W']
    
    def getHeight(self):
        return self.datastore['H']
    
    def getMusic(self):
        return self.datastore['music']
    
    def getIcon(self):
        return self.datastore['icon']
    
    def getPath(self):
        return self.datastore['path']
    

def slide_out(clip, duration, height, counter):
    def calc(t, counter, duration, h):
        ts = t - (counter * duration)
        val = min(-45, h*(duration-ts))
        return ('center', val)
    return clip.set_pos(lambda t: calc(t, counter, duration, height))

def add_transition(clip_size, counter, clip):
    counter = clip_size - 1 - counter
    return slide_out(clip.resize(height= HX,width=WX), 2, HX, counter)
    
def addSlidedEffect(images, path, H, W):
    clips_slided=[]
    i=3
    for image in images[0:7]: 
        img=ImageClip(path+'/'+image).set_duration(i).resize(height= H, width=W)
        clips_slided.append(img)
        i+=2
    return clips_slided,i
    
def addCrossfadeEffect(images,path,H,W,delay,text_back):
    clips_crossfade=[]
    for image in images[7:]:
        img=ImageClip(path+'/'+image).set_duration(3).resize(height= H ,width= W)
        clips_crossfade.append(img.crossfadein(delay))
    clips_crossfade.append(text_back)
    return clips_crossfade
    
def createVideo(first,middle,clips_crossfade,clips_slided,W,H,i):
    last = concatenate(clips_crossfade,
    padding=-delay, method="compose")
    final2=CompositeVideoClip(clips_slided, size=(W,H)).set_duration(i/2)
    #final1=concatenate(clips_slided,padding=-delay,method="compose")
    basic_clip = concatenate_videoclips([first,final2,middle,last])
    return basic_clip

def addAudio(clip,music):
    audio = AudioFileClip(music).set_duration(40)
    clip_with_audio = clip.set_audio(audio)
    return clip_with_audio

def addTextFront(W,H):
    img = Image.open(path2)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 80)
    draw.text((600, 450),"Welcome to Atasa!",(0,0,0),font=font)
    img.save(path2+'frame_with_text_front.jpg')
    first = ImageClip(path2+'frame_with_text_front.jpg').set_duration(3).resize(height= H ,width= W)
    return first

def addTextMiddle(W,H):
    img = Image.open(path2)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 80)
    draw.text((600, 450),"And there's more....",(0,0,0),font=font)
    img.save(path2+'frame_with_text_middle.jpg')
    middle = ImageClip(path2+'frame_with_text_middle.jpg').set_duration(3).resize(height= H ,width= W)
    return middle 

def addTextBack(W,H):
    img = Image.open(path2)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 80)
    draw.text((400, 500),"With Love from all of us at Jio",(0,0,0),font=font)
    img.save(path2+'frame_with_text_back.jpg')
    text_back = ImageClip(path2+'frame_with_text_back.jpg').set_duration(3).resize(height= H ,width= W)
    return text_back 
    
'''def addIcon(clip,icon):
    logo = (ImageClip(icon).set_duration(20).margin(right=8, top=8, opacity=0).set_pos(("right","bottom")))
    final_clip = CompositeVideoClip([clip, logo])
    return final_clip'''
        
def releaseVideo(clip):
    clip.write_videofile("videonevvw.mp4", fps=24, audio_codec="aac")
    
def main():
    images = [img for img in os.listdir(t.getPath()) if img.endswith(ext1)] 
    '''for img in os.listdir(t.getPath()):
        if img.endswith(ext1) :
            im = Image.open(t.getPath()+'/'+img)
            im = im.convert('RGB')
            im.save(t.getPath()+'/'+img+'.jpg', quality=95)
    images = [img for img in os.listdir(t.getPath()) if img.endswith(ext1)]'''
    first = addTextFront(t.getWidth(),t.getHeight())
    text_back = addTextBack(t.getWidth(),t.getHeight())
    middle = addTextMiddle(t.getWidth(),t.getHeight())
    clips_crossfade = addCrossfadeEffect(images, t.getPath() , t.getHeight(), t.getWidth(), delay,text_back)
    #print(clips_crossfade)
    clips_slided,i = addSlidedEffect(images,t.getPath() ,t.getHeight(),t.getWidth())
    clips_slided = [add_transition(len(clips_slided), x, clip) for x, clip in enumerate(clips_slided)]
    print(clips_slided)
    basic_clip = createVideo(first,middle,clips_crossfade,clips_slided,t.getWidth(),t.getHeight(),i)
    final_clip = addAudio(basic_clip,t.getMusic())
        #queue.put(final_clip)
    releaseVideo(final_clip)
    

#root_folder = "/Users/janhavisavla/Desktop/Image_test_data/Parent_dir/"
#main()
#images = [img for img in os.listdir(t.getPath()) if img.endswith(ext1) or img.endswith(ext2)] 

from PIL import Image,ImageOps
import os
from PIL import ImageFont
from PIL import ImageDraw 

#path = "/Users/janhavisavla/Desktop/Jio_cloud/attachments/"
extension1='.JPG'
extension2='.jpg'
images = [img for img in os.listdir(t.getPath()) if img.endswith(extension1) or img.endswith(extension2)]
background = Image.open('/Users/janhavisavla/Desktop/Jio_cloud/Archive/temp2.jpg','r')
basewidth, hsize = 1400, 800
offset = (250,132)

for image in images :
    img = Image.open(t.getPath()+image, 'r')
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img = ImageOps.expand(img,border=15,fill='white')
    background.paste(img, offset)
    f, e = os.path.splitext(t.getPath()+image)
    background.save(f+'_frame.jpg')
    
t=Tobenamed()
ext1='frame.jpg'
delay=0.5
HX = t.getHeight()+t.getHeight()*.10
WX = t.getWidth()+t.getWidth()*.10
path2="/Users/janhavisavla/Desktop/Jio_cloud/Archive/temp1.jpg"
main()