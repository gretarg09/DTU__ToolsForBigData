import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

f = open( 'list_of_points' , 'r')

X = []
Y = []

for line in f:
    # The method strip() returns a copy of the string in which all chars have been stripped from the beginning 
    #   and the end of the string 
    line = line.strip()
    # Split the line on ' ' and capture the result in the variables x and y
    x,y = line.split(' ')
    X.append(float(x))
    Y.append(float(y))

# Use numpy.polyfit to fit polynomial of degree 3
#  The function returns the polynomial coefficients, highest power first
z =  np.polyfit(np.array(X),np.array(Y),3)
# scipy.optimize.root

print "The polynomial is as follows: y = {} + {}*x + {}*x^2 + {}*x^3".format(z[-1],z[-2],z[-3],z[-4])

# Calculating the Y values for the polynomial
#   here we use anonymous function to calculate the Y values for each x
Y_poly = map((lambda x: z[-1] + x*z[-2] + x**2*z[-3] + x**3*z[-4]),X)

# Find the real roots of the polynomial by using fsolve
real_roots = fsolve((lambda x: z[-1] + x*z[-2] + x**2*z[-3] + x**3*z[-4]),0)
print "The real roots are: {}".format(real_roots)

# plot up the original coordinates
plt.plot(X,Y)

# plot up the polynomial coordiantes
plt.plot(X,Y_poly,'--',color='r')

# plot a zero line onto the graph to visualize the real roots
plt.plot(X,np.zeros(len(X)),color='g')

plt.title("Polynomial of degree 3")
plt.xlabel("X")
plt.ylabel("Y")
plt.margins(0.1,0.1)
plt.show()
