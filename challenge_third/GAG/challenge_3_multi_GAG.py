from __future__ import division

import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import challenge_3_func_GAG as func
import adjusted_rand_index as rand_index_validation
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


###################### FUNCTIONS ###############################
# Function that takes in a file pathm pre processes the frames of the video and then calculates 
# a local sensitive hashing for each frame, resulting in a list of LSH values. 
# The lsh values list/vector is then feature hashed into a vector of size N.
# The function returns the resulting feature hash vector as well as the imageid

def process_video (filepath):
    reader = imageio.get_reader(filepath)
    
    # Set variables
    length = len(reader)
    bedge_size = 350
    frames_lsh = []
    
    # Get image id
    image_id = filepath.split("/")[-1].split(".")[0]
    

    
    for counter, frame in enumerate(reader):
        
        if counter > (length / 2) - (bedge_size/2) and counter < (length/2) + (bedge_size/2):
                                    
            # Start analysing the frames
            
            frame = np.array(frame)
            
            #------------------------- CROP IMAGE ----------------------------------#
            # Here we crop the black frame from the images
            # There are two different cases, either a portrait image of a landscape image3
            
            height = np.size(frame, 0)
            width = np.size(frame, 1)
                        
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
            
        
        
            #------------------ Histogram normalization ------------------------------#
            
            gray = cv2.equalizeHist(gray)
            
            #---------------------- LOCALITY SENSITIVE HASHING ----------------------------------#
                    
            image_hash = str(imagehash.average_hash( Image.fromarray(gray), hash_size = 4))        
            frames_lsh.append(image_hash)
        
    
    # ------------------ FEATURE HASHING -----------------------------
    # initialize the feature hashing matrix
    N = 600 # number of buckets
    
    # Create the feature hashing vector
    feature_hash_vector = np.zeros(N)
    
    for hash_str in frames_lsh:
        h = hash(hash_str)
        feature_hash_vector[h % N] += 1
        
    
    return image_id, feature_hash_vector

print ("\n-------------------- STARTING -----------------------")
     
video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/videos"

t1 = time.time()

#for file in filenames: 
filepaths =  [video_folder_path + "/" + file  for file in os.listdir(video_folder_path)]
    
# Use the mutliprocessing to process each video
p = Pool(8)
results = p.map(process_video,filepaths,chunksize=1)
p.close()


t2 = time.time()

print("Execution time - First part : {}".format(t2-t1))   
    
######################### ANALYSE THE RESULT ###################################
           

       
print ("\n-------------------- TESTING RESULT --------------------------")       
       
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
    
        
    run_agglomerative = False
    if run_agglomerative:
        
        print ("-------------------- Agglomeration ------------------------")
    
        agglomerative = cluster.AgglomerativeClustering(n_clusters= n_clusters, linkage="ward").fit(data)
        video_and_label_agglomerative = zip(agglomerative.labels_, video_names)
        
        clusters = defaultdict(set)
        
        for label, video in video_and_label_agglomerative:
            clusters[label].add(video)
            
        rand_index_result = rand_index_validation.rand_index(clusters.values())
        
        print(rand_index_result)
    

    run_spectral = True
    if run_spectral:    
        print ("--------------------- SPECTRAL ------------------------")
        
        spectral = cluster.SpectralClustering(
                                    n_clusters=n_clusters, n_init = 20, eigen_solver='arpack',
                                    affinity="nearest_neighbors", assign_labels = 'discretize').fit(data)
    
        
        video_and_label_spectral = zip(spectral.labels_, video_names)
        
        clusters = defaultdict(set)
        
        for label, video in video_and_label_spectral:
            clusters[label].add(video)
            
        t3 = time.time()
        print("Execution time before validation: {}".format(t3-t1))     

        rand_index_result = rand_index_validation.rand_index(clusters.values())
        
        print(rand_index_result)
    
    
    
    run_ward = False
    if run_ward:
        print ("-------------------- WARD --------------------")
       
        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(data, n_neighbors=n_clusters, include_self=False)
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)
    
    
        ward = cluster.AgglomerativeClustering(
                                            n_clusters=n_clusters, linkage='ward',
                                            connectivity=connectivity).fit(data)
        
        video_and_label_ward = zip(ward.labels_, video_names)
        
        clusters = defaultdict(set)
        
        for label, video in video_and_label_ward:
            clusters[label].add(video)
            
        rand_index_result = rand_index_validation.rand_index(clusters.values())
    
        print(rand_index_result)
    
    run_brich = False
    if run_brich:
        print ("----------------- BIRCH --------------------")
    
        birch = cluster.Birch(n_clusters=n_clusters).fit(data)
        video_and_label_birch = zip(birch.labels_, video_names)
        
        clusters = defaultdict(set)
        
        for label, video in video_and_label_birch:
            clusters[label].add(video)
            
        rand_index_result = rand_index_validation.rand_index(clusters.values())
        
        print(rand_index_result)
    
    
    #for name, clusters in clusters_and_names:
    #    print name
        # print
        # print clusters
        # print
    #    print type(clusters),len(clusters)
    #    print "rand index: {}".format(rand_index(clusters))
    #    print

t4 = time.time()

print("Execution time : {}".format(t4-t1))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


