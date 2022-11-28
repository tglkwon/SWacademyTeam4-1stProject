import matplotlib.pyplot as plt
import numpy as np

# OR, AND, NOR, NAND

X = np.array([[0,0],
              [0,1],
              [1,0],
              [1,1]])
Y_OR = np.array([0,0,1,1])
Y_AND = np.array([0,0,0,1])
Y_NOR = np.array([1,1,0,0])
Y_NAND = np.array([1,1,1,0])

X = np.c_[np.ones(len(X)), X]

optimizedTheta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y_OR)


linearFn = lambda X,W:X.dot(W)
linearDerviFn = lambda X,Y,W:2*X.T.dot(Y-X.dot(W))

lossFn = lambda X,Y,W: np.linalg.norm(Y-linearFn(X,W))

theta = np.random.rand(len(X[0]))
h = 1e-5
i = 200000
history = list()
for _ in range(i):
    v = linearDerviFn(X,Y_OR,theta)
    u = v / np.linalg.norm(v)
    theta += h*u

    if _%1000 == 0:
        # history.append(theta)
        history.append(lossFn(X,Y_OR,theta))

print(optimizedTheta, theta)

for b,x1,x2 in X:
    plt.scatter(x1,x2, c='r' if linearFn(np.array([b,x1,x2]), theta) > .5 else 'b')

plt.show()


logisticFn = lambda X,W: 1/(1+np.exp(-X.dot(W)))
logisticDerviFn = lambda X,Y,W:X.T.dot(Y-logisticFn(X,W))

logisticlossFn = lambda X,Y,W: Y[Y==1].dot(np.log(logisticFn(X[Y==1], W)))\
                                + (1-Y[Y==0]).dot(np.log(1-logisticFn(X[Y==0], W)))
theta = np.random.rand(3)
h = 1e-5
i = 200000
history = list()
for _ in range(i):
    v = logisticDerviFn(X,Y_OR,theta)
    u = v / np.linalg.norm(v)
    theta += h*u

    if _%1000 == 0:
        # history.append(theta)
        history.append(-logisticlossFn(X,Y_OR,theta))

plt.plot(history)
plt.show()

for b,x1,x2 in X:
    plt.scatter(x1,x2, c='r' if logisticFn(np.array([b,x1,x2]), theta) > .5 else 'b')

plt.show()
