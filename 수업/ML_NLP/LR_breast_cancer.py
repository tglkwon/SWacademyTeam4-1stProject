import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
import numpy as np

data = load_breast_cancer()
X = data.data
Y = data.target

X = np.c_[np.ones(len(X)), X]

linearFn = lambda X,W:X.dot(W)
linearDerviFn = lambda X,Y,W:2*X.T.dot(Y-X.dot(W))

theta = np.random.rand(len(X[0]))
h = 1e-5
i = 200000
history = list()
for _ in range(i):
    v = linearDerviFn(X,Y,theta)
    u = v / np.linalg.norm(v)
    theta += h*u

    if _%1000 == 0:
        history.append(theta)

x1 = np.array([1, X[:, [1]].min()])
x2 = np.array([1, X[:, [1]].max()])

for x, y in zip(X, Y):
    plt.scatter(x[1], y, c='r' if linearFn(x, theta) > .5 else 'b', s=1)

for w in history:
    plt.plot([x1[1], x2[1]], [linearFn(x1,w[:2]), linearFn(x2,w[:2])], 'r-', alpha=.1)

plt.plot([x1[1], x2[1]], [linearFn(x1, theta[:2]), linearFn(x2,theta[:2])], 'r-')
plt.show()

### logistic regression
logisticFn = lambda X,W: 1/(1+np.exp(-X.dot(W)))
logisticDerviFn = lambda X,Y,W:X.T.dot(Y-logisticFn(X,W))

theta = np.random.rand(3)
h = 1e-5
i = 200000
history = list()
for _ in range(i):
    v = logisticDerviFn(X,Y,theta)
    u = v / np.linalg.norm(v)
    theta += h*u

    if _%1000 == 0:
        history.append(theta)

x1 = np.array([1, X[:, [1]].min()])
x2 = np.array([1, X[:, [1]].max()])

for x, y in zip(X, Y):
    plt.scatter(x[1], y, c='r' if logisticFn(x, theta) > .5 else 'b', s=1)

for w in history:
    plt.plot([x1[1], x2[1]], [logisticFn(x1,w), logisticFn(x2,w)], 'r-', alpha=.1)

plt.plot([x1[1], x2[1]], [logisticFn(x1, theta), logisticFn(x2,theta)], 'r-')
plt.show()