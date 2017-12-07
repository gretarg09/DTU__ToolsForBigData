from __future__ import division

import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import challenge_3_func_GAG as func
from multiprocessing import Process, Pool 
import imagehash
import json
import time
import math
from PIL import Image
from collections import Counter
from collections import defaultdict
import os
import imageio



import sklearn.cluster as cluster
from sklearn import mixture
from sklearn.cluster import KMeans
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice


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


video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/videos"
#video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/more_than_twenty"
#video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/minor_videos"


###################### FUNCTIONS ###############################
def process_video (filepath):
    reader = imageio.get_reader(filepath)
    
    # Set variables
    length = len(reader)
    bedge_size = 250
    frames_lsh = []
    image_id = filepath.split("/")[-1].split(".")[0]
    
    
    #print("--------------------------------------")
    #print( "Video frame length: {}".format(length) )
    #print "File name: {} ".format(image_id)
    
    
    for counter, frame in enumerate(reader):
        
        if counter > (length / 2) - (bedge_size/2) and counter < (length/2) + (bedge_size/2):
                                    
            # Start analysing the frames
            
            frame = np.array(frame)
            
            #### CROP IMAGE ####
            # Here we crop the black frame from the images
            # There are two different cases, either a portreit image of a landscape image3
            
            height = np.size(frame, 0)
            width = np.size(frame, 1)
            
           # print("height : {}".format(height))
           # print("width : {}".format(width))
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        
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
            
            gray = gray[y_start:y_end, x_start:x_end]
            
        
        
            #### Histogram normalization ####
            
            #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # gray = clahe.apply(gray)
            gray = cv2.equalizeHist(gray)
            
            ##################################
            
            #gray = cv2.resize(gray,(pxls,pxls))
                    
            image_hash = str(imagehash.average_hash( Image.fromarray(gray), hash_size = 8))        
            frames_lsh.append(image_hash)
        
        
    #print(frames_lsh)
        
    
    # ------------------ FEATURE HASHING -----------------------------
    # initialize the feature hashing matrix
    N = 1000 # number of buckets
    
    
    feature_hash_vector = np.zeros(N)
    
    for hash_str in frames_lsh:
        h = hash(hash_str)
        feature_hash_vector[h % N] += 1
        
    
    return image_id, feature_hash_vector


########################### STARTING ###########################
print ("\n#################### STARTING ######################")
     

t1 = time.time()

#for file in filenames: 
filepaths =  [video_folder_path + "/" + file  for file in os.listdir(video_folder_path)]
    
p = Pool(8)
results = p.map(process_video,filepaths,chunksize=1)
p.close()



t2 = time.time()

print("Execution time - First part : {}".format(t2-t1))   
    
######################### ANALYSE THE RESULT ###################################
           
print ("\n#################### SIMILARITY ######################")
       

#func.find_hamming_distances(results)
#func.find_cosine_similarity(results)

######################### CALCULATE RAND INDEX ###################################

       
print ("\n#################### TESTING RESULT ######################")       
       
test_result = True      

n_clusters = 970

if test_result:        
       
    # make data ready for clustering algorithms

    data = []  
    video_names = []
    for img, res in results:
        data.append(res)
        video_names.append(img)

    print ("before calculating the clustering")
    
    
    print ("-------------------- Agglomeration ------------------------")
    
    
    agglomerative = cluster.AgglomerativeClustering(n_clusters= n_clusters, linkage="ward").fit(data)
    video_and_label_agglomerative = zip(agglomerative.labels_, video_names)
    
    clusters = defaultdict(set)
    
    for label, video in video_and_label_agglomerative:
        clusters[label].add(video)
        
    rand_index_result = func.rand_index(clusters.values())
    
    print(rand_index_result)
    
    
    print ("--------------------- SPECTRAL ------------------------")
    
    
    spectral = cluster.SpectralClustering(
                                n_clusters=n_clusters, eigen_solver='arpack',
                                affinity="nearest_neighbors").fit(data)

    
    video_and_label_spectral = zip(spectral.labels_, video_names)
    
    clusters = defaultdict(set)
    
    for label, video in video_and_label_spectral:
        clusters[label].add(video)
        
    rand_index_result = func.rand_index(clusters.values())
    
    print(rand_index_result)
    
    
    print ("-------------------- WARD --------------------")
           
    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(
                                data, n_neighbors=n_clusters, include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)


    ward = cluster.AgglomerativeClustering(
                                        n_clusters=n_clusters, linkage='ward',
                                        connectivity=connectivity).fit(data)
    
    video_and_label_ward = zip(ward.labels_, video_names)
    
    clusters = defaultdict(set)
    
    for label, video in video_and_label_ward:
        clusters[label].add(video)
        
    rand_index_result = func.rand_index(clusters.values())
    
    print(rand_index_result)
    
    
    print ("----------------- BIRCH --------------------")
    
    birch = cluster.Birch(n_clusters=n_clusters).fit(data)
    
    video_and_label_birch = zip(birch.labels_, video_names)
    
    clusters = defaultdict(set)
    
    for label, video in video_and_label_birch:
        clusters[label].add(video)
        
    rand_index_result = func.rand_index(clusters.values())
    
    print(rand_index_result)
    
    
    #for name, clusters in clusters_and_names:
    #    print name
        # print
        # print clusters
        # print
    #    print type(clusters),len(clusters)
    #    print "rand index: {}".format(rand_index(clusters))
    #    print

t3 = time.time()

print("Execution time : {}".format(t3-t2))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


