from __future__ import division

import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time


filenames = [
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur1/1XQZDVLZ1LS1.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/ur1/5VQKMCWWPZW3.mp4", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4/", 
        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/76KUS3QCGVCY.mp4/"]
# cap = cv2.VideoCapture(filenames[0])
# ret = True
# while(ret):
#     ret, frame = cap.read()
#     print frame
#     print ret
#     #cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

pxls = 10
for file in filenames:
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
	    	#print gray
	    	#print gray + sum_images
	    	sum_images = gray + sum_images


	    else:
	    	print "---ELSE---"
	    	print frame
	    	break

	    # Display the resulting frame

	    #cv2.imshow('frame',gray)

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	
	img_compared = np.empty((pxls,pxls))
	for i,row in enumerate(sum_images):
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
	print hash_string
	print int(hash_string.replace(" ", ""),16)
