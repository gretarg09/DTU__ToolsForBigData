import timeit

# Use the timeit module in python to time the exection of both a python and cython version of the same program
py = timeit.timeit('queries_GAG.main()', setup='import queries_GAG', number=1)
cy = timeit.timeit('queries_GAG_cython.main()', setup='import queries_GAG_cython', number=1)

print "The execution time of the python program was: {}".format(py)
print "The execution time of the cython program was: {}".format(cy)
print "The execution of the cython program was {} times faster".format(py/cy)