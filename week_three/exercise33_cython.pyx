from __future__ import division

# Cython function to calculate the sum 1/1^2 + 1/2^2 + 1/3^2 + ... + 1/10000^2
def calculate(n):
    cdef float sum = 0.0 #static type declaration
    cdef int i = 0 # static type declarations of the iterator variable
    for i in range(1,n+1):
        sum += 1/(i**2)
    return sum