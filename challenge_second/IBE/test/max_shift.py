import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
import json
import time
from os import listdir
from os.path import isfile, join
import os



mypath ="C:/Users/helga/Dropbox/Andri/ten"
#filenames = ["C:/Users/helga/Dropbox/Andri/ten/" + f for f in listdir(mypath) if isfile(join(mypath, f))]
fn = mypath
la = [(x[0], time.ctime(x[1].st_ctime)) for x in sorted([(fn, os.stat(fn)) for fn in os.listdir(mypath)], key = lambda x: x[1].st_ctime)]

for i in la:
	print i
# mypath = "C:/Users/helga/Dropbox/Andri/hond1"
# filenames = ["C:/Users/helga/Dropbox/Andri/hond1"  + f for f in listdir(mypath) if isfile(join(mypath, f))]


num_frames = []
num_frames_video = 0
for file in filenames:
	#file = mypath + file
	#print file
	print file

	cap = cv2.VideoCapture(file)

	num_frames_video = 0
	each_video = []	
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read(1)

	    # Our operations on the frame come here
	    


	    if ret:
	    	

	    	num_frames_video += 1
	    	

	    else:
	    	#print "---ELSE---"
	    	#print frame
	    	each_video.append(num_frames_video)
	    	
	    	break
	print each_video



	cap.release()
	cv2.destroyAllWindows()

	num_frames.append(each_video)

print "hallli"
print num_frames
for video in num_frames:
	print max(video) - min(video)

