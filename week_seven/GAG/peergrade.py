import re
from mrjob.job import MRJob
from mrjob.step import MRStep

pickWord = re.compile(r"[\w']+")

class eulerTour(MRJob):
	def steps(self):
		return [
			MRStep(mapper=self.mapper,
					reducer=self.reducer_count_vertices),
			MRStep(reducer=self.reducer_is_euler_tour)
				]
	def mapper(self, key, line):
		for word in pickWord.findall(line):
			yield (word.lower(), 1)

	def reducer_count_vertices(self, key, values):
		yield "nodeEdgeCount", sum(values)%2

	def reducer_is_euler_tour(self, key , val):
		yield "uneven", sum(val)

if __name__ == '__main__':
	eulerTour.run()