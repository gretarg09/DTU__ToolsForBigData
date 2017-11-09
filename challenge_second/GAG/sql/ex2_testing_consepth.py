import sqlite3
import time
import multiprocessing
import heapq
import numpy as np


# The program proceedure
# 1) Get all subreddits
# 2.1) Run each subreddit on a specific thread
# 2.2) in each thread find the average dept of a thread with recursive sql
# 3) Find the Top 10 subreddit threads with the deepest subreddit threads on average 

if __name__ == '__main__':

	t1 = time.time()

	con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
	con.text_factory = str

	cur = con.cursor()

	Subreddit_id = 't5_2zlk4'

	print Subreddit_id

	print "\n######### STARTING #########"
	print

	# For each subreddit find all of the top level threads. 
	# They can be identified by the fact that they all start with t3

	cur.execute(""" 
				SELECT id, body 
				FROM comments
				WHERE subreddit_id = ? 
				AND parent_id LIKE 't3%'
				""",
				[Subreddit_id] )

	data = cur.fetchall()

	

	#print data
	depths = []
	for d in data:
		#print d[0] # the id
		cur.execute(""" WITH deepness (id,depth) AS 
					(
						-- INITIALIZATION  
						values (?,0)
		
						UNION ALL
		
						-- RECURSIION STEP
						SELECT comments.id, deepness.depth+1
						FROM comments JOIN deepness on comments.parent_id = deepness.id
					)
					Select max(depth) from deepness
					""", [d[0]])

		finalData = cur.fetchall()

		depths.append(finalData)

	print "############### Final dept array ######################"
	print depths
	print "The mean depth"
	print np.mean(depths)

	t2 = time.time()

	print "The execution time is {}".format(t2-t1)



