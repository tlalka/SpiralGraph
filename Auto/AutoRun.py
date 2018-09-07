#provide this program a name to a directory that has a "spiral-graph-classifications.csv", the origional photos, and the "Spirals_jpg.csv" and it will automatically upload the new images to the second workflow of Spiral Graph zooniverse project

import sys, os
import csv
import numpy as np
import pandas as pd
import json
from panoptes_client import Panoptes, Project, SubjectSet, Subject
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
from scipy.misc import imrotate
from PIL import Image as pil
from scipy.misc import imsave
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import rotate
import scipy.misc
import cv2
import shutil

path = input("Please enter path to picture folder (don't enter final backslash). 'test' for test")



#pull data down
#print("Gathering ellipse export...")
#classifications_all = project.get_export('classifications')
#check data is here


print("Generating \"clean\" file. If file is not what you expected, check that workflow_id and workflow_version are correct")
#clean data
project_name = "spiral-graph"
infile        = input("Please enter the name and path for the classifcations file")

if(not(os.path.isfile(infile))):
    print("no classification file found")
    sys.exit()

classifications_all = pd.read_csv(infile)
classifications_all['anno_json'] = [json.loads(q) for q in classifications_all['annotations']]
classifications_all['sub_data'] = [json.loads(q) for q in classifications_all['subject_data']]
classifications = classifications_all

op = path+"/"+project_name+"-clean.csv"
foth = open(op, "w")


# write the header line for each of the files
# each has the basic classification information + the mark information
# including sanity check stuff + stuff we may never need, like the tool number
# and the frame the user drew the mark on, respectively

# the other/interesting marker is an ellipse+tag: {(x, y), (rx, ry), angle, text}
foth.write("subject_id,x,y,rx,ry,angle, filename, spiral percentage\n")


# now extract the marks from each classification

i_empty = 0
i_mark = 0
for i, row in enumerate(classifications.iterrows()):
    # row[0] is the index, [1] is the classification info
    cl = row[1]
    
    class_id   = cl['classification_id']
    subject_id = cl['subject_ids']
    created_at = cl['created_at']
    username   = cl['user_name']
    userid     = cl['user_id']
    userip     = cl['user_ip']
    
    # the image which was classified
    #print (subject_id)
    #jpg = cl['subject_data'][329:353]
    jpgint = cl['subject_data'].find('jpg')
    jpg = cl['subject_data'][(jpgint+19):(jpgint+19+24)]
    #revjpg = rev[3:27]
    #jpg = revjpg[::-1]
    print(jpg)
    
    yes = cl['anno_json'][1]['value'][4:6]
    #print(yes)
    if(yes == 'St'):
        spiral = 1
    elif(yes == 'Sm'):
        spiral = 0
    else:
        spiral = -1
        print("Error: cannot determine yes or no")
    #sys.exit()
    # for anonymous users the userid field is blank so reads as NaN
    # which will throw an error later
    if np.isnan(userid):
        userid = -1

    # loop through annotations in this classification
    # (of which there can be arbitrarily many)
    for j, anno in enumerate(cl['anno_json']):
        #print(j)
        # first, if this classification is blank, just write the basic information
        if len(anno['value']) < 1:
            i_empty+=1
            femp.write("%d,%d,\"%s\",\"%s\",%d,%s, %d\n" % (class_id, subject_id, created_at, username, userid, userip, spiral))
        elif (j == 0):
            # it's not empty, so let's collect other info
            # the marks themselves are in anno['value'], as a list
            
            for i_v, thevalue in enumerate(anno['value']):
                i_mark+=1
                
                #normalize values
                angle = thevalue['angle']
                
                if thevalue['rx'] > thevalue['ry']:
                    if angle >= 90:
                        angle -= 180
                    
                    if angle < -90:
                        angle += 180
                    
                    foth.write("%d,%.2f,%.2f,%.2f,%.2f,%.2f, %s, %d\n" % (subject_id, thevalue['x'], thevalue['y'], thevalue['rx'], thevalue['ry'], angle, jpg, spiral))
                
                else:
                    angle += 90
                    
                    if angle >= 90:
                        angle -= 180
                    
                    if angle < -90:
                        angle += 180
                    
                    foth.write("%d,%.2f,%.2f,%.2f,%.2f,%.2f, %s, %d\n" % (subject_id, thevalue['x'], thevalue['y'], thevalue['ry'], thevalue['rx'], angle, jpg, spiral))

#-180, 180, -180 is to the left,
#flip x and y, add 180, if over 180, minus 360
foth.close()
print("Saved %d marks from %d classifications (of which %d were empty) to %s-marks-*.csv." % (i_mark, len(classifications), i_empty, project_name))

#average data
print("Averageing data... If >15 classifications for the same image, they are thrown out")
infile        = path+"/"+project_name+"-clean.csv"
classifications= pd.read_csv(infile)

w = 9 #width, how many values we need to keep track of id, x, y, rx, ry, angle, jpg, count, spiral
d = 15 #depth, how many duplicates of each picture we have YOU MAY NEED TO CHANGE THIS
n = 25 #number of classifications in this set, it's usually 1000

