This document contains a description of all directories in this folder and the use of their python scripts. Contact tlalka@live.unc.edu, 9195998860 for more details.

Draw Arms:
These scripts covert line data from step 2 of the zooniverse project into fits images of the galaxy’s arms. You can use GIMP or ds9 to view the images.
Run the python script “extract_markings.py” on your zooniverse classification file “spiral-graph-classifications.cvs” to create the “spiral-graph-clean.txt” file. It’s format is as following:

"task" : r_19CharacterFileName.jpeg
"tool":
"x": xcoordinate,”y”: ycoordinate
"x": xcoordinate,”y”: ycoordinate
…
"x": xcoordinate,”y”: ycoordinate
"task" : r_aDifferent19CharacterFileName.jpeg
"tool":
"x": xcoordinate,”y”: ycoordinate 
…
End

extract_markings.py may need to be changed if you change the project or if Zooniverse changes how it exports classifications.

“map.py” takes the “spiral-graph-clean.txt”, creates the FITS pictures, and puts them into a folder called “line” at the target directory. When you run map.py, it will ask for the name/path to a directory that holds all the deprojected images that match the images in your classification file. An example path may be “/Users/astrolab/Documents/Zooniverse/Auto/test/rotated”. 

The “test” folder contains an example of what you would expect to see from successfully running the code. The target directory given to the program is simply “test” or “/Users/astrolab/Documents/Zooniverse/DrawArms/test/test”.



Auto:
This script cleans the data from step 1 of the zooniverse project, averages the classifications, deprojects the galaxy images, uploads the images to the zooniverse project, and links them to the “draw arms” workflow. What that means is, after a set of 1000 images is done on step 1 (the drawing an ellipse part) of the zooniverse project, you can run this one script and it will automatically put those images onto step 2. 
When you run this script, it will ask for a the path to the original pictures folder. It will then ask for the file name for the classifications from zooniverse, and produce a “spiral-graph-clean.csv” file. It will then take that file and produce a “spiral-graph-averaged.csv” file. The angles are the normalized weighted average. Next, it will take that averaged file, and use it to deproject all the original images. They will be placed into a directory named “rotated”. If less than 67% of people said an image was a spiral galaxy, it will not be deprojected. It will then ask for which zooniverse project you would like to upload and link the images to. You can skip this step by putting in nothing. It uses the login (username='Astrolab11', password='Astroguest11!') to do this. It will also attempt to upload the metadata file “Spirals_jpg.csv” to zooniverse.
This script also has a “test” folder with sample data files and images that should exhibit it’s proper behavior.

GenerateColorGalaxies:
This script generates color jpg images of the SDSS survey. You probably don’t want to use this.

GenerateFITSGalaxies:
The “generate_decals.py” file takes a “SelectedSpirals.csv” file and downloads the FITS images for these galaxies. It gets imaged from the “DECAL” survey when possible and “SDSS” when not. It acquires the images from the http://legacysurvey.org and the metadata from http://skyserver.sdss.org. In addition to downloading the imaged and creating a metadata file called “Spirals_jpg.csv”, it processes the FITS images into jpg previews ready to upload to zooniverse. To process these images it checks that the pixels at (256,256),(341,341),(171,171),(171,341),(341,171) and (171,171) are not blank (this would mean the DECAL survey does not gave this galaxy and we need to use the SDSS survery). It then calculates the 5% percentile of darkest pixels, and the brightest pixel out of the nine pixels in the center of the image. It scales the image logarithmically ranging from this maximum and minimum and exports the jpeg in ds9. 

The folder 6000 contains all 6000 fits and jpg images. TO upload them to zooniverse, just drag a set of 1000 into the upload window, it will automatically upload only the jpegs for you.

JPGvsFITS_DECAL&SDSS compares the FITS images to the original JPEGs

JPG_DECALvsSDSS compares the JPEG DECAL images to the JPEG SDSS images

The “genrand” script generates a folder with 25 random galaxies out of the 6000. 

The “random25” folder contains 25 random galaxies out of the 6000

Unprocessed contains FITS images before we used our custom image adjustment and processing. The are just logarithmically scaled using the default values. 

ExtractEllipseData:
This file contains scripts for extracting the classification for the ellipse data and cleaning it. These functions are already in the “auto” code, so you probably don’t need this folder.

DeprojectEllipseData:
This file contains scripts for deprojecting the ellipse data. These functions are already in the “auto” code, so you probably don’t need this folder.

TutorialPictures:
This file contains the videos, pictures and gifs used in the tutorials of the zooniverse project. 

25test:
This file contains the process on the sample set of 25 galaxies we tested. “classes.csv” contains the data from Zooniverse. “randoms” both the old and the new deprojected pictures. “Rotated copy” inside “randoms” contains the images deprojected using the mean instead of the weighted average.



Troubleshoot:

generate_decals.py only gave me 6000 images and not 6222.
When run by default, it gets sets of 1000. Run python2.7 generate_decals.py -p 'SelectedSpirals.csv’ -s 222 -b 27 to get the last set (it will be called set 28)

“generate_decals.py” downloads FITS images, but doesn’t create jpg previews. Run “source activate iraf27” in your terminal and then try again.

“generate_decals.py” takes a very long time.
Plug in your ethernet cable. It will take a long time to download and process large sets. 

“map.py” fails to draw any arms. 
Make sure to run extract_markings.py to get the clean input file first. If extract_markings.py doesn’t work, zooniverse may have changed the output formate for their classifications. If you downloaded “all classifications” from zooniverse, make sure to delete old, outdated classifications, or classifications for the “draw ellipse” step. It’s best to download classifications only for the “draw arms” workflow. 

“map.py” gives arms that aren’t centered in the image.
Make sure you are giving it the directory to the rotated images, not the original ones. It needs the dimensions of each image to plot the arms properly.

“AutoRun.py” fails to run.
Make sure that the “clean” classification file looks right. If zooniverse changes how they export classifications, the program may fail to generate a corrected “spiral-graph-clean.csv”. If you downloaded “all classifications” from zooniverse, make sure to delete old, outdated classifications, or classifications for the “draw arms” step. It’s best to download classifications only for the “draw ellipse” workflow. 

“AutoRun.py” runs but fails to generate any rotated images.
Make sure that the “spiral percentage” column in the “clean” file is over 1. If any are negative, the program is failing to read the data for the “is this galaxy smooth or spiral?” Question correctly. It assumes that the smooth option starts with “Sm” and the spiral option starts with “St”. If you changed these options in the zooniverse site, make sure to change the code accordingly. 

“AutoRun.py” runs and generates images, but they don’t look right.
Check the “spiral-graph-averaged.csv” to see if the numbers are what you expected.

“AutoRun.py” fails to upload any images to the zooniverse site. 
Zooniverse may have changed their APIs. You can upload the images by hand by just dragging a group of 1000 into a new “subject set”. Don’t forget to upload the cvs file with the meta data.

If you are troubleshooting, it helps to attempt to run the code on the test folder/data I provided. You can’t then compare what’s different about your data that makes the program fail. 




