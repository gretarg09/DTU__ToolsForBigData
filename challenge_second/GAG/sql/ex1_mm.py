import sqlite3
import time
from multiprocessing import Process, Pool
import string


con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
con.text_factory = str
cur = con.cursor()

def query(subreddit_id):

	symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

	cur.execute(""" 
	SELECT body 
	FROM comments
	WHERE subreddit_id = ?
	""",
	subreddit_id)

	all_words = set()

	p2 = Pool(8)
	results_preprocessing = p2.map(preprocessing_data, cur.fetchall())
	
	for text in results_preprocessing:
		for word in text:
			all_words.add(word)

	p2.close()

	nr_of_words = len(all_words)

	return (nr_of_words, subreddit_id)

def preprocessing_data():
	comment = d[0]
	comment = comment.lower()
	comment = comment.translate(string.maketrans("",""), string.punctuation)
	return set(comment.split())



if __name__ == '__main__':

	with con:

		#cur.execute("SELECT DISTINCT LOWER(id) FROM subreddits LIMIT 1")   #(%s, %s, %s)", (var1, var2, var3))
		cur.execute("SELECT DISTINCT LOWER(id) FROM subreddits WHERE id='t5_2qh0u'") 
		#cur.execute("SELECT DISTINCT id FROM subreddits where id = 't5_2fwo'")
		
		t3 = time.time()
		p = Pool(8)
		results = p.map(query, cur.fetchall())
		
		for result in results:
			print result

		p.close()

		t4 = time.time()

		print "Execution time {}".format(t4-t3)
		
