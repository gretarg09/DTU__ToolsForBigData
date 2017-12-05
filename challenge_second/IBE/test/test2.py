from __future__ import division

import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time
from os import listdir
from os.path import isfile, join
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

data = []


filenames = ["C:/Users/helga/Dropbox/Andri/ur1/1XQZDVLZ1LS1.mp4",
			 "C:/Users/helga/Dropbox/Andri/ur1/5VQKMCWWPZW3.mp4",
			 "C:/Users/helga/Dropbox/Andri/hond2/4IVIG8O5PNHB.mp4",
			 "C:/Users/helga/Dropbox/Andri/hond2/Y97Z4868G3XV.mp4",
			 "C:/Users/helga/Dropbox/Andri/more_than_twenty/0V0CA9OJC2FM.mp4"]


#mypath = "C:/Users/helga/Dropbox/Andri/more_than_twenty"
#mypath ="C:/Users/helga/Dropbox/Andri/ten"
#filenames = ["C:/Users/helga/Dropbox/Andri/ten/" + f for f in listdir(mypath) if isfile(join(mypath, f))]


 
# print filenames
# exit(1)

pxls = 8
num_clusters = 20
num_name = []
num = 0
total_ture = np.zeros((pxls,pxls))

for file in filenames:
	#file = mypath + file
	#print file

	cap = cv2.VideoCapture(file)
	sum_images =  np.zeros((pxls,pxls + 1))

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read(1)

	    # Our operations on the frame come here
	    


	    if ret:
	    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    	#print gray
	    	#print type(gray)
	    	# 9 columns, 8 rows, diffrence between libs
	    	gray = cv2.resize(gray,(pxls + 1,pxls))
	    	img_compared = np.empty((pxls,pxls))
	    	num += 1
	    	for i,row in enumerate(gray):
	    		for j,column in enumerate(row):
	    			if j + 1 == len(row):
			            break
			        else:
			            img_compared[i][j] = row[j] > row[j+1]
			            if img_compared[i][j]:
			            	total_ture[i][j] = total_ture[i][j] + 1


	    else:
	    	break

	    # Display the resulting frame

	    #cv2.imshow('frame',gray)

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()


	

	for i,row in enumerate(gray):
		for j,column in enumerate(row):
			if j + 1 == len(row):
				break
			else:
				img_compared[i][j] = total_ture[i][j] > num / 2





	for i,row in enumerate(img_compared):
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
	print file
	print hash_string
	print
	total_ture = np.zeros((pxls,pxls)) 