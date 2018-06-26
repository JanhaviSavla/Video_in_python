#  !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:38:13 2018

@author: test
"""
#OKAY SO NOW I WILL TRY TO WRITE AN EFFICIENT CODE 

from moviepy.editor import *
import os
import json
import multiprocessing
from multiprocessing import Queue, Process, cpu_count

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
    
    #def getPath(self):
        #return self.datastore['path']
    

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
    i=0
    for image in images[0:10]: 
        img=ImageClip(path+'/'+image).set_duration(i).resize(height= H, width=W)
        clips_slided.append(img)
        i+=2
    return clips_slided,i
    
def addCrossfadeEffect(images,path,H,W,delay):
    clips_crossfade=[]
    for image in images[10:]:
        img=ImageClip(path+'/'+image).set_duration(2).resize(height= H ,width= W)
        clips_crossfade.append(img.crossfadein(delay))
    return clips_crossfade
    
def createVideo(clips_crossfade,clips_slided,W,H,i):
    final2 = concatenate(clips_crossfade,
    padding=-delay, method="compose")
    final1=CompositeVideoClip(clips_slided, size=(W,H)).set_duration(i/2)
    basic_clip = concatenate_videoclips([final1,final2])
    return basic_clip

def addAudio(clip,music):
    audio = AudioFileClip(music).set_duration(20)
    clip_with_audio = clip.set_audio(audio)
    return clip_with_audio
    
'''def addIcon(clip,icon):
    logo = (ImageClip(icon).set_duration(20).margin(right=8, top=8, opacity=0).set_pos(("right","bottom")))
    final_clip = CompositeVideoClip([clip, logo])
    return final_clip'''
        
def releaseVideo(clip,filename):
    clip.write_videofile(filename+"video.mp4", fps=24, audio_codec="aac")
    
def main(files, root_folder):
    for filename in files:
        filepath=root_folder+filename
        images = [img for img in os.listdir(filepath) if img.endswith(ext)] 
        clips_crossfade = addCrossfadeEffect(images, filepath , t.getHeight(), t.getWidth(), delay)
        clips_slided,i = addSlidedEffect(images,filepath ,t.getHeight(),t.getWidth())
        clips_slided = [add_transition(len(clips_slided), x, clip) for x, clip in enumerate(clips_slided)]
        basic_clip = createVideo(clips_crossfade,clips_slided,t.getWidth(),t.getHeight(),i)
        final_clip = addAudio(basic_clip,t.getMusic())
        #queue.put(final_clip)
        releaseVideo(final_clip,filename)
    
t=Tobenamed()
ext='.jpg'
delay=1
HX = t.getHeight()+t.getHeight()*.10
WX = t.getWidth()+t.getWidth()*.10
