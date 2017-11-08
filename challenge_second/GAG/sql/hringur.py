import sqlite3
import string
import time
from collections import Counter
import multiprocessing
import operator
import heapq


def measure_subreddit(subreddit_id):

	#start = time.time()
	#print subreddit_id
	comment_text = ""
	for comment in c.execute(""" SELECT body  
							 	 FROM comments
								 WHERE subreddit_id=:id""", {"id": subreddit_id}):
		comment_text += " " + comment[0]

	comment_text = comment_text.translate(None, string.punctuation)
	comment_text = comment_text.translate(None, string.digits).lower()
	comment_text = comment_text.split()
	
	end = time.time()

	#print 'Runtime: ' + str(end-start) + ' id:' + subreddit_id
	return (len(set(comment_text)), subreddit_id) #{}.fromkeys(comment_text).keys()
		



if __name__ == "__main__":
	
	start = time.time()
	#Connect to our database
	conn = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')

	conn.text_factory = str

	result = []

	#Get a cursor object in the database
	c = conn.cursor()
	sub_ids = []



	for subreddit_id in c.execute("""SELECT id FROM subreddits WHERE id='t5_2fwo'"""):
		sub_ids.append(subreddit_id[0])
		
	print len(sub_ids)

	p = multiprocessing.Pool(8)

	result += p.map(measure_subreddit, sub_ids)

	print heapq.nlargest(10, result)
	#print max(result)


	end = time.time()

	print 'Runtime: ' + str(end-start)