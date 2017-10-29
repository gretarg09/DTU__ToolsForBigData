#!/usr/bin/env python

from mrjob.job import MRJob
import re
import sys

# https://docs.python.org/3/library/re.html#re.compile
# explenations about re.compile can be found in the above link

WORD_RE = re.compile(r"[\w']+")

class MRWordOccurences(MRJob):
	def mapper(self,_,line):

		# yield each word in the line
		# could also use line.split() instead if using regex
		for word in WORD_RE.findall(line):
			yield (word.lower(), 1)

	def reducer(self, key, values):
		yield key, sum(values)


if __name__ == '__main__':
    MRWordOccurences.run()