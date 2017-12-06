from __future__ import division
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time
import math
import sklearn.cluster as cluster
from sklearn import mixture
from sklearn.cluster import KMeans
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice
from os import listdir
from os.path import isfile, join



filenames = [
        "C:/Users/helga/Dropbox/Andri/hond1/0WS86GPURFK5.mp4", 
        "C:/Users/helga/Dropbox/Andri/hond1/76KUS3QCGVCY.mp4", 
        "C:/Users/helga/Dropbox/Andri/hond1/96EC4QS20Z28.mp4", 
        "C:/Users/helga/Dropbox/Andri/hond1/CL8W7L333U90.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/FDAZ5NL5NFL2.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/HBX8QLI9HH25.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/JY2ZAINWD2RX.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/LP47ZGJ256YU.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/NTETO8P77N96.mp4",
        "C:/Users/helga/Dropbox/Andri/hond1/SLK2PRXGW3DZ.mp4"]

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

num_clusters = 21
data = []
video_name = []
pxls = 8
# mypath = "C:/Users/helga/Dropbox/Andri/hond1"
mypath = "C:/Users/helga/Dropbox/Andri/more_than_twenty"
# mypath ="C:/Users/helga/Dropbox/Andri/ten"
filenames = ["C:/Users/helga/Dropbox/Andri/more_than_twenty/" + f for f in listdir(mypath) if isfile(join(mypath, f))]
print "starting...."
for file in filenames:
    cap = cv2.VideoCapture(file)
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print( "Video frame length: {}".format(length) )
    
    
    sum_images = np.zeros((pxls,pxls + 1))

    # print("--------------------------------------")
    # print file
    
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
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
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

    video_name.append(file[len(mypath)+1:-4])
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
    
    # print hash_string
    data.append([int(has,16) for has in hash_string.split()])


    params = {'damping': .77,
         'preference': -240,
         'quantile': .2,
         'n_clusters': num_clusters,
         'eps': .18,
         'n_neighbors': 2}

# normalize dataset for easier parameter selection
X = StandardScaler().fit_transform(data)

# estimate bandwidth for mean shift
bandwidth = cluster.estimate_bandwidth(X, quantile=params['quantile'])

# connectivity matrix for structured Ward
connectivity = kneighbors_graph(
    X, n_neighbors=params['n_neighbors'], include_self=False)
# make connectivity symmetric
connectivity = 0.5 * (connectivity + connectivity.T)

# ============
# Create cluster objects
# ============
ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(X)

two_means = cluster.MiniBatchKMeans(n_clusters=params['n_clusters']).fit(X)

ward = cluster.AgglomerativeClustering(
    n_clusters=params['n_clusters'], linkage='ward',
    connectivity=connectivity).fit(X)

spectral = cluster.SpectralClustering(
    n_clusters=params['n_clusters'], eigen_solver='arpack',
    affinity="nearest_neighbors").fit(X)

dbscan = cluster.DBSCAN(eps=params['eps']).fit(X)

affinity_propagation = cluster.AffinityPropagation(
    damping=params['damping'], preference=params['preference']).fit(X)

average_linkage = cluster.AgglomerativeClustering(
    linkage="average", affinity="cityblock",
    n_clusters=params['n_clusters'], connectivity=connectivity).fit(X)

birch = cluster.Birch(n_clusters=params['n_clusters']).fit(X)

gmm = mixture.GaussianMixture(
    n_components=params['n_clusters'], covariance_type='full').fit(X)




# Clustering algorithms
kmeans = cluster.KMeans(n_clusters=num_clusters, random_state=0).fit(X)    
agglomerative = cluster.AgglomerativeClustering(n_clusters=num_clusters, linkage="ward").fit(X)
#spectral = cluster.SpectralClustering(n_clusters=num_clusters, affinity="precomputed", n_init= 200).fit(data)
#affinity = cluster.affinity_propagation(S=data, max_iter=200, damping=0.6)
#gmix = mixture.GaussianMixture(n_components=num_clusters, covariance_type='full').fit(data)
    

    #https://ekzhu.github.io/datasketch/lsh.html
    

clustering_algorithms = (
        ('MiniBatchKMeans', two_means),
        ('AffinityPropagation', affinity_propagation),
        ('MeanShift', ms),
        ('SpectralClustering', spectral),
        ('Ward', ward),
        ('AgglomerativeClustering', average_linkage),
        ('DBSCAN', dbscan),
        ('Birch', birch),
        ('GaussianMixture', gmm),
        ('kmeans', kmeans),
        ('agglomerative', agglomerative)
    )


clusters_and_names = []

