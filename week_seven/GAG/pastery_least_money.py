from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import sys

class MinSale(MRJob):

	def mapping(self, _, line):
		data = line.strip().split(",")
		date, time, store, item, cost, payment = data
		yield (store,time), int(cost)

	def combining(self, key, values):
		 
		# we need to store the sum values since it is a generator
		sum_val = sum(values)
		
		# split up the time between hour and minutes
		hour, minutes = key[1].split(':')

		# find how many minutes have past from the day
		total_min =  int(hour) * 60  + int(minutes)
		
		# 8 o'clock in minutes
		prior_time = 128 

		# 11 o'clock in minutes
		latter_time = 660 

		# between 8 and 11 who sold more than 1 item
		if total_min > 128 and total_min < 660 and sum_val > 0:
			yield key[0], sum_val 

	def prior_reducing(self, key, values):
		yield None, (sum(values), key)

	def latter_reducing(self, key, values):
		yield min(values)

	def steps(self):
		return  [
			MRStep( mapper = self.mapping,
				    combiner = self.combining,
				    reducer = self.prior_reducing),
			MRStep( reducer = self.latter_reducing )
		]


if __name__ == '__main__':
	MinSale.run()


