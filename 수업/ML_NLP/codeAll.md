import numpy as np

# OR, AND, NOR, NAND
X = np.array([[0,0], 
              [0,1], 
              [1,0], 
              [1,1]])
Y_OR = np.array([0,1,1,1])
Y_AND = np.array([0,0,0,1])
Y_NOR = np.array([1,0,0,0])
Y_NAN = np.array([1,1,1,0])

X = np.c_[np.ones(len(X)), X] 

optimizedTheta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y_OR)

theta = np.random.rand(3)

optimizedTheta, theta

linearFn = lambda X,W:X.dot(W)
#                    (d,3) (3,)
linearDerivFn = lambda X,Y,W:2*X.T.dot(Y-X.dot(W))
#                             (3,4)   (4,)    (4,)

h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y_OR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(theta)

optimizedTheta, theta, len(history)

import matplotlib.pyplot as plt

for b,x1,x2 in X:
    plt.scatter(x1,x2, c='r' \
                if linearFn(np.array([b,x1,x2]), theta) > .5 \
                else 'b')
theta

----

logisticFn = lambda X,W:1/(1+np.exp(-X.dot(W)))
logisticDerivFn = lambda X,Y,W:X.T.dot(Y-logisticFn(X,W))
#                             (3,4)   (4,4)

theta = np.random.rand(3)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y_OR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(theta)

for b,x1,x2 in X:
    plt.scatter(x1,x2, c='r' \
                if logisticFn(np.array([b,x1,x2]), theta) > .5 \
                else 'b')
theta

----

from sklearn import datasets

data = datasets.load_breast_cancer()

X = data.data[:,0]
Y = data.target

X = np.c_[np.ones(len(X)), X]

X.shape, Y.shape

plt.scatter(X[:,[1]], Y)

theta = np.random.rand(2)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%10000 == 0:
        history.append(theta)

x1 = np.array([1, X[:,[1]].min()])
x2 = np.array([1, X[:,[1]].max()])

for x,y in zip(X, Y):
    plt.scatter(x[1], y, c='red' if linearFn(x,theta) > .5 else 'blue', s=1)

for w in history:
    plt.plot([x1[1], x2[1]], [linearFn(x1,w), linearFn(x2,w)], 'r-', alpha=.1)
plt.plot([x1[1], x2[1]], [linearFn(x1,w), linearFn(x2,w)], 'r-')

theta = np.random.rand(2)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%10000 == 0:
        history.append(theta)

x1 = np.array([1, X[:,[1]].min()])
x2 = np.array([1, X[:,[1]].max()])

for x,y in zip(X, Y):
    plt.scatter(x[1], y, c='red' if linearFn(x,theta) > .5 else 'blue', s=1)

----

# OR, AND, NOR, NAND
X = np.array([[0,0], 
              [0,1], 
              [1,0], 
              [1,1]])
Y_OR = np.array([0,1,1,1])
Y_AND = np.array([0,0,0,1])
Y_NOR = np.array([1,0,0,0])
Y_NAN = np.array([1,1,1,0])

X = np.c_[np.ones(len(X)), X]

linearLossFn = lambda X,Y,W:np.linalg.norm(Y-linearFn(X,W))

theta = np.random.rand(3)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y_OR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(X, Y_OR, theta))

plt.plot(history)

logisticLossFn = lambda X,Y,W:Y[Y==1].dot(np.log(logisticFn(X[Y==1],W)))\
                    +(1-Y[Y==0]).dot(np.log(1-logisticFn(X[Y==0], W)))

theta = np.random.rand(3)
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y_OR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(X, Y_OR, theta))

plt.plot(history)

----

AND, NOR, NAND를 Linear, Logistic으로 해보고, 되도록 그림도 그려보고

# OR, AND, NOR, NAND
X = np.array([[0,0], 
              [0,1], 
              [1,0], 
              [1,1]])
