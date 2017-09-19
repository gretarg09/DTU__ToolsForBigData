import numpy as np

f = open ( 'matrix.txt' , 'r')
matrix = [ map(int,line.split(',')) for line in f if line.strip() != "" ]

print "The input matrix is: \n \n {} \n".format(np.matrix(matrix))

A = np.matrix(matrix)[:,:-1]
b = np.array(matrix)[:,-1]

print "The matrix A: \n \n {} \n".format(A)
print "The matrix B: \n \n {} \n".format(b)

x = np.linalg.solve(A, b)

print "The solution to the linear matrix equation is: \n \n {} \n".format(x)

# Check if the result make sense
print "DOES THE RESULT MAKE SENSE? \n"
#lets check the result by comparing the result of A.dot(x) to b
print "The result from A.dot(x) is: \n \n {} \n".format(A.dot(x))


# To check if the numbers in the two arrays are the same we created this funciton
# Re: Comparing floats for equality in Python
def feq(a,b):
    if abs(a-b)<0.00000001:
        return 1
    else:
        return 0

isTheSame = True
# Here we go through every float number in the result of the dot product A.dot(x)
#   we use np.nditer to iter through the array and then we use the function feq to check if the float numbers are equal
for i,number in enumerate(np.nditer(np.asarray(A.dot(x)))): 
    if feq(float(b[i]), float(number)) == 0:
        isTheSame = False
        break

if isTheSame:
    print "Which is the same as b"
else:
    print "Which is not the same as b"