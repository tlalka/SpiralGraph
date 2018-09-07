#!/usr/bin/env python3

import os
import re
import sys
import argparse
import ast
import math
from PIL import Image
import numpy as np
from astropy.io import fits

##
## Main Loop
##

def main():

    image_file = "star.fits"
    image = fits.open(image_file)
    size = 512
    data = image[0].data
    a = data[int(size/2),int(size/2)]
    b = data[int(size/2 + size/6),int(size/2 + size/6)]
    c = data[int(size/2 + size/6),int(size/2 - size/6)]
    d = data[int(size/2 - size/6),int(size/2 + size/6)]
    e = data[int(size/2 - size/6),int(size/2 - size/6)]
    image.close()
    
    print(str(a)+" "+str(b)+" "+str(c)+" "+str(d)+" "+str(e))
    
    if(a == 0.0 or b == 0.0 or c == 0.0 or d == 0.0 or e == 0.0):
        print("no good")
    
    #get 90th percentile
    vmin = np.percentile(data, 5)
    vmax = max(data[int(size/2),int(size/2)],
                  data[int(size/2)-1,int(size/2)-1],
                  data[int(size/2)-1,int(size/2)],
                  data[int(size/2),int(size/2)-1],
                  data[int(size/2)+1,int(size/2)+1],
                  data[int(size/2)+1,int(size/2)],
                  data[int(size/2),int(size/2)+1],
                  data[int(size/2)+1,int(size/2)-1],
                  data[int(size/2)-1,int(size/2)+1])
    #data[data < vmin] = vmin
#for i in range(int(size/2)-5, int(size/2)-5)
#   print(data[>,])
    #if(os.path.isfile('B'+image_file)):
    #   os.remove('B'+image_file)
    

    #hdu=fits.PrimaryHDU(data)
    #hdu.writeto('B'+image_file)
    
    #fits2jpg(data, .5,1.5, 'test.fits')
    os.system("source activate iraf27")
    #os.system("ds9 " +image_file+" -log -cmap value 1 .5 -export jpeg ex.jpeg 100 -quit")
    #print("ds9 B" +image_file+" -scale limits " +str(vmin)+" "+str(vmax)+ " -log -export jpeg ex.jpeg 100")
    os.system("ds9 " +image_file+" -scale limits " +str(vmin)+" "+str(vmax)+ " -log -export jpeg ex.jpeg 100")
  
    #crop image
    #name = 'ex.jpeg'
    #image_j = Image.open(name)
    #cropped_j = image_j.crop((241, 113, 497, 369))
    #cropped_j.save("cr.jpeg")

    sys.exit()

if __name__ == '__main__':
    main()

