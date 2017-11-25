from __future__ import division
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time


#filenames = [
#        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4", 
#        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/76KUS3QCGVCY.mp4", 
#        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/96EC4QS20Z28.mp4", 
#        "/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/CL8W7L333U90.mp4"]

filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4"]

pxls = 10

for file in filenames:
    cap = cv2.VideoCapture(file)
    sum_images = np.zeros((pxls,pxls + 1))

    print("--------------------------------------")
    print file
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read(1)
        
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray,(pxls + 1,pxls))
            sum_images = gray + sum_images
            
        else:
            break
        
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
    
    print "The full matrix"
    print img_compared
    
    hash_string = ""
    for difference in img_compared:
        print "each line:"
        print difference 
        decimal_value = 0
        hex_string = []  
        for index, value in enumerate(difference):
            print index
            if value: 
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value  = 0
        hash_string = hash_string +''.join(hex_string) + ' '
    
    print hash_string
    print int(hash_string.replace(" ", ""),16)
    
    
    
    
    
    
    
    
    
    
    
    
    