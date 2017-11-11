#Two subreddits have an author in common if the author has made a 
#comment on threads in both subreddits.
#Show the 10 subreddit pairs with most authors in common and how 
#many authors they have in common.

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

# this varibles are here so we dont have to do the same query many times
subreddit_id = 'None'
authors_id_one = []


def comon_author_in_subreddits(subredditts_ids):
	#print 'hallo'
	global authors_id_one
	global subreddit_id
	b = random.randint(0, 10)
	
	print subredditts_ids
	subreddit_id_one, subreddit_id_two = subredditts_ids

	if subreddit_id != subreddit_id_one: 
		print "boom"
		cur.execute("""
			SELECT  DISTINCT  author_id
			FROM comments
			where	 subreddit_id = ?
			
			
			""", (subreddit_id_one,))

		authors_id_one = cur.fetchall()
		subreddit_id = 	subreddit_id_one

	print '1111'


	cur.execute("""
		SELECT DISTINCT author_id
		FROM comments	
		where subreddit_id = ?
		
		
		""", (subreddit_id_two,))
	print "1.51.51.51.51.5"

	authors_id_two = cur.fetchall()

	print '22222'

	#in_comon = set(author_id_one).intersection(set(author_id_two))
	num_comon = 0
	# for author in authors_id_one:
	# 	if author in authors_id_two:
	# 		num_comon += 1
	# p = set(list1)&set(list2)
	
	for author in authors_id_one:
		num_comon += authors_id_two.count(author)
   
   	print "asdf"

	return (num_comon, subreddit_id_one, subreddit_id_two)
	
	


if __name__ == '__main__':
	print "\nHello Mr Programmer, I'm running..\n"
	t1 = datetime.now()

	with conn:



		cur.execute("""
			SELECT distinct t1.id, t2.id
			FROM subreddits t1, subreddits t2
			"""
			)

		print "\nfirst SQL Query finished..\n"
		k = 0
		best_results = []#Queue.PriorityQueue(maxsize=10)
		while k<3:
			try:
				p = Pool(15)
				result = p.map(comon_author_in_subreddits, cur.fetchmany(5))
				for i in result:
					heapq.heappush(best_results, i) #best_results.put(i)
				p.close()
				p.join()
			except Exception as e:
				print e
				break
			k += 1



	t2 = datetime.now()

	print "Time taken: {}".format(t2-t1)
	for i in heapq.nlargest(10, best_results):
		print i

	print "\nGod by Mr Programmer, I'm Done..\n"