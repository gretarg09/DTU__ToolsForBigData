from __future__ import division 
import sqlite3
import time
import string

symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
start = time.time()


with con:
	# Get the first 20 subreddits
	cur = con.cursor()

	#cur.execute( """SELECT DISTINCT LOWER(id) FROM subreddits LIMIT 20""")  
	cur.execute("SELECT DISTINCT LOWER(id) FROM subreddits WHERE id='t5_2qh0u'") 
	#cur.execute("SELECT DISTINCT id FROM subreddits where id = 't5_2fwo'")


	for subreddits_id in cur.fetchall():

		# Get all comments for a subreddit 
		cur.execute(
			""" 
			SELECT body 
			FROM comments
			WHERE subreddit_id = ?
			""", subreddits_id
			)

		distinct_words = set()

		for d in cur.fetchall():

			# ===================== clean the data ======================================
			#comment = d[0]
			#comment = comment.lower()
			#for sym in symbols:
			#	comment = comment.replace(sym, " ")

			#for w in comment.split(" "):
			#	if len(w.replace(" ","")) > 0:
			#		distinct_words.add(w)


			# ====================== end of cleaning ===================================

			comment = d[0]
			comment = comment.lower()
			comment = comment.translate(string.maketrans("",""), string.punctuation)

			for word in comment.split():
				distinct_words.add(word)



		print "{} number of words {}" .format(subreddits_id, len(distinct_words))

end = time.time()

print "----------------------"
print "Exectution time was {}".format(end - start)