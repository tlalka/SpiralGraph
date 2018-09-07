#legacy survey
#http://legacysurvey.org//viewer/jpeg-cutout?ra=191.6403&dec=-1.7062&zoom=14&layer=decals-dr5
"http://legacysurvey.org//viewer/jpeg-cutout?ra=" "&dec=" "&zoom=14&layer=decals-dr5"
#rounding and such not needed
#images return black if not there, name is "blank"
#http://legacysurvey.org/viewer/data-for-radec/?ra=162.6421&dec=48.6932&layer=mzls+bass-dr6
#http://legacysurvey.org/viewer/jpeg-cutout?ra=154.7709&dec=46.4537&layer=mzls+bass-dr6&pixscale=0.3&bands=grz
#"http://legacysurvey.org/viewer/fits-cutout?ra="+ra+"&dec="+dec+"&layer=mzls+decals-dr5&pixscale=0.454&bands=g"


"""
Zooniverse.org requires data sets to be no larger than 1000 images. This file creates jpg images from the SDSS ID, and
concurrently the RA and DEC of each Spiral Galaxy in a .csv input file: SelectedSpirals.csv. It then creates a subset
folder to contain the jpg images and a separate .csv file for each subset of default 1000 images. Set size can be
 imputed to any value.

This file can be run using a terminal with the following arguments:
    -p or --path_to_csv: provide a string path to the location of a csv file to parse.
                        This will throw an error if the path does not exist.
    -s or --set_size: integer value of how many spiral galaxy jpg images each folder will hold. Default=1000
    -b or --start_set: integer value that will start the generation of images at a certain folder.
    -e or --end_set: integer value that will end generation of jpg files at a certain file
                        Has to be smaller then start_set if given, and will end at the start of given folder number
    -n or --name: string value that is the name of each folder/set
    -v or --verbose: Prints debug messages and links to every jpg found.

    Examples:

        python2.7 generate_decals.py -p 'SelectedSpirals.csv'

        python2.7 generate_jpgs_and_csv.py -p 'SelectedSpirals.csv' -s 50
        
        python2.7 generate_jpgs_and_csv.py -p 'SelectedSpirals.csv' -b 7 -v
        
        python2.7 generate_decals.py -p 'SelectedSpirals.csv' -s 100 -b 20 -e 21
        
        python2.7 generate_jpgs_and_csv.py -p 'SelectedSpirals.csv' -s 5 -b 1 -e 2 --verbose

    Helpful Note:
        The most common error is an IOError: socket error.
        This means the connection was lost while getting jpg images online.
        Simply run the program starting at the folder it was loading with -b #, and the same set size to continue.

"""

# imports
import numpy as np
import csv
import urllib
import os
import argparse
from astropy.io import fits
import re
import sys
import ast
from PIL import Image

# metadata
__author__ = 'Tessa D. Wilkinson <tessadwilkinson@gmail.com>'
__description__ = 'Uses a csv data file to generate folders of jpg images sets, each with its own csv data file.'
__maintainer__ = 'Museum of Natural Science: Astronomy and Astrophysics Research Lab'
__date__ = '05/26/2017'


def separate_lists_by_sets(parallel_lists, set_size):
    """
    Auxillary function to parse input .csv file into set_size chunks

    :param parallel_lists: A zipped list of lists consisting of image ids, ra's, and dec's to parse
    :type parallel_lists: list
    :param set_size: Determines how large to make each folder of out images.
    :type set_size: int
    :return: List of lists; each inner list will be up to the set_size value
    """

    outerlist = []
    sublist = []
    for item in parallel_lists:
        sublist.append(item)
        if len(sublist) >= set_size:
            outerlist.append(sublist)
            sublist = []

    return outerlist


