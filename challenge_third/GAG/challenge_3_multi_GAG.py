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
from collections import defaultdict
import os
from multiprocessing import Process, Pool

import sklearn.cluster as cluster
#from sklearn import mixture
#from sklearn.cluster import KMeans
#from sklearn import cluster, datasets, mixture
#from sklearn.neighbors import kneighbors_graph
#from sklearn.preprocessing import StandardScaler





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


#video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/videos"
video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/more_than_twenty"
#video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/minor_videos"

###################### Functions #########################################

def process_video(filepath):
    
    # enable multithreading in OpenCV for child thread
   # cv2.setNumThreads(-1)
    
    print filepath
    
    cap = cv2.VideoCapture(filepath)
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    image_id = filepath.split("/")[-1].split(".")[0]
    
    print length
    
    counter = -1
    frames_lsh = []
    window_size = 250
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read(1)
        
        print frame
        
        # increase counter
        counter = counter + 1
    
        if ret:
            
            #if counter > (length / 2) - (window_size/2) and counter < (length/2) + (window_size/2):
                                
            # Start analysing the frames
            
            #### CROP IMAGE ####
            # Here we crop the black frame from the images
            # There are two different cases, either a portreit image of a landscape image

            height = np.size(frame, 0)
            width = np.size(frame, 1)
            
            if height > width: # if portrait image
                x = 250
                y = 450                
            else: # else it is a landscape 
                x = 450
                y = 250
        
            x_start = int(width/2 - x/2)
            x_end = int(width/2 + x/2)
            y_start = int(height/2 - y/2)
            y_end = int(height/2 + y/2)
            
            frame = frame[y_start:y_end, x_start:x_end]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #### Histogram normalization ####
            
            #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
           # gray = clahe.apply(gray)
            gray = cv2.equalizeHist(gray)
            
            image_hash = str(imagehash.average_hash( Image.fromarray(gray), hash_size = 8))                
            frames_lsh.append(image_hash)
        
        else:
            break
       
    
    print frames_lsh
    
    # When video has been processed then release the capture
    cap.release()
    #cv2.destroyAllWindows()


    # ------------------ FEATURE HASHING -----------------------------
    # initialize the feature hashing matrix
    N = 1000 # number of buckets
    
    
    feature_hash_vector = np.zeros(N)

    for hash_str in frames_lsh:
        h = hash(hash_str)
        feature_hash_vector[h % N] += 1

    
    return (image_id,feature_hash_vector)


def dummy_func(filepath):
    print filepath
    


if __name__ == "__main__":
    t1 = time.time()
    
    #for file in filenames0:
    #filepaths = [video_folder_path + "/" + file for file in os.listdir(video_folder_path)]  
      
     # disable multithreading in OpenCV for main thread to avoid problems after fork
    #cv2.setNumThreads(0)
    
    # start multiprocessing
    p = Pool(1)
    results = p.map(process_video, filenames2, chunksize=1)

#print results
    
    
# ------------------------ TESTING -------------------------------
    


#t2 = time.time()
#
#print("Execution time - First part : {}".format(t2-t1))   
#    
########################## ANALYSE THE RESULT ###################################
#           
#print ("\n#################### SIMILARITY ######################")
#       
#
##func.find_hamming_distances(results)
##func.find_cosine_similarity(results)
#
########################## CALCULATE RAND INDEX ###################################
#
#       
#print ("\n#################### TESTING RESULT ######################")       
#       
#test_result = True       
#      
#if test_result:        
#       
#    # make data ready for clustering algorithms
#
#    data = []  
#    video_names = []
#    for img, res in results:
#        data.append(res)
#        video_names.append(img)
#
#    print ("before calculating the clustering")
#    
#    agglomerative = cluster.AgglomerativeClustering(n_clusters= 21 , linkage="ward").fit(data)
#    video_and_label = zip(agglomerative.labels_, video_names)
#    
#    clusters = defaultdict(set)
#    
#    for label, video in video_and_label:
#        clusters[label].add(video)
#        
#    rand_index_result = func.rand_index(clusters.values())
#    
#    print(rand_index_result)
    
    #for name, clusters in clusters_and_names:
    #    print name
        # print
        # print clusters
        # print
    #    print type(clusters),len(clusters)
    #    print "rand index: {}".format(rand_index(clusters))
    #    print




