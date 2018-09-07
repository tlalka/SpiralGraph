import os
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
from scipy.misc import imrotate
from PIL import Image as pil
from scipy.misc import imsave
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import rotate
import scipy.misc
import cv2

#this script takes a "clean" cvs file, and the jpgs that match the "filename" colum, and deproject them
#run this script inside the folder that contains the origional images, and it will place the new ones in a folder called "rotated"
#make sure a rotate folder doesn't already exist
#it will produce one image called "rotated.jpg" as a middle step

project_name = "spiral-graph"

infile        = "%s-averaged.csv" % project_name

classifications = pd.read_csv(infile)
dirname = 'rotated'
if(os.path.isdir("/rotated")):
    print("rotated folder already exists")
else:
    os.mkdir(dirname)

for i, row in enumerate(classifications.iterrows()):

    cl = row[1]
    angle = cl['angle']
    ry = cl['ry']
    rx = cl['rx']
    name =cl['filename']
    #name = name[2:]
    print(name)
    myimage = pil.open(name)

    img = rotate(myimage, angle, reshape=True)
    
    imsave("rotated.jpg",img)

    stretch = 2 - (ry/rx)

    h, w = img.shape[:2]

#RX MUST BE BIGGER THAN RY OR THE PHOTO WILL LOOK LIKE A LONG HORIZONTAL LINE
    scaled_img = cv2.resize(img, None, fx=1, fy=stretch, interpolation = cv2.INTER_LINEAR) # scale image
    sh, sw = scaled_img.shape[:2] # get h, w of scaled image
    center_y = int(sh/2 - h/2)
    center_x = int(sw/2 - w/2)
    cropped = scaled_img[center_y:center_y+h, center_x:center_x+w]
    newname = "r_" + name
    imsave(os.path.join(dirname, newname),cropped)


print("done")


#
