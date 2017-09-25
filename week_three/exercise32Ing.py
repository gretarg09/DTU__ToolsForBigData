from scipy.optimize import minimize
import numpy as np

#get the data
matrix = np.loadtxt('points_ex3_scipy.txt', delimiter=" ")
x = matrix[:,0]
y = matrix[:,1]
    
x_values = np.array(x)
y_values = np.array(y)

# get the coefficiencts of the cubic function
fit = np.polyfit(x_values, y_values, 3)

# make a function which fits the data which is given to it
p = np.poly1d(fit)  

xo = [-3] # start the optimization algorithm at -3

res = scipy.optimize.fsolve(p, xo)
print "The root is at:",res

#verifying the solution
print "The roots of the fited function: ", np.roots(fit)

#lets plott upp the data points and the fitted data
plt.plot(x_values, y_values, "go", alpha = 0.3)
plt.plot(x_values, [p(x) for x in x_values], color = "black")
plt.plot(xo, res, '*', color = "red")
plt.title("The data and the polynomial fit ")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["data", "fit", "root"])
plt.show()
