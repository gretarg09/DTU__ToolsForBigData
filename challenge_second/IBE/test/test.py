from __future__ import division

import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time
import mmh3


def getHashLshAlgorithm(img):
    
    # Resize to 9x8 pixels
    img = cv2.resize(img,(9,8))

    # Compare adjacent values (x>y)
    img_compared = np.empty((8,8))
    for i,row in enumerate(img):
        for j,column in enumerate(row):
            if j + 1 == len(row):
                break
            else:
                img_compared[i][j] = row[j] > row[j+1]

    hash_string = ""
    for difference in img_compared:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        hash_string = hash_string +''.join(hex_string) + ' ' 
    return hash_string

# Run the program for the following images 
filenames = ['cat.png', 'cat_mod.png','cat_mod_more.png','cat_orange.png']

for name in filenames:
    print "The hash for the figure {}:".format(name)
    print getHashLshAlgorithm(cv2.imread(name, cv2.IMREAD_GRAYSCALE))


# Grayscale the image
#img_cat = cv2.imread('cat.png', cv2.IMREAD_GRAYSCALE)
#img_cat_mod = cv2.imread('cat_mod.png', cv2.IMREAD_GRAYSCALE)
#img_cat_mod_more = cv2.imread('cat_mod_more.png', cv2.IMREAD_GRAYSCALE)
#img_cat_orange = cv2.imread('cat_orange.png', cv2.IMREAD_GRAYSCALE)