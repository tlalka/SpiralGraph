#!/usr/bin/env python3

##
## MAP.PY - Create FITS image files from the galaxy arm zooniverse data files
##
## Version 2.1  01-Jun-2018
##
## Author: Ian Hewitt & Dr. Patrick Treuthardt, NC Museum of Natural Sciences,
##         Nature Research Center, Raleigh, NC USA.
##
## This utility will take the test data output files from the zooniverse
##   galaxy arm mapping project.  These files contain data points which have
##   been marked as lying on the arms of the galaxies.  These points will be
##   mapped to a fits file and the points within an arm will be conbnected
##   with line segments.  In addition, the close arm point to the center will
##   be used to estimate the bar size.
##
## Usage: map.py [-v|--verbose] <files>
##
##   You must specify the name option.
##
##   -v|--verbose    (Optional) Causes more detail (like power value ranges) to
##                   be printed in Results_Short.txt.  Specifying -v or 
##                   --verbose implies -m|--mode as well.
##
##  Revision History:
##         V2.1 - 01-Jun-2018 - Rebase to Ubuntu 16.04 LTS (minor changes)
##         V2.0 - 20-Dec-2017 - Updated for Spiral Graph format in DEc 2017
##         V1.2 - 27-Jul-2017 - Change mapping to NOT add 10% border around
##                              the image radius
##         V1.1 - 13-Jul-2017 - Change to add keywords BAR, ARMS, and the
##                              version to the generated FITS image file.
##                            - Trim image so that the arms go almost to the
##                              edge of the image for better analysis results.
##                            - Change default size of image to 511
##                            - Fix bug in bar/core size calculation
##                            - Fix bug in meesage printed in verbose mode
##                              which caused the program to crash.
##         V1.0 - 06-Jul-2017 - Initial version
##
##  Requirements/Environment:
##
##     This program was created under Python 3.x and Astroconda. 
##

## Import System Libraries 

import os
import re
import sys
import argparse
from PIL import Image as pil
import numpy as np
from astropy.io import fits
import shutil

##
## Main Loop
##

def main():

## Constants 

    VERSION='2.0/20171220'
    X=240
    Y=240
    Z = [512]
    GALS=1000
    jpg = ["nill"]

## Get command line arguments using argparse.

    options = argparse.ArgumentParser(description="This Utility Will Map The Data From The Zooniverse Galaxy Arm Project")
    options.add_argument('files',help='Input data files')
    options.add_argument('-v','--verbose',help='Provide Very Detiled Results For Each File - Optional',action="store_true",default=False)    
    args=options.parse_args()

##
## Set up the arrays for the galaxy arm data points (tuples)
##

    bar=[0.0 for g in range(0,GALS)]
    xcenter=[0 for g in range(0,GALS)]
    ycenter=[0 for g in range(0,GALS)]
    galaxy_arms=[[[(0.0,0.0) for g in range(0,GALS)] for h in range(0,7)] for i in range(0,128)]

##
## Read in the data file(s) and parse the text files for the data points.  This
##   code uses the Python Regular Expression library.  If you are not familiar
##   with this, please see https://docs.python.org/2/howto/regex.html
##

    gal_index=-1

##
## Test if file exists (ADD)
##
    path = input("Please enter path to picture folder (don't enter final backslash). 'test/rotated' for test")
    dirname = path+'/line'
    if(os.path.isdir(dirname)):
        print("line folder already exists")
        shutil.rmtree(dirname)
        os.mkdir(dirname)
    else:
        os.mkdir(dirname)

    with open(args.files) as g:
        g_lines = g.readlines()

    arm=0
    gal_index+=1

    for line in g_lines:
        
        if line[0]==']' or line[0]=='[' or line[0]==',':
            print('Skip [/]')
            continue

        if 'task' in line:
            print('                                     Task skip')
            #get jpg file name
            jpg2 = path+'/'+line[7:33]
            jpg.append(line[7:31])
            im= pil.open(jpg2)
            X=im.size[0]
            Y=im.size[1]
            Z.append(im.size[0])
            print("jpg" + str(im.size))
            gal_index+=1
            arm = 0
            bar=[0.0 for g in range(0,Z[gal_index])]
            xcenter=[0 for g in range(0,Z[gal_index])]
            ycenter=[0 for g in range(0,Z[gal_index])]
            continue

        if 'tool' in line:
            arm+=1
            arm_index=0
            print('                         Tool Skip')
            continue

