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

#filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/hond1/0WS86GPURFK5.mp4"]

filenames = ["/Users/GretarAtli/Dropbox/ToolsForBigData/ur2/LVK4R8FJA3N9.mp4"]

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

for file in filenames:
    cap = cv2.VideoCapture(file)
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video frame length: {}".format(length) )
    
    
    sum_images = np.zeros((pxls,pxls + 1))

    #print("--------------------------------------")
    #print file
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read(1)
        
        if ret:
            # Start analysing the frames
            
            #### CROP IMAGE ####
            
            height = np.size(frame, 0)
            width = np.size(frame, 1)
            
            if height > width: # if portrait image
                x = 256
                y = 454                
            else: # else it is a landscape 
                x = 454
                y = 256
        
            
            x_start = width/2 - x/2
            x_end = width/2 + x/2
            y_start = height/2 - y/2
            y_end = height/2 + y/2

            
            crop_frame = frame[y_start:y_end, x_start:x_end]
            
            #------------------#
            
            print (height,width)
            
            cv2.imwrite('croppedframeur.png',crop_frame)
            
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray = cv2.resize(gray,(pxls + 1,pxls))
            #sum_images = gray + sum_images

            
            break
            
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
    
    print hash_string
    print int(hash_string.replace(" ", ""),16)
    
    
    
    #https://ekzhu.github.io/datasketch/lsh.html
    
    
    
    
    
    
    
    
    