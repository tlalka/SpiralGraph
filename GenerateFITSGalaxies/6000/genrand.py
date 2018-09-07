import os
from shutil import copyfile
import random
import csv

list = []
s = 0
d = 0
for root, dirs, filz in os.walk('/Users/astrolab/Documents/Zooniverse/GenerateFITSGalaxies/6000'):
    for dir in dirs:
        for root2, dirs2, filz2 in os.walk('/Users/astrolab/Documents/Zooniverse/GenerateFITSGalaxies/6000/'+dir):
            for file in filz2:
                if(file[20:] == 'jpeg'):
                 list.append(dir+'/'+file)
                 if(file[18:19] == 'S'):
                 #print("S")
                    s = s + 1
                 else:
                    d = d + 1
#print("D")

#print(list)
print("d to s ratio: " + str(100*(d/(d+s))))
name = '/Users/astrolab/Documents/Zooniverse/GenerateFITSGalaxies/randoms'
os.mkdir(name)
outfile = open(name + '/Spirals_jpg.csv', 'w+')
writer = csv.writer(outfile, delimiter=',')
writer.writerow(['subject id', 'jpg', 'Image', 'SDSS information', 'LEDA information', 'RA', 'DEC'])
for i in range(0, 25):
    upper = len(list)
    ran = random.randrange(0, upper)
    file = list[ran]
    copyfile(file, name+'/'+file[13:])
    writer.writerow([i, file, "", "", "", "", ""])
#print(file)

