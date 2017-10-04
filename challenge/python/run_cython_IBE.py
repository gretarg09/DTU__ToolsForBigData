import timeit

pattern = '.main("or[0,10]or[0,10]or")'
#pattern = '.main("cats[0,10]are[0,10]to")'
#pattern = '.main("when[15,25]republic[15,25]along")'


# Use the timeit module in python to time the exection of both a python and cython version of the same program
cy_IBE = timeit.timeit('queries_IBE_cython' + pattern, setup='import queries_IBE_cython', number=1)


print "---------- GAG ----------"
print "The execution time of the cython program was: {}".format(cy_IBE)
