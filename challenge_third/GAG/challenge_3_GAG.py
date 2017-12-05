from __future__ import division
from itertools import combinations
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import challenge_3_func_GAG as func
import imagehash
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
        
    sum_images = np.zeros((pxls,pxls + 1))

    print("--------------------------------------")
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video frame length: {}".format(length) )
    
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
    
    hash_string = func.difference_hash(sum_images,pxls)
    print (hash_string)
    results.append((image_id,hash_string.replace(" ","")))
    #print (sum_images)
    
    
    
######################### ANALYSE THE RESULT ###################################
           
print ("\n#################### RESULT ######################")
func.find_hamming_distances(results)
    


