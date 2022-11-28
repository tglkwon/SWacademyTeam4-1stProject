import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

data = fetch_california_housing()
print(data.data[:,3], data.target)

import numpy as np

X = np.c_[np.ones(len(data.data)), data.data[:,3], np.power(data.data[:,3], 2),
          np.power(data.data[:,3], 3), np.power(data.data[:,3], 4), np.power(data.data[:,3], 5),]
# np.hstack((np.ones(len(data.data)).reshape(-1,1), data.data[:,].reshape(-1,1)))[:3]
# X.shape

theta = np.linalg.inv(X.T.dot(X)).dot(X.T.dot(data.target))

plt.scatter(data.data[:,3], data.target)
plt.scatter(data.data[:,3], X.dot(theta), color='r')
plt.show()


from math import exp, factorial, sqrt
X = np.arange(0.1, 3.1, 0.1)
Y = np.exp(X)


def taylor(x, N):
    a = 0
    result = 0.0
    for n in range(N):
        result += (exp(a)/factorial(n)) * ((x-a)**n)

    return result

_Y = list()
for x in X:
    _Y.append(taylor(x, 5))

plt.plot(X, Y)
plt.plot(X, _Y)
plt.show()

X1 = np.arange(0.0, 10.0, 0.1)
X2 = np.arange(0.0, 10.0, 0.1)

def rosnebrock(x1, x2):
    return (1-x1) ** 2 + 100 * (x2 - x1**2)**2

Y = list()
for x1, x2, in zip(X1, X2):
    Y.append(rosnebrock(x1, x2))

def x1_derivative(x1, x2):
    return -2*(1-x1) - 400*x1*(x2-x1**2)

def x2_derivative(x1, x2):
    return 200 * (x2 - x1**2)

theta = [(-1.3, 0.9)]
# x1_derivative(*X0), x2_derivative(*X0)

h = 0.01
for _ in range(2000):
    X0 = theta[-1]
    absf = sqrt(x1_derivative(*X0)**2 + x2_derivative(*X0)**2)
    theta.append((X0[0] - h * x1_derivative(*X0)/absf,
                X0[1] - h * x2_derivative(*X0) / absf))

print(theta[-1])
# plt.plot(X1, Y)
# plt.plot(X2, Y)
# plt.show()
