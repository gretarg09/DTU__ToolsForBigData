#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
import heapq
import re
import sys



class MRLargestVocabulary(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol

	def steps(self):
		return  [
			MRStep( mapper = self.mapper_get_vocabulary,
				    reducer = self.reducer_get_vocabulary_size ),
			MRStep( reducer = self.reducer_get_top_ten )
		]

	def mapper_get_vocabulary(self, _, line):
		symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

		body = line['body']
		subreddit = line['subreddit']

		body = body.lower()
		for sym in symbols:
			body = body.replace(sym, " ")

		words = set()
		for w in body.split(" "):
			if len(w.replace(" ","")) > 0:
				yield subreddit, w


	def reducer_get_vocabulary_size(self,key,value):
		#print key, len(set(value))
		yield None, (key, len(set(value)))
		
	def reducer_get_top_ten(self,key,value):
		yield None, heapq.nlargest(10, value, key=lambda x:x[1])


if __name__ == '__main__':
    MRLargestVocabulary.run()