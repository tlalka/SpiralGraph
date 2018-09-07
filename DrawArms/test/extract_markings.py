import sys, os
import numpy as np
import pandas as pd
import json

#This program takes a "classifcations" file from the image scrapper, and cleans it into a human-reable document
#ready for the "average_markings script" to use


project_name = "spiral-graph"
infile        = "%s-classifications.csv" % project_name
workflow_id = 4343
workflow_version = 173.185
classifications_all = pd.read_csv(infile)

classifications_all['anno_json'] = [json.loads(q) for q in classifications_all['annotations']]
classifications_all['sub_data'] = [json.loads(q) for q in classifications_all['subject_data']]

classifications = classifications_all
foth = open("%s-clean.txt"  % project_name, "w")
i_empty = 0
i_mark = 0
for i, row in enumerate(classifications.iterrows()):
    # row[0] is the index, [1] is the classification info
    cl = row[1]
    # the image which was classified
    #print (subject_id)
    rev = cl['subject_data'][::-1]
    revjpg = rev[3:29]
    jpg = revjpg[::-1]
    print(jpg)
    foth.write("\"task\":" + jpg + "\n")
    

    # loop through annotations in this classification
    # (of which there can be arbitrarily many)
    for j, anno in enumerate(cl['anno_json']):
        for i_v, thevalue in enumerate(anno['value']):
            i_mark+=1
            foth.write("\"tool\":\n")
            for k, points in enumerate(thevalue['points']):
                #print(points)
                foth.write("\"x\":%d,\"y\":%d\n" % (points['x'], points['y']))
#foth.write(",\n")


foth.write("end")
foth.close()


print("Saved %d marks from %d classifications (of which %d were empty) to %s-marks-*.csv." % (i_mark, len(classifications), i_empty, project_name))


#
