from __future__ import division,print_function
import sqlite3
import time
import heapq
from multiprocessing import Process, Pool 
from itertools import combinations
from collections import defaultdict
from itertools import combinations


con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
con.text_factory = str
cur = con.cursor()


def getUniqNameListCount(subreddit_id):
	#print("Running for {}".format(subreddit_id))
	cur.execute("SELECT author_id FROM comments WHERE subreddit_id = ?",[subreddit_id])
	return (set([i[0] for i in cur.fetchall()]),subreddit_id )



if __name__ == '__main__':

	print("########### Starting ################")

	t1 = time.time()

	cur.execute("""SELECT subreddit_id, count(ROWID) 
				   FROM comments 
				   GROUP BY subreddit_id""")


	top_n = cur.fetchall()
	top_n.sort(key=lambda x: x[1],reverse=True)

	t2 = time.time()

	n = 2 # number of top subreddits Ids

	for i in top_n[0:n]:
		print (i)

	print("######### First step Finished #########")
	print("Execution time {}".format(t2-t1))	

	# Next step is to take the subreddit_ids that have the most comments 
	# and find all of the authors that they do have in common 

	# First I get all the unique authors of these subreddit Ids

	t3 = time.time()

	p = Pool(n)
	results = p.map(getUniqNameListCount, [i[0] for i in top_10[0:n]])
	p.close()
	p.join()

	t4 = time.time()

	print("######### Second step Finished #########")
	print("Execution time {}".format(t4-t3))

	print(results[0])

	# Add the result into a default dict 

	t5 = time.time()
	top_n_distinctAuthors = defaultdict(set)

	# Find the common authors of the pairs
	for result in results:
		top_n_distinctAuthors[results[1]] = results[0]

	t6 = time.time()

	print("Adding dictionary execution time {}".format(t6-t5))

	the_result = defaultdict(int)

	# Now we use iteritem combination to get find the the number of common authors between pairs
	#for i in combinations(top_n_distinctAuthors.keys, 2):
	#	the_result[i] = 


	print("Overall execution time {}".format(t6-t1))