for name, algorithm in clustering_algorithms:


    try:
        video_and_label = zip(algorithm.labels_, video_name)
    except:
        # gmm dose not have .labels method
        video_and_label = zip(algorithm.predict(X), video_name)
    
    clusters = {}
    
    for label, video in video_and_label:

         if label not in clusters:
            clusters[label] = set([video])
         else:
             clusters[label].add(video)
        
    clusters_and_names.append((name, clusters.values()))
    



# check the rand index



from sklearn.metrics import adjusted_rand_score



def rand_index(clusters):
    truth = [
        set(['PC9Q6BW6W8VQ', '4DDXSHKS2IO4', 'VQGCPX8Z6XGH', 'QBH7QIIFQ4UK', 'PJNRJE4KRMVA', 'VU18BXJ7E98V', 'SJM8AQIRRGEM', 'JS2IGMCCE0UR', 'TQ8JXUOLLYM6', 'SHAG7PK12DY3']),
        set(['X0XJZ82P91XP', 'ITCIIVP3NIWT', 'MZQ8UKOI2TH1', 'FWTIVJWGC5W0', '5LBXP3DQB1ZV', 'CFBJKY8U2EJJ', 'AFA0UAQH5R80', 'MTWOUICAOQHH', 'F8875AUQ1YW5', '2OBHSZIX0AMS']),
        set(['HL63F2BNOXQO', 'HHVNVHP7RE44', 'O3EYQ5KCXQN2', '5L48Z43BI5OM', '5MZQ0TJ71OF3', 'MJ3NBDBHKX2Z', 'PT0KESCPZ7UU', '5VAW399EPYMT', 'PKEM4LE0MQ9K', 'LTXMMAQUHLR4']),
        set(['EMEHLAKYA8E6', 'HNL7C8Q3M4HO', '1S4O2POCTDGM', 'DWOZ8DJXK4PO', 'REBYLY0QRKSS', 'MAT24SZ88H1X', '4CU1929MA650', '9220H8P1KB4W', '5D18P9GTGUMD', 'DG1KC6AT1O2S']),
        set(['LC74ZN0KULDF', 'O6DRDN55LGS4', 'WHQZOEVJUI34', '2GEVEDOAWTGZ', 'MM2B45SULBQ4', '5WZSXVXQ2WBN', '0V0CA9OJC2FM', 'WQJ7C35XQ6ZY', '7TYVE8D1TWB4', 'IB45QHV3ZWPN']),
        set(['KVQ0DI7DMA9M', 'N9M13WSJ9O4X', 'ZR48D91D1ZIH', 'X903IBGRY8LF', 'VYS8B8HE6EM1', 'VFZ003C37B5Z', 'MATT3IM1R8K5', 'VI3E9GKO6GPS', 'BCV838KCL850', '5LF9DICID5LS']),
        set(['2H79ACWZUQED', 'ZLIFGZW9D741', '8NUMCA0BWN8W', 'ZPLEWBTAEIXG', '39KDGW6G5QKC', 'M6DX4IDA6OSH', '93CYWYVZIOGZ', 'O90LFFI2ZR1W', 'FG7BBEEDVSYI', 'A6O7JS2Y8CDW']),
        set(['SFR07XTFCCJU', '5EEZNJ918JHG', '0K160AK52ZYS', 'EZUCOY1XGOSO', 'VO8CJU4Z62G8', 'FVMG6J0COUYW', '8CENFQPL2FI5', 'QCBLNBSJUE4X', 'IO7OXN9XLR8B', 'YPPU9HYNYB33']),
        set(['BQI3RYQ1TAJV', 'NOPATUEXOGUV', 'RVX7KINPR50Q', 'LHAT5CZTGWIX', 'HYG0R2DNZQTW', 'LYZ5WFPPDN4C', 'ZH1KIMY7KWYU', 'VWCWOXBEAIRB', 'KD3E9UZFRNFL', 'TSIGN83K0772']),
        set(['P4N2V0NVVV8H', 'YMHF4GAOFNOA', 'EP1H5ZJ5VHLH', 'Z32MBWUK5EAC', '59YXH3WTZEUE', 'H73ZJDYPXHJ9', 'PYMUTU6LGTEK', 'FWR8AQHXYDSQ', 'V3RT1616SU2T', 'HEKXL3LG1FYK']),
        set(['PI64R8RDU5KH', 'S9XAH4MG6NOF', 'WFAZYD4K3BHL', 'AWV4XDBZBNXV', 'U66VLX1FZ4VB', '6P3N8Y3SOUBU', 'QVUKU04SK1IP', 'YCLD5KJBZ9WW', 'GKT85KBXD457', '3ZYOF88E62SK']),
        set(['LDY5SZC34GMH', 'DRQZDUT9I2IX', 'N0RE8W3NKA6F', 'ZQT3SIA3CU7E', '5BERVTCC67NL', 'XBFWVA6VXOUI', '0A3J1A75VD25', '5U99NV1IYXJD', '62RCAEP9V3YQ', 'PDUHWMAFTQUA']),
        set(['VFUYELZ8N98L', 'OPAB10OUZINI', 'PRI2JWRAZRQ2', '7NICDIC6YEJG', 'GI3AS3PL1G6G', 'MZGFXOFYZ3B9', '1GYZIHN8D9YF', '5JV8MT8T7217', '9KQ5PTREJHNG', 'KMSO4053DNKA']),
        set(['94HUNOV6D50Z', '6U4GSNO3HZ9U', 'IYRA8ZQXPCSK', '9M8S1D2ED4X1', '75WSCVHV9RIJ', '8MVEMXM1H0IC', 'OLJRO416ROSQ', 'TYK8MF9HTCSE', '7L2I0KW236DJ', 'GZRUU9MVD5F5']),
        set(['PU2OOPTYI6AF', 'TL2D29GA5YXY', '5OEOC4A11DFL', 'VDYMLFBSRHOD', 'STL4SNVVPH2Q', '9NQROV3KHAFC', 'I9TO1T2YDY0C', 'X3X9FELTJRU9', 'X281EK4DGMWJ', '1BZTVRL7CJPB']),
        set(['PIV7A2LAA2R1', 'N776WD6EU8Q3', '9BVHN720PO3G', 'Q7HYH9EZUFMY', 'VZV2SE7ZOJRJ', 'HGGSF2RGMHYA', 'Y8GUIRV70HB4', 'A9HJ87EGKR8D', 'U58K6OYTTQY4', 'L22AT94NBT0U']),
        set(['OAG1MKHELHFO', 'J2ZXNIG0BPLP', 'GHXX0GDZC2ZJ', 'Q74808QJ9V61', 'KX9V5HTQGPIU', '79KNQAACVXMT', '1T8KUDXSVGTO', 'E2GSJWN0KZ5F', 'QCUIPNF8JE1G', 'JQ9155A40CNK']),
        set(['6M0ITNH532FT', '6OC9OYOTGW3H', 'H7CSJS65M5H4', 'BYC3ODH9BE7M', 'OI2N8AESXCOC', 'F73M1Y00VMQ3', 'XTIDZ33TA21B', '8FW7TDBYR3R6', 'QWM74DETIGU3', 'RAGRTH1HRLWI']),
        set(['VOYHGYGUEI2D', '60FCHT4BLIBE', 'Y834K5B6FDSJ', '4IXLA4JNYZCV', 'SAK6MDHJ0Z56', 'HLAAP1HCYV35', '4Q58ULSTRL2Z', 'GBQBEU144BMT', 'WDBQUVHM7TES', 'IJP10DNTNCNV']),
        set(['V3HS7SDTYQN4', 'E8VCNFOWCW1N', 'RL4MKRP524PU', 'COCSVWTEY6AE', 'WBNMSO7X17PU', 'INRA6NWETUDL', 'RUWUCFQZQH9W', 'GY03QRA6FXCM', '7J1RW84N7IUZ', 'Z86FHQ2O1SVS']),
        set(['LUW4GWH3RP4Z', 'ZZTM0X6OON1U', '1XMN4WYN9ZOG', 'L5SPAW18PX07', '8PBLJBOI3GB1', 'A11Z6M9V9B89', 'GZIGOU721UZZ', '6MUNQE00N2V5', '3OB1UZGIE8ZY', 'E667SMU77M16'])

        ]
    elems = list(set.union(*truth))
    
    # Index of Containing Set
    memory_truth = {}
    memory_clusters = {}
    def ics(element, set_list, set_list_name):
        if set_list_name == "truth":
            if element in memory_truth:
                return memory_truth[element]
        if set_list_name == "clusters":
            if element in memory_clusters:
                return memory_clusters[element]

        for c, s in enumerate(set_list):
            if element in s:
                if set_list_name == "truth":
                    memory_truth[element] = c
                if set_list_name == "clusters":
                    memory_clusters[element] = c
                return c

    x = map(lambda e: ics(e, clusters, 'clusters'), elems)
    y = map(lambda e: ics(e, truth, 'truth'), elems)
   

    return adjusted_rand_score(x,y)

for name, clusters in clusters_and_names:
    print name
    # print
    # print clusters
    # print
    print type(clusters),len(clusters)
    print "rand index: {}".format(rand_index(clusters))
    print

# k = 0
# for name, clusters in clusters_and_names:
#     for clst in clusters:
#         k += 1
#         print len(clst), k
#     print name