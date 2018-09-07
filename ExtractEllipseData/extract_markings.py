import sys, os
import numpy as np
import pandas as pd
import json


#This program takes a "classifcations" file from the image scrapper, and cleans it into a human-reable document
#ready for the "average_markings script" to use


project_name = "spiral-graph"

infile        = "%s-classifications.csv" % project_name

# MAKE SURE TO CHANGE THESE TO MATCH YOUR CSV FILE
workflow_id = 3828
workflow_version = 42.96

classifications_all = pd.read_csv(infile)

classifications_all['anno_json'] = [json.loads(q) for q in classifications_all['annotations']]
classifications_all['sub_data'] = [json.loads(q) for q in classifications_all['subject_data']]

# only use classifications from the workflow & version we care about
in_workflow = classifications_all.workflow_version == workflow_version

classifications = classifications_all[in_workflow]

foth = open("%s-clean.csv"  % project_name, "w")


# write the header line for each of the files
# each has the basic classification information + the mark information
# including sanity check stuff + stuff we may never need, like the tool number
# and the frame the user drew the mark on, respectively

# the other/interesting marker is an ellipse+tag: {(x, y), (rx, ry), angle, text}
foth.write("subject_id,x,y,rx,ry,angle, filename\n")


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
    jpg = cl['subject_data'][40:62]
    print(jpg)
    
    # for anonymous users the userid field is blank so reads as NaN
    # which will throw an error later
    if np.isnan(userid):
        userid = -1

    # loop through annotations in this classification
    # (of which there can be arbitrarily many)
    for j, anno in enumerate(cl['anno_json']):

        # first, if this classification is blank, just write the basic information
        if len(anno['value']) < 1:
            i_empty+=1
            femp.write("%d,%d,\"%s\",\"%s\",%d,%s\n" % (class_id, subject_id, created_at, username, userid, userip))
        else:
            # it's not empty, so let's collect other info
            # the marks themselves are in anno['value'], as a list
            
            for i_v, thevalue in enumerate(anno['value']):
                i_mark+=1

                # how we write to the file (and which file) depends on which tool
                # is being used
				
				#normalize values
                angle = thevalue['angle']
             
                if thevalue['rx'] > thevalue['ry']:
                    if angle >= 90:
                        angle -= 180

                    if angle < -90:
                        angle += 180

                    foth.write("%d,%.2f,%.2f,%.2f,%.2f,%.2f, %s\n" % (subject_id, thevalue['x'], thevalue['y'], thevalue['rx'], thevalue['ry'], angle, jpg))

                else:
                    angle += 90

                    if angle >= 90:
                        angle -= 180

                    if angle < -90:
                        angle += 180

                    foth.write("%d,%.2f,%.2f,%.2f,%.2f,%.2f, %s\n" % (subject_id, thevalue['x'], thevalue['y'], thevalue['ry'], thevalue['rx'], angle, jpg))
					#-180, 180, -180 is to the left,
					#flip x and y, add 180, if over 180, minus 360
					





foth.close()


print("Saved %d marks from %d classifications (of which %d were empty) to %s-marks-*.csv." % (i_mark, len(classifications), i_empty, project_name))


#
