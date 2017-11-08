import sqlite3
import time
import multiprocessing
import heapq


if __name__ == '__main__':

	con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
	con.text_factory = str

	cur = con.cursor()

	Subreddit_id = 't5_2r0gj'

	print Subreddit_id

	print "\n######### STARTING #########"
	print

	# For each subreddit find all of the top level threads. 
	# They can be identified by the fact that they all start with t3

	cur.execute(""" 
				SELECT id, body 
				FROM comments
				WHERE subreddit_id = ?
				--AND parent_id = 't3_2qyr1a'
				AND parent_id LIKE 't3%'
				--LIMIT 1
				""",
				[Subreddit_id] )

	data = cur.fetchall()

	#print data

	for d in data:
		print d[0] # the id
		print d[1] # the body
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

		print finalData
		print "-----------------------------------"






