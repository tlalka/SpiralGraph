import sys, os
import numpy as np
import pandas as pd
import json


#This program takes a "data" file, and cleans it into the infomration we are concened with



infile        = "data.csv" 

classifications = pd.read_csv(infile)

foth = open("clean.csv", "w")


# write the header line for each of the files
# each has the basic classification information + the mark information
# including sanity check stuff + stuff we may never need, like the tool number
# and the frame the user drew the mark on, respectively

# the other/interesting marker is an ellipse+tag: {(x, y), (rx, ry), angle, text}
foth.write("RA, DA, classifications, disk, faceon, spiral, spiral_weighted, bulge_1, bulge_2, bulge_3, bulge_4, arms_tight, arms_medium, arms_loose, arms_1, arms_2, arms_3, arms_4, arms_5, arms_6, irregular \n")


i = 0

for i, row in enumerate(classifications.iterrows()):
    # row[0] is the index, [1] is the classification info
    cl = row[1]
    
    ra  = 0.0 + cl['ra']
    dec = 0.0 + cl['dec']
    votes = 0.0 + cl['total_classifications']
    disk   = 0.0 + cl['t01_smooth_or_features_a02_features_or_disk_weighted_fraction']
    faceon   = 0.0 + cl['t02_edgeon_a05_no_weighted_fraction']
    spiral   = 0.0 + cl['t04_spiral_a08_spiral_weighted_fraction']
    spiral_W = disk * faceon * spiral 
    bulge_1   = 0.0 + cl['t05_bulge_prominence_a10_no_bulge_weighted_fraction']
    bulge_2   = 0.0 + cl['t05_bulge_prominence_a11_just_noticeable_weighted_fraction']
    bulge_3   = 0.0 + cl['t05_bulge_prominence_a12_obvious_weighted_fraction']
    bulge_4   = 0.0 + cl['t05_bulge_prominence_a13_dominant_weighted_fraction']
    arms_tight   = 0.0 + cl['t10_arms_winding_a28_tight_weighted_fraction']
    arms_medium   = 0.0 + cl['t10_arms_winding_a29_medium_weighted_fraction']
    arms_loose    = 0.0 + cl['t10_arms_winding_a30_loose_weighted_fraction']
    arms_1 = 0.0 + cl['t11_arms_number_a31_1_weighted_fraction']
    arms_2 = 0.0 + cl['t11_arms_number_a32_2_weighted_fraction']
    arms_3 = 0.0 + cl['t11_arms_number_a33_3_weighted_fraction']
    arms_4 = 0.0 + cl['t11_arms_number_a34_4_weighted_fraction']
    arms_5   = 0.0 + cl['t11_arms_number_a36_more_than_4_weighted_fraction']
    arms_6     = 0.0 + cl['t11_arms_number_a37_cant_tell_weighted_fraction']
    irregular     = 0.0 + cl['t08_odd_feature_a22_irregular_weighted_fraction']
    

    # the image which was classified
    #print (subject_id)
    #print("%f" % faceon)
    
    if(spiral_W > .67 and (1-irregular) > .67 and not (bulge_1+bulge_2 > .67 and arms_tight > .67) and not (bulge_4 > .67 and arms_loose > .67)):
        foth.write("%f, %f, %d, %f %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" % (ra, dec, votes, disk, faceon, spiral, spiral_W, bulge_1, bulge_2, bulge_3, bulge_4, arms_tight, arms_medium, arms_loose, arms_1, arms_2, arms_3, arms_4, arms_5, arms_6, irregular))
        #print(i)
        i = i+1



foth.close()


print("Saved %d marks from %d classifications to clean.csv." % (i, len(classifications)))


#
