#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
import heapq
import re
import sys
import time



class MRLargestVocabulary(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol
	global symbols
	symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

	def steps(self):
		return  [
			MRStep( mapper_init =  self.init_top_vocabulary,
					mapper = self.mapper_get_vocabulary,
				    reducer = self.reducer_get_vocabulary_size ),
			MRStep( reducer = self.reducer_get_top_ten )
		]

	def init_top_vocabulary(self):
        self.top_vocabulary = {}

	def mapper_get_vocabulary(self, _, line):
	
		body = line['body']
		subreddit = line['subreddit']
		subreddit_id = line['subreddit_id']
		#symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

		body = body.lower()
		for sym in symbols:
			body = body.replace(sym, " ")

		for w in frozenset(body.split(" ")):
			if len(w.replace(" ","")) > 0:
				yield (subreddit,subreddit_id), w


	def reducer_get_vocabulary_size(self,key,words):
		#print key, len(set(value))
		uniq_words = {}
		for word in words:
			uniq_words.setdefault(word)

		yield (key, len(uniq_words))
		
	def reducer_get_top_ten(self,key,value):
		yield None, heapq.nlargest(10, value, key=lambda x:x[1])


if __name__ == '__main__':

    t0 = time.time()
    MRLargestVocabulary.run()
    t1 = time.time()

    print "The execution time was {}".format(t1-t0)