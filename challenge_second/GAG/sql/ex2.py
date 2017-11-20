from __future__ import division,print_function
import sqlite3
import time
import heapq
from multiprocessing import Process, Pool 
from itertools import combinations
from collections import defaultdict
from itertools import combinations
import operator


con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
con.text_factory = str
cur = con.cursor()


def getUniqNameListCount(subreddit_id):
	#print("Running for {}".format(subreddit_id))
	#print (subreddit_id)
	cur.execute("SELECT author_id FROM comments WHERE subreddit_id = ?",[subreddit_id])
	return ([i[0] for i in cur.fetchall()], subreddit_id)



if __name__ == '__main__':

	print("########### Starting ################")

	t1 = time.time()

	cur.execute("""SELECT subreddit_id, count(ROWID) 
					   FROM comments 
					   GROUP BY subreddit_id""")

	top_n = cur.fetchall()
	top_n.sort(key=lambda x: x[1],reverse=True)

	t2 = time.time()

	while True:

		n = 120 # number of top subreddits Ids

		for i in top_n[0:n]:
			print (i)

		print("######### First step Finished #########")
		print("Execution time {}".format(t2-t1))	

		# Next step is to take the subreddit_ids that have the most comments 
		# and find all of the authors that they do have in common 

		# First I get all the unique authors of these subreddit Ids

		t3 = time.time()

		p = Pool(n)
		results = p.map(getUniqNameListCount, [i[0] for i in top_n[0:n]])
		#results = p.map(getUniqNameListCount, ['t5_2qh61', 't5_2t9x3'])
		p.close()
		#p.join()

		t4 = time.time()

		print("######### Second step Finished #########")
		print("Execution time {}".format(t4-t3))

		# Add the result into a default dict 
		t5 = time.time()
		top_n_distinctAuthors = defaultdict(set)

		for result in results:
			top_n_distinctAuthors[result[1]] = set(result[0])

		t6 = time.time()

		print("Adding dictionary execution time {}".format(t6-t5))

		the_result = defaultdict(int)

		# Now we use iteritem combination to get find the the number of common authors between pairs
		for i in combinations(top_n_distinctAuthors.keys(), 2):
			the_result[i] = len(top_n_distinctAuthors[i[0]].intersection(top_n_distinctAuthors[i[1]] ))

		t7 = time.time()

		print("Finding the intersection execution time {}".format(t7-t6))

		the_result_sorted = sorted(the_result.items(), key=operator.itemgetter(1), reverse = True)

		print("Check if the 10 highest stake is smaller then top n+1")

		print("The result sorted {}".format(the_result_sorted[9][1]))
		print("Top 121 {}".format(top_n[n][1]))

		if top_n[n][1] <  the_result_sorted[9][1]:
			break
		else:
			n = n + 100

	
	for key,value in the_result_sorted[0:10]:
		name1 = cur.execute("SELECT name FROM subreddits WHERE id = ?",[key[0]]).fetchall()
		name2 = cur.execute("SELECT name FROM subreddits WHERE id = ?",[key[1]]).fetchall()
		print("{},{} - {}".format(name1[0][0],name2[0][0],value))

	t8 = time.time()
	print("Overall execution time {}".format(t8-t1))

