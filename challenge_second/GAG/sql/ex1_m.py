from __future__ import print_function
import sqlite3
import time
from multiprocessing import Process, Pool
import string
import heapq


def query(subreddit_id):

	cur.execute(""" 
	SELECT body 
	FROM comments
	WHERE subreddit_id = ?
	""",
	subreddit_id)

	all_words = set()

	for d in cur.fetchall():
		# extract the data of the tuple
		comment = d[0]

		# ===================== clean the data ======================================
		translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
		#translator = string.maketrans(string.punctuation, ' '*len(string.punctuation))
		comment = comment.translate(translator).lower()

		all_words.update(comment.split())
		# ====================== end of cleaning ====================================


	nr_of_words = len(all_words)

	return (nr_of_words, subreddit_id)


if __name__ == '__main__':

	# Start the timer
	t1 = time.time()

	# Create a connection to the database
	con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
	# Tell sql that to convert the bytes returned by the query using the str function, same as doing str(the_bytes, 'utf-8')
	con.text_factory = str
	cur = con.cursor()

	#cur.execute("SELECT id FROM subreddits")   #(%s, %s, %s)", (var1, var2, var3))
	#cur.execute("SELECT id FROM subreddits WHERE id='t5_2qh0u'") 
	cur.execute("SELECT id FROM subreddits where id = 't5_2fwo'")
	
	p = Pool(8)
	results = p.map(query, cur.fetchall())
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
		
