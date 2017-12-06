from __future__ import division
import cv2 # for this I needed to install opencv -> pip install opencv-python
import os
import time

video_folder_path = "/Users/GretarAtli/Dropbox/ToolsForBigData/videos"

t1 = time.time()

frame_lengths = []
filenames = []

frame_tuple = []

counter = 0

for file in os.listdir(video_folder_path):    
    filepath = video_folder_path + "/" + file
    print (counter)

    cap = cv2.VideoCapture(filepath)
    frame_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    
    frame_lengths.append(frame_len)
    filenames.append(file) 
    frame_tuple.append((file,frame_len))

    counter += 1
    cap.release()
    
t2 = time.time()

print("\nNumber of files {}\n".format(len(frame_lengths)))
print("Min frame length {}\n".format(min(frame_lengths)))
print("Max frame length {}\n".format(max(frame_lengths)))
print("Execution time {}\n".format(t2-t1))


# When everything done, release the capture
cv2.destroyAllWindows()