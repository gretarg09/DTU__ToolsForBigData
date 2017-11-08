import sqlite3
from datetime import datetime
from multiprocessing import Pool


conn = sqlite3.connect('/Users/helga/OneDrive/Documents/ToolsForBigD/challenge2/reddit.db')
conn.text_factory = str
cur = conn.cursor()

def query_subreddit(subreddit_id):
	pass



if __name__ == '__main__':
	print "\nHello Mr Programmer, I'm running..\n"
	t1 = datetime.now()
	with conn:
		cur.execute(""" 
			SELECT id  
			FROM subreddits
			"""
			)

	print len(cur.fetchall())
	t2 = datetime.now()

	print "The time is {}".format(t2-t1)