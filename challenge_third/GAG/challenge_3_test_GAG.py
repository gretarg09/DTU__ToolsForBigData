from __future__ import division
from itertools import combinations
from sklearn.feature_extraction import FeatureHasher
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import imagehash
import json
import time
import math
from PIL import Image
from collections import Counter
from collections import defaultdict


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
#video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/more_than_twenty"
video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/small_videos"


import imageio
filename = "/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4"

reader = imageio.get_reader(filename)

# Set variables
length = len(reader)
bedge_size = 250
frames_lsh = []

for counter, frame in enumerate(reader):
    
    if counter > (length / 2) - (bedge_size/2) and counter < (length/2) + (bedge_size/2):
                                
        # Start analysing the frames
        
        #### CROP IMAGE ####
        # Here we crop the black frame from the images
        # There are two different cases, either a portreit image of a landscape image3
        
        height = np.size(frame, 0)
        width = np.size(frame, 1)
        
        print("height : {}".format(height))
        print("width : {}".format(width))
        
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
    
    
print(frames_lsh)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


