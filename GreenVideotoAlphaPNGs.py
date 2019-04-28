#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import numpy
import math

import youtube_dl

import cv2
from PIL import Image
from PIL import ImageChops

from natsort import natsorted, ns

import argcomplete
import argparse

# python3 GreenVideotoAlphaPNGs.py https://www.youtube.com/watch?v=ybX4VuArZOQ

VIDEO_URL = 'https://www.youtube.com/watch?v=ybX4VuArZOQ'


"""
https://www.reddit.com/r/Python/comments/m68js/trying_to_write_a_very_simple_green_screen_code/
https://en.wikipedia.org/wiki/Chroma_key
http://www.cs.utah.edu/~michael/chroma/
"""
def GreenScreen(infile,outfile='output.png', keyColor=None, tolerance = None):
    
    #open files
    inDataFG = Image.open(infile).convert('YCbCr')

    #make sure values are set
    if keyColor == None:keyColor = inDataFG.getpixel((1,1))
    if tolerance == None: tolerance = [50,130]
    [Y_key, Cb_key, Cr_key] = keyColor
    [tola, tolb]= tolerance
    
    (x,y) = inDataFG.size #get dimensions
    foreground = numpy.array(inDataFG.getdata()) #make array from image
    maskgen = numpy.vectorize(colorclose) #vectorize masking function

    
    alphaMask = maskgen(foreground[:,1],foreground[:,2] ,Cb_key, Cr_key, tola, tolb) #generate mask
    alphaMask.shape = (y,x) #make mask dimensions of original image
    imMask = Image.fromarray(numpy.uint8(alphaMask))#convert array to image
    invertMask = Image.fromarray(numpy.uint8(255-255*(alphaMask/255))) #create inverted mask with extremes
    
    #create images for color mask
    colorMask = Image.new('RGBA',(x,y),tuple([0,0,0,0]))
    allgreen = Image.new('YCbCr',(x,y),tuple(keyColor))
    
    colorMask.paste(allgreen,invertMask) #make color mask green in green values on image
    inDataFG = inDataFG.convert('RGBA') #convert input image to RGB for ease of working with
    cleaned = ImageChops.subtract(inDataFG,colorMask) #subtract greens from input
    
    cleaned.save(outfile, "PNG") #save cleaned image

    
def colorclose(Cb_p,Cr_p, Cb_key, Cr_key, tola, tolb):
    temp = math.sqrt((Cb_key-Cb_p)**2+(Cr_key-Cr_p)**2)
    if temp < tola:
        z= 0.0
    elif temp < tolb:
        z= ((temp-tola)/(tolb-tola))
    else:
        z= 1.0
    return 255.0*z

# Get video title
def info_video(link):
    with youtube_dl.YoutubeDL({'quiet': True, 'no_warnings': True, 'simulate': True}) as ydl:
        return ydl.extract_info(link)['title']

# Download video for youtube    
def dl_video(link):
    ydl_opts = {
            'format':'mp4',
            'outtmpl': "{}.mp4".format(info_video(link)),
            'no_warnings': True,
           #  'quiet': True
               }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        return "{}.mp4".format(ydl.extract_info(link)['title'])
    
# Download audio for youtube    
def dl_audio(link):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': "{}.mp3".format(info_video(link)),
    # 'quiet': True,
    'no_warnings': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        return "{}.mp3".format(ydl.extract_info(link)['title'])
    
# Video to image
"""https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames"""
def video_to_images(video_name):
    if os.path.isfile(video_name): 
        vidcap = cv2.VideoCapture(video_name)
        success,image = vidcap.read()
        count = 0
        if not os.path.exists(video_name[:-4]):
            os.makedirs(video_name[:-4])

        while success:
          cv2.imwrite("{}/{}.png".format(video_name[:-4], count), image)     # save frame as JPEG file      
          success,image = vidcap.read()
          count += 1
        print('convert video to a image')
    else:
        print("not exist")

# Remove green in each image
def removeGreenDir(directory):
    if os.path.isdir(directory):
        images = [img for img in natsorted(os.listdir(directory), alg=ns.PATH) if img.endswith(".png")]
        if not os.path.exists("{}_alpha".format(directory)):
            os.makedirs("{}_alpha".format(directory))
        for filename in images:
                GreenScreen("{}/{}".format(directory,filename), "{}_alpha/{}".format(directory,filename))
        print('removed the green for pngs')
    else:
        print("not exist")

def create_project_dir():
    video_title = info_video(args.link)
    project_dir = "project_{}".format(video_title)
    os.makedirs(project_dir)
    for fname in os.listdir('.'):
        if(fname.startswith(video_title)):
            os.rename(fname,"{}/{}".format(project_dir, fname))
    print("create dir and move file")

if __name__ == '__main__':
        
    def _parser():
        parser = argparse.ArgumentParser(description="Green Screen Video to sequence of PNGs with alpha layer in python")
        parser.add_argument('link', type=str, help='link')
        return parser
    
    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()  

    video_name = dl_video(args.link) #Download video
    dl_audio(args.link) #Download audio

    video_to_images(video_name) #VideoToPNGs
    removeGreenDir(video_name[:-4]) #RemoveGreen
    create_project_dir() # create project directory
    print("done")
