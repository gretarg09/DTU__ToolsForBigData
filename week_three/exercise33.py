import exercise33_python
import exercise33_cython
import timeit

py = timeit.timeit('exercise33_python.calculate(10000)', setup='import exercise33_python', number=500)
cy = timeit.timeit('exercise33_cython.calculate(10000)', setup='import exercise33_cython', number=500)

print "The execution time of the python program was: {}".format(py)
print "The execution time of the cython program was: {}".format(cy)
print "The execution of the cython program was {} times faster".format(py/cy)