def generate_jpgs_and_csv(path_to_csv, set_size=1000, start_set=None, end_set=None, subject_set_name='SubjectSet',
                          verbose=False):
    """

    This definition creates a folder of subsets to be loaded to Zooniverse.org
    - Each Subset folder has:
        - A set of jpg files that is defined by the set_size, start_set, and end_set variables
        - A .csv file containing a iterative number, jpg file name, and url for each jpg file


    :param path_to_csv: Pointer to csv data sheet with spiral galaxy image id, ra, and dec in that order
    :type path_to_csv: str
    :param set_size: Determines how many images go into each separated folder
    :type set_size: int
    :param start_set: Determines a start point for jpg generation, and is dependent on set_size.
    :type start_set: int
    :param end_set: Determines an end point for jpg generation, and is dependent on set_size. Cannot be smaller than
                    start_set, if given.
    :type end_set: int
    :param subject_set_name: The name of the subject set that will also be each folder name
    :type subject_set_name: str
    :param verbose: Allows for debug printing statements and links for each jpg generated.
    :type verbose: bool
    :return: A folder containing the set_size number of jpg files and a csv file. (set_size + 1 items)
    :return: The returned csv file for each folder provides the data stored for each image: the subject id, jpg file
            location, the spiral galaxy jpg image http link, the SDSS information link, and the LEDA information link

    """

    # raise an error if csv file is not in path
    if not os.path.exists(path_to_csv):
        raise AttributeError("{} doesn't exist!".format(path_to_csv))

    # import csv file to obtain variable columns as lists, REQUIRES FIRST THREE COLUMNS IN THIS ORDER!
    image_id_list, ra_list, dec_list = np.loadtxt(path_to_csv, usecols=(0, 1, 2), skiprows=1, delimiter=',', dtype=str,
                                                  unpack=True)

    # This creates a separate folder and .csv for each 1000 images
    spiral_multilist = separate_lists_by_sets(zip(image_id_list, ra_list, dec_list), set_size)

    print('Possible total of {} sets with set size of {}.'.format(len(spiral_multilist), set_size))

    # Throw an error if start set is above possible number rof sets
    assert start_set < len(
        spiral_multilist), 'Variable start_set: {} is above possible number of sets: {}. Adjust start_set or set_size.'.format(
        start_set, len(spiral_multilist))

    # start or end at a given number. -1's is to offset zero based enumeration
    if start_set and not end_set:
        spiral_multilist = spiral_multilist[start_set - 1:]

    elif end_set and not start_set:
        spiral_multilist = spiral_multilist[:end_set - 1]

    elif start_set and end_set:
        # Throw an error to void start_set == end_set because it would give no results
        assert start_set < end_set, 'Variable start_set: {} must be less than variable end_set: {}'.format(start_set,
                                                                                                           end_set)
        spiral_multilist = spiral_multilist[start_set - 1:end_set - 1]

    # Iterate through each list of sets and save into a file
    folder_num = 0
    for number_list, group in enumerate(spiral_multilist):

        # creating a .csv file to store jpg information
        if start_set:
            folder = '{}_{}/'.format(subject_set_name, start_set + folder_num)
            folder_num += 1
        else:
            folder = '{}_{}/'.format(subject_set_name, number_list + 1)

        # if folder doesn't exist, create a new one subject set
        if not os.path.exists(folder):
            os.makedirs(folder)

        if verbose:
            print('Filling {}...'.format(folder))
            print('\n') * 5

        # write a .csv file to input into Zooniverse with jpg files
        outfile = open(folder + 'Spirals_jpg.csv', 'w+')
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(['subject id', 'jpg', 'Image', 'SDSS information', 'LEDA information', 'RA', 'DEC'])

        # obtain identifiers from csv column lists
        for n, (image_id, ra, dec) in enumerate(group):

            if verbose:
                print('Initializing jpeg download _____________ # {}'.format(n))
                print ('image_id = ')
                print image_id

            # Step 1: web scrapping to obtain Ra and Dec

            # need to use the url that doesn't have any menus
            info_url = 'http://skyserver.sdss.org/dr7/en/tools/explore/summary.asp?id=' + str(
                image_id) + "&spec=0x01c2cac422c00000"
            temp_file = urllib.urlopen(info_url)
            
            if verbose:
                print 'info_url = '
                print info_url
            # print(temp_file.readlines())

            # parse through lines of html to get to sdss j number and ra and dec

            html_context = [context for context in temp_file.readlines()]
            
            if verbose:
                print 'html_context = '
                print html_context
            
            
            # get sdss J number
            j = html_context[21].find('J')
            plus = html_context[21].find('+')
            end = html_context[21].find(' </font')
            num1 = html_context[21][j + 1: plus]
            num2 = html_context[21][plus + 1:end]
            # get ra and dec
            ra_index = html_context[22].find('ra=')
            comma1 = html_context[22].find(', d')
            dec_index = html_context[22].find('dec=')
            comma2 = html_context[22].find(',&')
            ra_degree = html_context[22][ra_index + 3:comma1]
            dec_degree = html_context[22][dec_index + 4:comma2]

            # Step 2: use ra and dec to access image url for downloading the jpeg

            if verbose:
                print('_Obtaining image for galaxy at ra={} and dec={}.'.format(ra_degree, dec_degree))
            url = 'http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra=' + str(ra_degree) + '&dec=' + str(
                dec_degree) + '&scale=0.19806&width=512&height=512&opt=&query='

            leda_url = 'http://leda.univ-lyon1.fr/ledacat.cgi?sdss%20j' + num1 + '%2B' + num2 + '&ob=ra'

            # Step 3: Make a jpg file
            if verbose:
                print(url)
                print(info_url)
                print(leda_url)
                print('__Saving jpeg image: {}.jpg'.format(image_id))
            jpg = urllib.urlretrieve(url, folder + str(image_id) + ".jpg")

            # write the jpg information into the csv file
            writer.writerow([n, jpg[0], url, info_url, leda_url, ra_degree, dec_degree])

            # download DECAL image
            url = "http://legacysurvey.org/viewer/jpeg-cutout?ra="+str(ra_degree)+"&dec="+str(dec_degree)+"&size=512&layer=decals-dr5&pixscale=0.227&bands=grz"
            image_file = folder + str(image_id) + "B.jpeg"
            jpg = urllib.urlretrieve(url, image_file)

        # close the file per set
        outfile.close()
        
        # to tell what files are being printed
        print('Set {} of {} saved to {}.'.format(number_list + 1, len(spiral_multilist), folder[:-1]))

    if verbose:
        print('Obtaining jpeg files complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # expect a path argument atleast
    parser.add_argument("-p", "--path_to_csv", type=str, default='', required=True)
    parser.add_argument("-s", "--set_size", type=int, default=1000, required=False)
    parser.add_argument("-b", "--start_set", type=int, default=None, required=False)
    parser.add_argument("-e", "--end_set", type=int, default=None, required=False)
    parser.add_argument("-n", "--name", type=str, default='SubjectSet', required=False)
    parser.add_argument("-v", "--verbose", action='store_true', required=False)

    args = parser.parse_args()

    generate_jpgs_and_csv(path_to_csv=args.path_to_csv, set_size=args.set_size, start_set=args.start_set,
                          end_set=args.end_set, subject_set_name=args.name, verbose=args.verbose)
