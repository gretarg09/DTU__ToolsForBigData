# The size of a vocabulary for a subreddit is defined as the total # number of distinct words is used in the comments of the 
# subreddit.

import sqlite3
import time
from multiprocessing import Process, Pool
import string

con = sqlite3.connect('reddit.db')
con.text_factory = str
cur = con.cursor()

def query(subreddit_id):
	# make a querey search
	#subreddit_id,cur = subreddit_id 

	t1 = time.time()
	symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']
	
	cur.execute(""" 
	SELECT DISTINCT body 
	FROM comments
	WHERE subreddit_id = ?
	""",
	subreddit_id)
	
	# Fetch the resulting data
	data = cur.fetchall()
	# here we will have all our unique words, except the first distrinct words
	all_words = []

	for d in data:
	
		# extract the data of the tuple
		comment = d[0]

		# ===================== clean the data ======================================
		comment = comment.lower()
		# for sym in symbols:
		# 	comment = comment.replace(sym, "") 
		comment = comment.translate(string.maketrans("",""), string.punctuation)


		

		
		for word in set(comment.split()):
			all_words.append(word)

	
	res = (len(set(all_words)), subreddit_id)

	return res




if __name__ == '__main__':


	with con:

		# Get the cursor object
		
		subreddit_nr = 0 #subreddit_nr var i..
		cur.execute("SELECT DISTINCT id FROM subreddits where id = 't5_2fwo'")   #(%s, %s, %s)", (var1, var2, var3))
		
		
		t3 = time.time()

		p = Pool(4)

		result = p.map(query, cur.fetchall())
		print result
		p.close()
		p.join()
		# for d in cur.fetchall():
		# 	bla = query(d)
		# 	print bla
		t4 = time.time()

		print "THe time", t4-t3
		


   # p = Process(target=f, args=('bob',))
   # p.start()
   # p.join()




