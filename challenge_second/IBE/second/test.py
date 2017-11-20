#Two subreddits have an author in common if the author has made a 
#comment on threads in both subreddits.
#Show the 10 subreddit pairs with most authors in common and how 
#many authors they have in common.
import sqlite3
import heapq
from datetime import datetime
from multiprocessing import Pool


conn = sqlite3.connect('/Users/helga/OneDrive/Documents/ToolsForBigD/challenge2/reddit.db')
conn.text_factory = str
cur = conn.cursor()

def comon_author_in_subreddits(ids):
	
	author_id, subreddit_id = ids
		
	


#SELECT DISTINCT t1.orderID, t2.orderID, COUNT(*)
#FROM Orders t1
#WHERE t1.orderID <> ?
#AND ? < t1.orderID
#AND t1.customerID = ??
#GROUP BY t1.customerID, ??
#ORDER BY COUNT(*)
	

	cur.execute(""" 
			SELECT author_id, subreddit_id, ?
			FROM comments
			WHERE subreddit_id <> ?
			AND  subreddit_id < ?
			AND  author_id = ?

			"""
			,(subreddit_id, subreddit_id, subreddit_id, author_id))

	#print cur.fetchall()
		
	res = cur.fetchone()

	if res != []:
		#count_aouthor, subreddit_id, subreddit_id2 =  res
		return  res
	else:
		return (0,0,0)
	

if __name__ == '__main__':
	print "\nHello Mr Programmer, I'm running..\n"
	t1 = datetime.now()
	with conn:
		cur.execute(""" 
			SELECT DISTINCT  author_id, subreddit_id  
			FROM comments 
			"""
			)

		print "\nfirst SQL Query finished..\n"

		k = 0
		queue = []
		while k< 3: 
			p = Pool(1)
			result = p.map(comon_author_in_subreddits, cur.fetchmany(2))
			for i in result:
				heapq.heappush(queue, i)
			#comon_author_in_subreddits(cur.fetchall())
			p.close()
			p.join()
		
		
		t2 = datetime.now()
		result_for_file = []
		

		# print nice result
		# print
		# for i in sorted(result, reverse = True)[:10]:
		# 	print i
		# 	result_for_file.append(str(i[0]) +"     " + str(i[1])+"     " + str(i[2]))

		for i in heapq.nlargeset(10, queue):
			print i

		print 'Time:', t2-t1

		# file = open("big_tools_res_ex2","w") 

		# file.write("the time was: {}".format(t2-t1)) 
		# file.write("\n") 
		# for res in result_for_file:
		# 	file.write(res + "\n") 
		 
		 
		# file.close()

		print "\nGod by Mr Programmer, I'm Done..\n"


