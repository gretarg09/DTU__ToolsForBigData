import preproc_python
import preproc_cython
import timeit

# Use the timeit module in python to time the exection of both a python and cython version of the same program
py = timeit.timeit('preproc_python.__main__()', setup='import preproc_python', number=1)
cy = timeit.timeit('preproc_cython.__main__()', setup='import preproc_cython', number=1)

print "The execution time of the python program was: {}".format(py)
print "The execution time of the cython program was: {}".format(cy)
print "The execution of the cython program was {} times faster".format(py/cy)