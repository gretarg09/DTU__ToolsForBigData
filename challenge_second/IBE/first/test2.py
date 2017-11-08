# The size of a vocabulary for a subreddit is defined as the total # number of distinct words is used in the comments of the 
# subreddit.

import sqlite3
import time
from multiprocessing import Process, Pool
import string
import numpy as np
from datetime import datetime


def SetReduce(sets, pointer, newComment, LastComment, maxSize):
	try:
		for word in newComment:
			sets[pointer].add(word)
		#sets[pointer]=sets[pointer].union(newComment)
	except:
		sets.append(set())
		#sets[pointer]=sets[pointer].union(newComment)
		for word in newComment:
			sets[pointer].add(word)
	if not LastComment:
		if len(sets[pointer])>maxSize:
			newComment=sets[pointer]
			sets[pointer]=set()
			return SetReduce(sets, pointer+1, frozenset(newComment), LastComment, maxSize*20)
		return sets
	if not len(sets)-1 == pointer:
		return SetReduce(sets, pointer+1, sets[pointer],LastComment,maxSize)

	return sets

def cleaner(comment):
	for word in comment:
		yield word


def setter():
	for word in set(comment.split()):
		# profa einhvad stae fall
		#print len(data)**1.0002 / len(data)
		if first_words < val:
			first_words.add(word)
			words.add(word)

		else:
		# print len(words)
			if word not in frozenset(first_words):
				words.add(word)
				yield  
			


con = sqlite3.connect('reddit.db')
con.text_factory = str
cur = con.cursor()

def query(subreddit_id):
	# make a querey search
	#subreddit_id,cur = subreddit_id 

	t1 = time.time()
	symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

	cur.execute(""" 
	SELECT DISTINCT body 
	FROM comments
	WHERE subreddit_id = ?
	""",
	subreddit_id)

	# Fetch the resulting data
	data = cur.fetchall()
	# here we will have all our unique words, except the first distrinct words
	all_words = set()
	all_words_naive = []# np.array([''], dtype = str)#[]
	words = set()
	first_words = set()
	sets=[set([])]
	new_words = set()
	x = []
	teljari = 1
	val = int(100*np.log(len(data) / np.log(len(data) + 1))) # nota log sem mappar mikid olinulegt nidur og reyni ad hafa
	for d in data:
		# extract the data of the tuple
		comment = d[0]

		# clean the data 
		comment = comment.lower()
		comment = comment.translate(string.maketrans("",""), string.punctuation)


	#====================== endurkvaemt
	# 	last_set = teljari == len(data)
	# 	sets=SetReduce(sets, 0, frozenset(comment.split()), last_set, 1000)
			
	# 	teljari += 1
	# words = sets[-1]
	

		#================= fyrsta draslid
		# x += comment.split()
		# if len(x) > 1000 or teljari == len(data):
		# 		#j = set(s.split(" "))
		# 	j = frozenset(x)
		# 	x = []
		# 	words = words.union(j)

		# 	for w in j:
		# 		#if len(w.replace(" ","")) > 0: # hanner ad splita a bilinu.. gerir ekkert
		# 		if w:
		# 			words.add(w)
		# teljari += 1




		# =================skoda fyrstu 700
		
		#medaltalid milli 50tus og 500tus comments sem toluna 1000
		# _comments = set(comment.split())
		# for word in set(_comments):
		# 	# profa einhvad stae fall
		# 	#print len(data)**1.0002 / len(data)
		# 	if len(first_words) < 700:
		# 		first_words.update(_comments)
		# 		words.update(_comments)
		# 		break

		# 	else:
		# 	# print len(words)
		# 		if word not in first_words:
		# 			words.add(word)
				



		# ============== Naive	
		#for word in set(comment.split()):
			#all_words_naive.append(word)
			#print len(all_words_naive)
			#all_words_naive = np.append(all_words_naive, word)
	#words = set(all_words_naive)
		all_words_naive += comment.split()
	#all_words_naive = np.array(all_words_naive)
	words = np.unique(all_words_naive)
	#words = set(all_words_naive)
		

	
	t2 = time.time()
	
	#print all_words
	#print words
	return (len(words), subreddit_id)




if __name__ == '__main__':


	with con:

		# Get the cursor object
		
		subreddit_nr = 0 #subreddit_nr var i..
		cur.execute("SELECT DISTINCT id FROM subreddits LIMIT 10")   #(%s, %s, %s)", (var1, var2, var3))
		
		
		#t3 = time.time()
		t3 = datetime.now()

		p = Pool(10)

		result = p.map(query, cur.fetchall())

		print result
		p.close()
		p.join()
		p.terminate()
		
		t4 = datetime.now()
		print
		for i in sorted(result, reverse = True)[:10]:
			cur.execute("select name from subreddits  where id = ?",i[1])
			print i, cur.fetchall()[0][0]



		# for d in cur.fetchall():

		# 	print query(d[0])
		#t4 = time.time()


		print "THe time", t4-t3
	



