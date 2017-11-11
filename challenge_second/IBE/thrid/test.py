import sqlite3
from datetime import datetime
import multiprocessing 
import multiprocessing.pool


conn = sqlite3.connect('/Users/helga/OneDrive/Documents/ToolsForBigD/challenge2/reddit.db')
conn.text_factory = str
cur = conn.cursor()

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)



class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess




def query_comment_threads(id):
	print "hhhaaaallliiii"
	return 'ingvar'
	


def query_subreddit(subreddit_id):
	print "query_subredditer"
	num_processes = 32
	p_subreddit = multiprocessing.Pool(num_processes)
	results = p_subreddit.map(query_comment_threads, range(num_processes))
	p_subreddit.close()
	p_subreddit.join()
	return 'Noner'



if __name__ == '__main__':
	print "\nHello Mr Programmer, I'm running..\n"
	t1 = datetime.now()
	with conn:
		cur.execute(""" 
			SELECT id  
			FROM subreddits
			limit 10
			"""
			)

	#print len(cur.fetchall())

	p = MyPool(64)
	result = p.map(query_subreddit, range(5))

	p.close()
	p.join()


	t2 = datetime.now()
	print "The time is {}".format(t2-t1)