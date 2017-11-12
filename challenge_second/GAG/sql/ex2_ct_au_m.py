from __future__ import division,print_function
import sqlite3
import time
import heapq
import numpy as np
from multiprocessing import Process, Pool 
from itertools import combinations


con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
con.text_factory = str
cur = con.cursor()


def getUniqNameListCount(subreddit_id):
	#print("Running for {}".format(subreddit_id))
	cur.execute("SELECT author_id FROM comments WHERE subreddit_id = ?",subreddit_id)
	return ( len(set([i[0] for i in cur.fetchall()])) ,subreddit_id )



if __name__ == '__main__':

	t1 = time.time()

	print ("########### Starting ################")

	#Subreddit_id = 't5_2qh1i'
	#Subreddit_id = 't5_2qhli'

	cur.execute("SELECT id FROM subreddits")

	t2 = time.time()

		# Start a pool of threads
	p = Pool(100)

	results = p.map(getUniqNameListCount, cur.fetchall())
	
	p.close()

 
	top_ten = heapq.nlargest(10, results)

	result_for_file = []
	fetch = ""
	for i in top_ten:
		cur.execute("select name from subreddits  where id = ?",i[1])
		fetch = cur.fetchall()[0][0]
		print (i, fetch)
		result_for_file.append(str(i[0]) +"     " + str(i[1][0]) + "      " + fetch)

	t2 = time.time()

	print ("Execution time {}".format(t2-t1))

	print ("\n######### ENDING #########")
	print
