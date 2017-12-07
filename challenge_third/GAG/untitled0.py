# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 13:52:12 2017

@author: helga
"""

from __future__ import division
from itertools import combinations
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
from scipy import spatial


######################### FUNCTIONS TO CALCULATE THE DIFFERENCES ###################################3
    
# This function takes in a list of key value pairs (image key,  feature vectore) and 
# Finds all combinations of the pairs and then calculated the number of different bits between two hash strings
# It returns a sorted list, sorted in reverse order so the pairs with the highest difference are on the top of the list
def find_cosine_similarity(tuple_pair_array):
    similarities = []

    # find all combinations
    for i in combinations(tuple_pair_array, 2):
                
        similarity =  1 - spatial.distance.cosine(i[0][1], i[1][1])
        similarities.append((i[0],i[1],similarity))

    similarities = sorted(similarities, key =  lambda x:x[2], reverse=False)

    for similarity_pair in similarities:
        output = "{}|{} -  similarity = {}".format(
            similarity_pair[0][0],
            similarity_pair[1][0],
            #similarity_pair[0][1],
            #similarity_pair[1][1],
            similarity_pair[2]
        )

        print output    




# This function takes in a list of key value pairs (image key, hex value string) and 
# Finds all combinations of the pairs and then calculated the number of different bits between two hash strings
# It returns a sorted list, sorted in reverse order so the pairs with the highest difference are on the top of the list
def find_hamming_distances(tuple_pair_array):
    distances = []

    # find all combinations
    for i in combinations(tuple_pair_array, 2):
        distance =  get_hamming_distance(i[0][1],i[1][1])
        distances.append((i[0],i[1],distance))

    distances = sorted(distances, key =  lambda x:x[2], reverse=True)

    for distance_pair in distances:
        output = "{}|{} - {}|{} - {}".format(
            distance_pair[0][0],
            distance_pair[1][0],
            distance_pair[0][1],
            distance_pair[1][1],
            distance_pair[2]
        )

        print output

# Functions that finds number of different bits between two hash strings  
def get_hamming_distance(hash_string1, hash_string2):
    """Get the number of different bits between two hash strings."""
    dist = 0
    # get diff matrices from hash string
    bits1 = hash_to_bits(hash_string1)
    bits2 = hash_to_bits(hash_string2)

    # compute distance
    for bit1, bit2 in zip(bits1, bits2):
        if bit1 != bit2:
            dist += 1
    return dist

def hash_to_bits(hash_string):
    """Convert a hash string into the corresponding bit string."""
    bits = []
    # Convert into individual hex numbers
    hex_nums = ['0x' + hash_string[i:i+2] for i in range(0, len(hash_string), 2)]
    for hex_num in hex_nums:
        bit_string = bin(int(hex_num, 16))[2:].rjust(8, '0') # binary string
        bits.append(bit_string)
    return "".join(bits) # return as one string
    
    
######################## HASHING ALGORITHMS ##############################

def difference_hash(sum_images,pxls):
    
    img_compared = np.empty((pxls,pxls))
    for i,row in enumerate(sum_images):
        for j,column in enumerate(row):
            if j + 1 == len(row):
                break
            else:
                img_compared[i][j] = row[j] > row[j+1]
    
   # print "The full matrix"
   #print img_compared
    
    hash_string = ""
    for difference in img_compared:
        #print "each line:"
        #print difference 
        decimal_value = 0
        hex_string = []  
        for index, value in enumerate(difference):
            if value: 
                decimal_value += 2**(index % pxls)
            if (index % pxls) == pxls-1:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value  = 0
        hash_string = hash_string +''.join(hex_string) + ' '
    
    return hash_string
    