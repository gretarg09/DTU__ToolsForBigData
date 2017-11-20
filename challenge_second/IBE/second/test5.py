#Two subreddits have an author in common if the author has made a 

#comment on threads in both subreddits.

#Show the 10 subreddit pairs with most authors in common and how 

#many authors they have in common.



import sqlite3

import heapq




from datetime import datetime

from multiprocessing import Pool

from itertools import combinations





conn = sqlite3.connect('C:\\Users\\s161294\\Downloads\\reddit.db')

conn.text_factory = str

cur = conn.cursor()



# this varibles are here so we dont have to do the same query many times

#subreddit_id = 'None'

#authors_id_one = []





def comon_author_in_subreddits(subredditts_ids):

    subreddit_id_one, subreddit_id_two = subredditts_ids





	cur.execute("""

		SELECT    author_id

		FROM comments

		where	 subreddit_id = ?

		

		

		""", (subreddit_id_one,))



	authors_id_one = cur.fetchall()










	cur.execute("""

		SELECT  author_id

		FROM comments	

		where subreddit_id = ?

		

		

		""", (subreddit_id_two,))

	



	authors_id_two = cur.fetchall()


	p = set(authors_id_one)&set(authors_id_two)
	num_comon = len(p)
	

	#for author in authors_id_one:

		#num_comon += authors_id_two.count(author)
	



	return (num_comon, subreddit_id_one, subreddit_id_two)

	

	





if __name__ == '__main__':

	print "\nHello Mr Programmer, I'm running..\n"

	t1 = datetime.now()



	with conn:

		cur.execute("""

			SELECT  id

			FROM subreddits

			"""

			)
		bla =  [item[0] for item in cur.fetchall()]

		it = combinations(bla, 2)


		print "\nfirst SQL Query finished..\n"

		k = 0
		

		best_results = []#Queue.PriorityQueue(maxsize=10)

		while k<3:

			try:

				p = Pool(100)
				args = [next(it) for i in xrange(400)]
				print args[0]
				result = p.map(comon_author_in_subreddits, args)
				args = []

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