##            coords=line.split(',')
##            x=coords[0].split(':')
##            y=coords[1].split(':')

        coords=re.findall(r'"x":([0-9]+.[0-9]+),"y":([0-9]+.[0-9]+)',line)

        if coords:

## Do a quick error check here.  If we have valid tuples, then we should have
##   have sane values for the gal_index and arm values.  If not, complain.

            if (arm < 1) or (arm > 6) or (gal_index < 0):
                print('WARNING: Data line found before valid header line - Skipping Line '+line)

## We have a set of 1or more 2 value tuples, get the tuples copied to the array

            for point in coords:
                print('arm: '+str(arm)+' ind: '+str(arm_index)+' coords: *{0}*'.format(coords) + ' gal' + str(gal_index))
                galaxy_arms[gal_index][arm][arm_index]=(float(point[0]),float(point[1]))
                arm_index+=1
## If we hit this else, it's not a header line or data line, but we print it
##   out if the -v option was specified

        else:
            print('ERROR: Cannot Match Input Line: '+line)

## Now have all the galaxy data, so it can be mapped for each galaxy
    for gal in range(1,gal_index+1):
        X = Z[gal]
        Y = Z[gal]
        print('Mapping Galaxy '+str(gal) + " X " + str(X) + " Y " + str(Y)+ " z " + str(Z[gal]))

        bar[gal]=float(X)
        xcenter[gal]=int(X/2)
        ycenter[gal]=int(Y/2)

        minX=X
        minY=Y
        maxX=1
        maxY=1
        image=np.zeros((X,Y),dtype=np.float32)

## Now map each arm into the array

        num_arms=0
        last_a=0
        for a in range(1,7):
            pindex=0
            print(galaxy_arms[gal][a][pindex])
            while galaxy_arms[gal][a][pindex] != (0.0,0.0):
                if last_a != a:
                    num_arms+=1
                    last_a=a

## New

                image[int(galaxy_arms[gal][a][pindex][0])][int(galaxy_arms[gal][a][pindex][1])]=255.0

## Determine if this is a new outer limit for the arm mapping

#print(str(galaxy_arms[gal][a][pindex][0]) + " maxX " + str(maxX))
                if int(galaxy_arms[gal][a][pindex][0]) > maxX:
                    maxX=int(galaxy_arms[gal][a][pindex][0])
                #print(str(galaxy_arms[gal][a][pindex][0]) + " minX " + str(minX))
                if int(galaxy_arms[gal][a][pindex][0]) < minX:
                    minX=int(galaxy_arms[gal][a][pindex][0])

                if int(galaxy_arms[gal][a][pindex][1]) > maxY:
                    maxY=int(galaxy_arms[gal][a][pindex][1])
                if int(galaxy_arms[gal][a][pindex][1]) < minY:
                    minY=int(galaxy_arms[gal][a][pindex][1])
                
## Determine distance to the center to try and determine the bar/core size

                xdistance=abs(float(galaxy_arms[gal][a][pindex][0])-float(X/2))
                ydistance=abs(float(galaxy_arms[gal][a][pindex][1])-float(Y/2))
                distance=(xdistance**2+ydistance**2)**0.5

                if distance < bar[gal]:
                    bar[gal]=distance

