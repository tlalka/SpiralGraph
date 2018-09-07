import sys, os
import numpy as np
import pandas as pd
import json

#This program takes a "clean" classification file, and averaged the values of the ellipese for each jpg
#The "averaged" file will be used with the "rotate" script to deproject the images

project_name = "spiral-graph"

infile        = "%s-clean.csv" % project_name


classifications= pd.read_csv(infile)
print("start")


w = 8 #width, how many values we need to keep track of id, x, y, rx, ry, angle, jpg, count
h = 3 #height, how many different pictures we are classifying YOU MAY NEED TO CHANGE THIS
d = 10 #depth, how many duplicates of each picture we have YOU MAY NEED TO CHANGE THIS

classes = 0 #how many images we found

data = []


foth = open("%s-averaged.csv"  % project_name, "w")


# write the header line for each of the files
foth.write("classification_id,x,y,rx,ry,angle,filename\n")


# read the clean file and average all the values into our list

for i, row in enumerate(classifications.iterrows()):
    # row[0] is the index, [1] is the classification info
    cl = row[1]
    
    same = False
    x = cl['x']
    y = cl['y']
    rx = cl['rx']
    ry = cl['ry']
    angle = cl['angle']
    subject_id   = cl['subject_id']
    jpg   = cl[6]
	
    # the image which was classified
    print ("from document = " + str(subject_id))

    # check if this id is new, or saved
    for list in data:
        if (classes > 0)and(list[0] == subject_id):
            print ("This one is already in data = " + str(list))
            same = True
            #this value is already in here, so we can average it in and break the loop
            list[1] += x/d
            list[2] += y/d
            list[3] += rx/d
            list[4] += ry/d
            list[5] += angle/d
            list[7] += 1
            break
        else:
            same = False

    if (same == False):
        # we didn't find it, so we need to create a fresh entry
        classes += 1
        print ("was not found in data, so add new. This many now = " + str(classes))
        data.append([subject_id,(x/d),(y/d),(rx/d),(ry/d),(angle/d),jpg,1.0])

#go through list, make sure the count is right, and save to a file
for list in data:
    if (list[7] != 10):
        print ("ERROR: %s has a count of %i. Value saved anyway" % (list[0], list[7]))

    print(list[0])

    foth.write("%d, %.2f, %.2f, %.2f, %.2f, %.2f, %s\n" % (list[0], list[1], list[2], list[3], list[4], list[5], list[6]))
               
if (classes != h):
	 print ("ERROR: only %i different pictures found. Values saved anyway" % (classes))

foth.close()


print("done")


#
