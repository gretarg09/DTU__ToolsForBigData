# The size of a vocabulary for a subreddit is defined as the total # number of distinct words is used in the comments of the 
# subreddit.

import sqlite3
from multiprocessing import Process, Pool
import string
from datetime import datetime






con = sqlite3.connect('reddit.db')
con.text_factory = str
cur = con.cursor()

def query(subreddit_id):
	# make a querey search
	#subreddit_id,cur = subreddit_id 

	
	cur.execute(""" 
	SELECT DISTINCT body 
	FROM comments
	WHERE subreddit_id = ?
	""",
	subreddit_id)

	# Fetch the resulting data
	data = cur.fetchall()
	# here we will have all our unique words, except the first distrinct words
	all_words_naive = []#
	words = set()
	
	
	for d in data:
		# extract the data of the tuple
		comment = d[0].lower()

		# clean the data 
		comment = comment.translate(string.maketrans("",""), string.punctuation)

		# collect the words
		all_words_naive += comment.split()
	# get the data
	words = set(all_words_naive)


	return (len(words), subreddit_id)




if __name__ == '__main__':


	with con:

		# Get the cursor object
		
		subreddit_nr = 0 #subreddit_nr var i..
		cur.execute("SELECT DISTINCT id FROM subreddits where id = 't5_2qh0u'")   #(%s, %s, %s)", (var1, var2, var3))
		
		

		t3 = datetime.now()

		p = Pool(10)

		result = p.map(query, cur.fetchall())

		print result
		p.close()
		p.join()
		p.terminate()
		
		t4 = datetime.now()
		print
		result_for_file = []
		fetch = ""
		for i in sorted(result, reverse = True)[:10]:
			cur.execute("select name from subreddits  where id = ?",i[1])
			fetch = cur.fetchall()[0][0]
			print i, fetch
			result_for_file.append(str(i[0]) +"     " + str(i[1][0]) + "      " + fetch)


		print "The time", t4-t3
	
		file = open("big_tools_res","w") 
 
		file.write("the time was: {}".format(t4-t3)) 
		file.write("\n") 
		for res in result_for_file:
			file.write(res + "\n") 
		 
		 
		file.close() 


