from __future__ import division
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
import json
import time
import mmh3

# ------------------ Reading in data and preprocessing ----------------------

path_to_folder = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/week_10/ex10/data"
name = '/reuters-'

file_paths = []

for i in range(3):
    for j in range(10):
        if i== 2 and j > 1:
            break
    
        file_paths.append(path_to_folder  + name + '0' + str(i) + str(j) + '.json')   

topics = []
bodies = []

# Read in the data
# we use try and catch to remove all articles that do not have at least one topic and a body
# we append one to the topic array if earn is part of the topics of the article. 
# We append 0 otherwise
for path in file_paths:
    with open(path) as json_data:
        d = json.load(json_data)
        for di in d:
            try:
                topic = di['topics']
                body = di['body']
                # Check if earn is part of the topics
                if "earn" in topic:
                    topics.append(1)
                else:
                    topics.append(0)
                bodies.append(body)
            except:
                pass
            

# -------------- The bag of word model ----------------------------

t1 = time.time()

# Create raw bag-of-words encoding.
cv = CountVectorizer(stop_words="english", lowercase=True)
bag_of_words_matrix = cv.fit_transform(bodies)
bag_of_words_matrix.toarray()

# Split the data into training and testing set
x_train,x_test,y_train,y_test = train_test_split( bag_of_words_matrix, topics, test_size=0.2)

# Now we are ready to use the random forest classifier
clf = RandomForestClassifier(n_estimators=50)
clf.fit(x_train, y_train)
y_predicte = clf.predict(x_test)

t2 = time.time()

# Report the score
print ("The bag of words implementation")
print ("--------------------------------")
print ("     The score is {}".format(
    np.sum( np.array(y_test) == np.array(y_predicte) ) / len(np.array(y_test))
    ))
print ("     The execution time was: {}\n".format(t2-t1))

# ---------------------- Feature hashing model ----------------------
# Now we implement feature hashing and use 1000 buckets instead of the raw bag-of-words encoding.

# First we implement the hashing vectorizer
# We both tried the build in hash function in python and the mmh3 hash() module in python
# Both methods gave similar results. We chose to go with the build in function
def hashing_vectorizer(features, N):
    x = np.zeros(N)
    for f in features:
        h = hash(f)
        #f = f.encode('utf-8')
        #h = mmh3.hash(f)
        x[h % N] += 1
        
    return x

t3 = time.time()

# initialize the feature hashing matrix
N = 1000 # number of buckets
feature_hasing_matrix = np.zeros((len(bodies), N))

# create the feature hashing matrix
for i,_ in enumerate(feature_hasing_matrix):
    feature_hasing_matrix[i] = hashing_vectorizer(bodies[i],N)
    
# Know we use this matrix to train our machine learning algorithm

# Split the data into training and testing set
x_train,x_test,y_train,y_test = train_test_split( feature_hasing_matrix, topics, test_size=0.2)

# Now we are ready to use the random forest classifier
clf = RandomForestClassifier(n_estimators=50)
clf.fit(x_train, y_train)
y_predicte = clf.predict(x_test)

t4 = time.time()

# Report the score
print("The feature hashing implementation")
print("     The score is {}".format(
    np.sum( np.array(y_test) == np.array(y_predicte) ) / len(np.array(y_test))
    ))
print ("     The execution time was: {}".format(t4-t3))