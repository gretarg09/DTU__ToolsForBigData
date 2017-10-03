import timeit

pattern = '.main("or[0,10]or[0,10]or")'
#pattern = '.main("cats[0,10]are[0,10]to")'
#pattern = '.main("when[15,25]republic[15,25]along")'


# Use the timeit module in python to time the exection of both a python and cython version of the same program
py_GAG = timeit.timeit('queries_GAG' + pattern, setup='import queries_GAG', number=1)
cy_GAG = timeit.timeit('queries_GAG_cython' + pattern, setup='import queries_GAG_cython', number=1)

py_IBE = timeit.timeit('queries_IBE' + pattern, setup='import queries_IBE', number=1)
cy_IBE = timeit.timeit('queries_IBE_cython' + pattern, setup='import queries_IBE_cython', number=1)

print "---------- GAG ----------"
print "The execution time of the python program was: {}".format(py_GAG)
print "The execution time of the cython program was: {}".format(cy_GAG)
print "The execution of the cython program was {} times faster".format(py_GAG/cy_GAG)

print"---------- Ingvar ----------"
print "The execution time of the python program was: {}".format(py_IBE)
print "The execution time of the cython program was: {}".format(cy_IBE)
print "The execution of the cython program was {} times faster".format(py_IBE/cy_IBE)