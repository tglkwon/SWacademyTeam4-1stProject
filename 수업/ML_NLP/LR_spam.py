import numpy as np
import matplotlib.pyplot as plt

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

X = np.zeros(len(D), len(V))
Y = np.zeros(len(D))

for i, d in enumerate(D):
    for t in d[1].lower().split():
        j = V.index(t)
        X[i][j] += 1
    Y[i] = 1 if d[-1] else 0

binX = X.copy()
binX[binX > 0] = 1

X = np.c_[np.ones(len(D)), X]
binX = np.c_[np.ones(len(D)), binX]

linearFn = lambda X,W:X.dot(W)
linearDerivFn = lambda X,Y,W:2*X.T.dot(Y-X.dot(W))
linearLossFn = lambda X,Y,W: np.linalg.norm(Y-linearFn(X,W))

x = np.zeros(X.shape[-1])
for t in T[0][1].lower().split():
    j = V.index(t)
    x[j+1] += 1

## TF-IDF
# TF: x[1:]/x[1:].max()
# IDF: np.log(len(D)/binX[1:].sum(axis=0))
weightedX = (X.T/X.sum(axis=1)).T * np.log(len(D) / binX.sum(axis=0))
weightedX = np.c_[np.ones(len(D)), weightedX]
theta = np.random.rand(weightedX.shape[-1])
h = 1e-5
i = 20000

history = list()

for _ in range(i):
    v = linearDerivFn(weightedX, Y, theta)
    u = v / np.linalg.norm(v)
    theta = theta + h * u

    if _ % 1000 == 0:
        history.append(linearLossFn(weightedX, Y, theta))

plt.plot(history)