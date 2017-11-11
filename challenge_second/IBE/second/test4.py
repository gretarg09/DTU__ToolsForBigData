import sqlite3
import itertools
import Queue
import heapq
import random

from datetime import datetime
from multiprocessing import Pool


conn = sqlite3.connect('/Users/helga/OneDrive/Documents/ToolsForBigD/challenge2/reddit.db')
conn.text_factory = str
cur = conn.cursor()





if __name__ == '__main__':
	print "\nHello Mr Programmer, I'm running..\n"

	with conn:
		cur.execute("""

			SELECT DISTINCT  t1.subreddit_id, t2.subreddit_id, t1.author_id, t2.author_id,  COUNT(t1.author_id)
             FROM comments t1, comments t2
       		WHERE t1.subreddit_id <> t2.subreddit_id
             AND t2.subreddit_id < t1.subreddit_id
             AND t1.author_id = t2.author_id
             GROUP BY t1.author_id, t2.author_id
             ORDER BY COUNT(*)
             DESC
             LIMIT 10
			""")

	print "\nQuery is Done!!..\n"
	print cur.fetchall()