## Connect the points
                
                if pindex > 0:
                    x=float(galaxy_arms[gal][a][pindex][0])
                    y=float(galaxy_arms[gal][a][pindex][1])
                    last_x=float(galaxy_arms[gal][a][pindex-1][0])
                    last_y=float(galaxy_arms[gal][a][pindex-1][1])

                    if (int(last_x)-int(x)) != 0.0:
                        slopex=(y-last_y)/abs(last_x-x)
                    else:
                        slopex=0.0

                    if (int(last_y)-int(y)) != 0.0:
                        slopey=(x-last_x)/abs(last_y-y)
                    else:
                        slopey=0.0

                    if args.verbose:
                        print('X='+str(x)+' Y='+str(y)+' LAST_X='+str(last_x)+' LAST_Y='+str(last_y))
                        print('SLOPEX='+str(slopex)+' SLOPEY='+str(slopey))

                    if (abs(last_x-x)>abs(last_y-y)):
                        pts=int(abs(last_x-x))
                        if slopey < 0:
                            slopey=-1.0
                        else:
                            slopey=1.0
                    else:
                        pts=int(abs(last_y-y))
                        if slopex < 0:
                            slopex=-1.0
                        else:
                            slopex=1.0

                    for t in range(1,pts):
                        ax=int(last_x)+int(slopey*float(t))
                        by=int(last_y)+int(slopex*float(t))
                        image[ax][by]=255.0

                pindex+=1
#move the image saving statments here if you want it uncropped

## Trim the image so that There is only 10% blank space beyond the end of the
##   most distant arm.
        print("cropping " + str(Z[gal]) + " maxX " + str(maxX)+" maxy " + str(maxY) + " minX " + str(minX)+" miny " + str(minY))
    
        if (maxX-(X/2)) > ((X/2-minX)):
            xsize=int(maxX-(X/2))
        else:
            xsize=int((X/2)-minX)

        if (maxY-(Y/2)) > ((Y/2-minY)):
            ysize=int(maxY-(Y/2))
        else:
            ysize=int((Y/2)-minY)

        if xsize > ysize:
            size=xsize+int(0.0*float(xsize))
        else:
            size=ysize+int(0.0*float(ysize))

        if args.verbose:
            print('maxX='+str(maxX)+' minX='+str(minX)+' maxY='+str(maxY)+' minY='+str(minY))
            print('xsize='+str(xsize)+' ysize='+str(ysize)+' X='+str(X)+' Y='+str(Y))
            print('size='+str(size))

        if size > X-1:
            size=int((X/2)-1)

#find the furthest point from the center
        center = Z[gal]/2
        minX2 = center - minX
        maxX2 = maxX - center
        minY2 = center - minY
        maxY2 = maxX - center

        lower=int((X/2)-size)
        upper=int((X/2)+size)
        dim=(size*2)+1

        print(" maxX2 " + str(maxX2)+" maxy2 " + str(maxY2) + " minX2 " + str(minX2)+" miny2 " + str(minY2) + " center "  + str(center))
        if(minX2 > maxX2):
            buffer = minX2
        else:
            buffer = maxX2
        if (buffer < minY2):
            buffer = minY2
        if (buffer < maxY2):
            buffer = maxY2

        dim = int(buffer + buffer/10) * 2
        lower = int(Z[gal]/2 - dim/2)
        print("dim " + str(dim) + " lower " + str(lower))

        if args.verbose:
            print('Upper='+str(upper)+' Lower='+str(lower))
            print('Size='+str(size)+' Dim='+str(dim))

        if(dim > 0):
            new_image=np.zeros((dim,dim),dtype=np.float32)
        else:
            new_image = image

        for i in range(0,dim):
            for j in range(0,dim):
                new_image[i][j]=image[(lower+i)][(lower+j)]

        os.system('rm -f '+path+'/line/L_'+str(jpg[gal])+'.fits')
        hdu=fits.PrimaryHDU(new_image)
        hdu.writeto(path+'/line/L_'+str(jpg[gal])+'.fits')
        fits.setval(path+'/line/L_'+str(jpg[gal])+'.fits','BAR',value=str(bar[gal]))
        fits.setval(path+'/line/L_'+str(jpg[gal])+'.fits','ARMS',value=str(num_arms))
        fits.setval(path+'/line/L_'+str(jpg[gal])+'.fits','COMMENT',value='Generated by map.py Version '+VERSION)
        del(image)

## This is the End of Main Program

## Call the main() function

if __name__ == '__main__':
    main()