Y_OR = np.array([0,1,1,1])
Y_AND = np.array([0,0,0,1])
Y_NOR = np.array([1,0,0,0])
Y_NAN = np.array([1,1,1,0])

X = np.c_[np.ones(len(X)), X]

theta = np.random.rand(3)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y_AND, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(X, Y_AND, theta))

plt.plot(history)

theta = np.random.rand(3)
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y_AND, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(X, Y_AND, theta))
        
plt.plot(history)

theta = np.random.rand(3)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y_NOR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(X, Y_NOR, theta))

plt.plot(history)

theta = np.random.rand(3)
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y_NOR, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(X, Y_NOR, theta))
        
plt.plot(history)

theta = np.random.rand(3)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y_NAN, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(X, Y_NAN, theta))

plt.plot(history)

theta = np.random.rand(3)
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y_NAN, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(X, Y_NAN, theta))
        
plt.plot(history)

----

cancer 데이터를 x의 특정한 feature가 아닌 x 전체에 대해 fitting 해보기

data = datasets.load_breast_cancer()
X = data.data[:,0]
Y = data.target
X = np.c_[np.ones(len(X)), X]
X.shape, Y.shape

theta = np.random.rand(2)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%10000 == 0:
        history.append(linearLossFn(X, Y, theta))

plt.plot(history)

theta = np.random.rand(2)
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%10000 == 0:
        history.append(-logisticLossFn(X, Y, theta))

plt.plot(history)

----

#### => 스팸 분류 적용

D = [
    (1, "Chinese Beijing Chinese", True),
    (2, "Chinese Chinese Shanhai", True),
    (3, "Chinese Macao", True),
    (4, "Tokyo Japan Chinese", False)
]

T = [
    (5, "Chinese Tokyo Japan")
]

# Controlled V
V = list(set('\n'.join([d[1].lower() for d in D]).split()))

len(V), V

X = np.zeros((len(D), len(V)))
Y = np.zeros(len(D))

X.shape, Y.shape

for i,d in enumerate(D):
    for t in d[1].lower().split():
        j = V.index(t)
        X[i][j] += 1
    Y[i] = 1 if d[-1] else 0

X, Y

binX = X.copy()

binX[binX > 0] = 1

X, binX

X = np.c_[np.ones(len(D)), X]
binX = np.c_[np.ones(len(D)), binX]

X, binX

theta = np.random.rand(binX.shape[-1])
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(binX, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(binX, Y, theta))

plt.plot(history)

x = np.zeros(X.shape[-1])

x[0] = 1

for t in T[0][1].lower().split():
    j = V.index(t)
    x[j+1] += 1

x

linearFn(x, theta) > .5

theta = np.random.rand(binX.shape[-1])
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(X, Y, theta))

plt.plot(history)

linearFn(x, theta) > .5

----

theta = np.random.rand(binX.shape[-1])
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(binX, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(binX, Y, theta))
        
plt.plot(history)

logisticFn(x, theta) > .5

theta = np.random.rand(binX.shape[-1])
h = 1e-5
i = 2000000

history = list()

for _ in range(i):
    v = logisticDerivFn(X, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(-logisticLossFn(X, Y, theta))
        
plt.plot(history)

logisticFn(x, theta) > .5

----

TF-IDF

# TF: freq/maxfreq
# IDF: log(N/n)
# weight = TF * IDF
weightedX = (X.T/X.sum(axis=1)).T * np.log(len(D)/binX.sum(axis=0))

weightedX = np.c_[np.ones(len(D)), weightedX]

weightedX.shape, X.shape, binX.shape

theta = np.random.rand(weightedX.shape[-1])
h = 1e-5
i = 200000

history = list()

for _ in range(i):
    v = linearDerivFn(weightedX, Y, theta)
    u = v/np.linalg.norm(v)
    theta = theta + h*u
    
    if _%1000 == 0:
        history.append(linearLossFn(weightedX, Y, theta))

plt.plot(history)