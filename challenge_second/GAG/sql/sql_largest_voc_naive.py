from __future__ import division 
import sqlite3
import timeit

symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

all_comments = 0

def process_comment(text):
	text = text.lower()
	for sym in symbols:
		text = text.replace(sym, " ")

	words = set()
	for w in text.split(" "):
		if len(w.replace(" ","")) > 0:
			words.add(w)

	return words



start = timeit.timeit()

con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')

with con:
	# Get the first 20 subreddits
	cur = con.cursor()
	i = 0
	cur.execute( """SELECT DISTINCT LOWER(id) 
					FROM subreddits 
					LIMIT 20""")  
	
	for subreddits_id in cur.fetchall():
		i += 1

		nr_comments_in_each = 0

		# Get all comments for a subreddit 
		cur.execute(
			""" 
			SELECT DISTINCT body 
			FROM comments
			WHERE subreddit_id = ?
			""", subreddits_id
			)

		comments = cur.fetchall()

		distinct_words = set()
		for comment in comments:
			nr_comments_in_each += 1
			all_comments += 1

			distinct_words = distinct_words.union(process_comment(comment[0]))

		print "{} {}  number of words {}" .format(subreddits_id, nr_comments_in_each, len(distinct_words))

end = timeit.timeit()

print "----------------------"
print "Exectution time was {}".format(end - start)
print "Number of comments processed {}".format(all_comments)



