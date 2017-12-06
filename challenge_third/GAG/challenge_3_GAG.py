from __future__ import division
from itertools import combinations
from sklearn.feature_extraction import FeatureHasher
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import challenge_3_func_GAG as func
import imagehash
import json
import time
import math
from PIL import Image
from collections import Counter





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
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/SLK2PRXGW3DZ.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4"]

filenames0 = [
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/6CY15JHMFHQ4.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/6NWTR5CP41WG.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/9H0UQ6RGPK51.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/9Y6TIK3P5MDO.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/MF34IWZEV0H1.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/PZGZKNTRVEUH.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/QB9RBNGHAR91.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SKGL1C7462UE.mp4",
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SM4TDHHC0FLL.mp4"
        #"/Users/GretarAtli/Dropbox/ToolsForBigData/ur3/3FVFA1DVA3NZ.mp4"
        ]


filenames1 = ["/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4",
             "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/96EC4QS20Z28.mp4"] 

filenames2 = ["/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4"]

filenames3 = [ "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SKGL1C7462UE.mp4",
              "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/SM4TDHHC0FLL.mp4"]

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



def hashing_vectorizer(feature, N):
    x = np.zeros(N)
    h = hash(feature)
    x[h % N] += 1
    
    return x



pxls = 8

# Result is a key value pair (image id, resulting hash hex value)
results = []

for file in filenames2:
    cap = cv2.VideoCapture(file)
        
    sum_images = np.zeros((pxls,pxls))

    print("--------------------------------------")
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video frame length: {}".format(length) )
    
    image_id = file.split("/")[-1].split(".")[0]
    print "File name: {} ".format(image_id)
    
    counter = -1
    frames_lsh = []
    
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read(1)
        
        # increase counter
        counter = counter + 1
        
        if ret:
            
            if counter % 10 == 0:
                                
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
               # gray = clahe.apply(gray)
                gray = cv2.equalizeHist(gray)
                
                ##################################
                
                #gray = cv2.resize(gray,(pxls,pxls))
                
                
                # average hashing (aHash)
                # perception hashing (pHash)
                # difference hashing (dHash)
                # wavelet hashing (wHash)
                    
                #frames_lsh.append(str(imagehash.average_hash( Image.fromarray(gray), hash_size = 8)))
                
                image_hash = str(imagehash.average_hash( Image.fromarray(gray), hash_size = 8))
                
                #image_hash = str(imagehash.( Image.fromarray(frame), hash_size = 8))
                
                frames_lsh.append(image_hash)
        
        else:
            break
        
        
        
    #sec   
    #print ("len : {}".format(len (frames_lsh) ))
    #for i in frames_lsh:
     #   print(i)
        
    #frames_lsh_counted = Counter(frames_lsh)
    
     
    #for key,value in sorted(frames_lsh_counted.items(), key = lambda x:x[1], reverse = True):
    #    print(key, value)
            
        
    
    
    #print ("############## Set #################")
    #print ("len : {}".format(len (set(frames_lsh)) ))
    #for i in set(frames_lsh) :
    #    print(i)
        
    #frames_lsh = list(set(frames_lsh))
           
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    

    #------------------ FEATURE HASHING -----------------------------
    # initialize the feature hashing matrix
    N = 8 # number of buckets
    feature_hashing_matrix = np.zeros((len(frames_lsh), N))
    
    # create the feature hashing matrix
    for i,_ in enumerate(feature_hashing_matrix):
        feature_hashing_matrix[i] = hashing_vectorizer(frames_lsh[i],N)


    print feature_hashing_matrix
    print result_vector

    result_vector = feature_hashing_matrix.sum(axis=0)
    results.append((image_id,result_vector))
    
    
    
######################### ANALYSE THE RESULT ###################################
           
print ("\n#################### RESULT ######################")
#func.find_hamming_distances(results)
func.find_cosine_similarity(results)


