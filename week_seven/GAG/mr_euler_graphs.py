#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import sys


# In this solution we use the fact that a multiple even numbers added to gether results in an even number

class MRIsEulerGraph(MRJob):

	def steps(self):
		return  [
			MRStep( mapper = self.mapper_get_edges,
				    reducer = self.reducer_check_degree ),
			MRStep( reducer = self.reducer_check_if_euler )
		]

	def mapper_get_edges(self, _, line):

		# For each node in and edge add one to the key
		for note in line.split():
			yield (note, 1)

	#def combiner_count_degree(self, key, values):

		# calculate the degree of the node
	#	yield (key, sum(values))


	def reducer_check_degree(self,key,value):

		# Check if the degree is even, if so add 1 to an array else add 0 to the same arre
		# send the array of 0's and 1's to the same reducer
		if sum(value) % 2 == 0:
			yield ("degree_array", 0)
		else:
			yield ("degree_array", 1)

	def reducer_check_if_euler(self,_, values):
		# if the sum of the values is equal to zero then we know that all of the nodes 
		# in the graph has even degree

		if sum(values) == 0:
			yield ("Answer:", "The graph is eular :)")
		else:
	 		yield ("Answer:", "The graph is not eular :(")

if __name__ == '__main__':
    MRIsEulerGraph.run()