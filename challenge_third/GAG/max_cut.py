#!/usr/bin/env python
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
import cv2 # for this I needed to install opencv -> pip install opencv-python

from os import listdir
from os.path import isfile, join
import os

print "starting.."
# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'
dirpath = "C:/Users/helga/Dropbox/Andri/videos"
# get all entries in the directory w/ stats
entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))
#NOTE: on Windows `ST_CTIME` is a creation date 
#  but on Unix it could be something else
#NOTE: use `ST_MTIME` to sort by a modification date
num_frames = []
each_video = []
for cdate, path in sorted(entries):
	#print time.ctime(cdate), os.path.basename(path)
	#print path
	cap = cv2.VideoCapture(path)

	num_frames_video = 0	
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read(1)

	    # Our operations on the frame come here
	    


	    if ret:
	    	

	    	num_frames_video += 1
	    	

	    else:
	    	#print "---ELSE---"
	    	#print frame
	    	break
	



	cap.release()
	cv2.destroyAllWindows()

	each_video.append(num_frames_video)
	if len(each_video) % 10 == 0:

			num_frames.append(each_video)
			each_video = []

print "calc biggest cut"
biggest_cut = []
for video in num_frames:
    biggest_cut.append(max(video)  - min(video))
print "writing to file.."
with open('biggest_cuts.txt', 'w') as f:
    for cut in biggest_cut:
        f.write('\n' + str(cut))
    
    
    


