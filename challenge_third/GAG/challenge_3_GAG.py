from __future__ import division
from itertools import combinations
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time
import math



filenames = [
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/76KUS3QCGVCY.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/96EC4QS20Z28.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/CL8W7L333U90.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/FDAZ5NL5NFL2.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/HBX8QLI9HH25.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/JY2ZAINWD2RX.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/LP47ZGJ256YU.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/NTETO8P77N96.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/SLK2PRXGW3DZ.mp4"]

#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/96EC4QS20Z28.mp4"] 

#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4"]

#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/76KUS3QCGVCY.mp4"]

# ur 2
#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SKGL1C7462UE.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SM4TDHHC0FLL.mp4"] 

# ur 3
#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/ur3/3FVFA1DVA3NZ.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/ur3/DD3C5S0MBKXB.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/ur3/LS2RXLT409EG.mp4",
#             "/Users/GretarAtli/Dropbox/ToolsForBigData/ur3/SPV675U9WWK7.mp4"]


pxls = 8

# Result is a key value pair (image id, resulting hash hex value)
results = []

for file in filenames:
    cap = cv2.VideoCapture(file)
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video frame length: {}".format(length) )
    
    
    sum_images = np.zeros((pxls,pxls + 1))

    print("--------------------------------------")
    image_id = file.split("/")[-1].split(".")[0]
    print "File name: {} ".format(image_id)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read(1)
        
        if ret:
            # Start analysing the frames
            
            #### CROP IMAGE ####
            # Here we crop the black frame from the images
            # There are two different cases, either a portreit image of a landscape image
            
            crop = True
            
            if crop:
                height = np.size(frame, 0)
                width = np.size(frame, 1)
                
                #print("height : {}".format(height))
                #print("width : {}".format(width))
                
                
                if height > width: # if portrait image
                    x = 256
                    y = 454                
                else: # else it is a landscape 
                    x = 454
                    y = 256
            
                x_start = int(width/2 - x/2)
                x_end = int(width/2 + x/2)
                y_start = int(height/2 - y/2)
                y_end = int(height/2 + y/2)
                
                #print("x start : {}".format(x_start))
                #print("x end : {}".format(x_end))
                #print("y start : {}".format(y_start))
                #print("y end : {}".format(y_end))
    
                
                frame = frame[y_start:y_end, x_start:x_end]
            
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #### Histogram normalization ####
            
            #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            #gray = clahe.apply(gray)
            #gray = cv2.equalizeHist(gray)
            
            #cv2.imwrite('second.png',gray)
            
            gray = cv2.resize(gray,(pxls + 1,pxls))
            
            sum_images = gray + sum_images
            
            
        else:
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
    #print (sum_images)
    
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
    
    print hash_string
    #print int(hash_string.replace(" ", ""),16)
    results.append((image_id,hash_string.replace(" ","")))
    
######################### ANALYSE THE RESULT ###################################
           
print ("#################### RESULT ######################")
find_hamming_distances(results)
    
######################### FUNCTIONS TO CALCULATE THE DIFFERENCES ###################################3
    
    
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
    
    
    
    