classes = 0 #how many images we found
data = []
#angles = [[0] * d] * n
op = path+"/"+project_name+"-averaged.csv"
foth = open(op, "w")
# write the header line for each of the files
foth.write("classification_id,x,y,rx,ry,angle,filename, spiral percentage\n")

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
    spiral = cl[7]
    
    # the image which was classified
    #print ("from document = " + str(subject_id))
    
    # check if this id is new, or saved
    for list in data:
        if (classes > 0)and(list[0] == subject_id):
            same = True
            if(list[7] < 15):
                list[7] += 1
                #print ("This one is already in data = " + str(list))
                #this value is already in here, so we can average it in and break the loop
                list[1] += x
                list[2] += y
                list[3] += rx
                list[4] += ry
                #list[5] += angle
                list[8] += spiral
                
                print(jpg+" current angle "+str(list[5]/(list[7]-1)) + " adding " + str(angle))
                if (((angle - (list[5]/(list[7]-1))) > 90) or ((angle - (list[5]/(list[7]-1))) < -90)):
                    a1 = abs(angle - (list[5]/(list[7]-1)))
                    a2 = abs(angle - 180 - (list[5]/(list[7]-1)))
                    print(a1)
                    print(a2)
                    if(a2<a1):
                        print("a2<a1 " + str(angle-180))
                        angle = angle - 180
                    else:
                        print("a2>a1 " + str(angle))
            
                list[5] += angle
                list[9].append(angle)
                list[10].append(rx)
            list[11].append(ry)
            
            
            else:
                print("over 15 classifications for " + jpg)
    break
        else:
            same = False

if (same == False):
    # we didn't find it, so we need to create a fresh entry
    classes += 1
        print ("was not found in data, so add new. " + jpg)
        data.append([subject_id,(x),(y),(rx),(ry),(angle),jpg , 1.0, (spiral), [angle],[rx],[ry]])


#go through list, make sure the count is right, and save to a file

for list in data:
    sum = 0
    weightsum = 0
    i = 0
    for i in range(0, int(list[7])):
        #print(list[10][i])
        #print(list[11][i])
        weight = 1 - list[11][i]/list[10][i]
        #print(weight)
        sum += weight * list[9][i]
        weightsum += weight
        i = 1 + i
    print(list[6] + " classifications "+str(list[7])+" angle "+ str(list[5]/list[7]) +" weight" + str(weightsum) + " sum " + str(sum) +" weightsum " + str(sum/weightsum))
    list[5] = (sum/weightsum)*list[7]

for list in data:
    if (list[7] < d):
        print ("ERROR: %s has a count of %i. Value saved anyway" % (list[6], list[7]))
    foth.write("%d, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n" % (list[0], list[1]/list[7], list[2]/list[7], list[3]/list[7], list[4]/list[7], list[5]/list[7], list[6], list[8]/list[7]))

if (classes != n):
    print ("ERROR: only %i different pictures found. Values saved anyway" % (classes))

foth.close()
print("Data averaged")


#make new pictures
print("Deprojecting images. Images with a spiral percentage below 67% are not used")
infile        = "%s-averaged.csv" % project_name
infile = path+"/"  + infile
classifications = pd.read_csv(infile)
dirname = path+"/" + 'rotated'
if(os.path.isdir(dirname)):
    print("rotated folder already exists")
    shutil.rmtree(dirname)
    os.mkdir(dirname)
else:
    os.mkdir(dirname)

for i, row in enumerate(classifications.iterrows()):
    cl = row[1]
    angle = cl['angle'] * -1
    ry = cl['ry']
    rx = cl['rx']
    spiral = cl[7]
    name =cl['filename']
    name = name[2:]
    name2 = path+"/" + name
    print(name2)
    
    if(spiral >= .67):
        myimage = pil.open(name2)
        img = rotate(myimage, angle, reshape=True)
        imsave("rotated.jpg",img)
        stretch = (rx/ry)
        h, w = img.shape[:2]
        
        #RX MUST BE BIGGER THAN RY OR THE PHOTO WILL LOOK LIKE A LONG HORIZONTAL LINE
        scaled_img = cv2.resize(img, None, fx=1, fy=stretch, interpolation = cv2.INTER_LINEAR) # scale image
        sh, sw = scaled_img.shape[:2] # get h, w of scaled image
        center_y = int(sh/2 - h/2)
        center_x = int(sw/2 - w/2)
        cropped = scaled_img[center_y:center_y+h, center_x:center_x+w]
        newname = "r_" + name
        imsave(os.path.join(dirname, newname),cropped)

print("Image processing complete")

slu = input("Please enter the name of the zooniverse project. '6839' for test, '4212' for the real project")
print("Logging in with Astrolab11")
Panoptes.connect(username='Astrolab11', password='Astroguest11!')
project = Project.find(slu)#slug=slu)
#upload data and new pictures
#create a new set
subject_set = SubjectSet()
subject_set.links.project = project
setname = input("Please enter subject set name you would like")
subject_set.display_name = setname
subject_set.save()

project.reload()

infile= path + "/Spirals_jpg.csv"

# Prepare metadata
subject_metadata = {}
classifications= pd.read_csv(infile)
new_subjects = []

print("uploading and linking images")

for i, row in enumerate(classifications.iterrows()):
    cl = row[1]
    jpg = cl['jpg']
    jpg = jpg[::-1]
    jpg = jpg[:24]
    jpg = jpg[::-1]
    jpg = path + "/rotated/r_" + jpg
    image = cl['Image']
    sdss = cl['SDSS information']
    leda = cl['LEDA information']
    ra = cl['RA']
    dec = cl['DEC']
    subject_metadata.update({jpg:{'image' : jpg[13:], 'link': image, 'SDSS': sdss, 'LEDA': leda, 'RA': ra, 'DEC': dec}})
#print(jpg)
#subject_metadata[jpg].update(image, sdss, leda, ra, dec)

#upload images
for filename, metadata in subject_metadata.items():
    print(filename)
    #print(metadata)
    subject = Subject()
    subject.links.project = project
    if((os.path.isfile(filename))):
        subject.add_location(filename)
        subject.metadata.update(metadata)
        subject.save()
        new_subjects.append(subject)

#link set to workflow
subject_set.add(new_subjects)
workflow = project.links.workflows[1]
workflow.add_subject_sets(subject_set)

print("done")

