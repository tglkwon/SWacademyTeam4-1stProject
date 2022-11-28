import numpy as np
import matplotlib.pyplot as plt

N = 100
X = np.random.rand(N,2)

X = np.r_[X, X+np.array([0,1.5])]
X = np.r_[X, X+np.array([1.5,0])]

K = 4
C = X[np.random.choice(N*4, K)]

def Expectation(X, C):
    Rnk = np.zeros((N * 4, K))
    for i, x in enumerate(X):
        # 거리
        # k = np.argmin(np.linalg.norm(C - x, axis=1))
        # cosine similarity
        k = np.argmax(np.dot(C, x)/(np.linalg.norm(C, axis=1)*np.linalg.norm(x)))
        Rnk[i, k] = 1

    return Rnk

def Maximization(X_c):
    return np.average(X_c, axis=0)


SE = list()
SC = list()
Cs = list()

Cs.append(C)

cm = ['r','g','b','c','m','y','k']
for _ in range(10):
    Rnk = Expectation(X, C)
    se = 0.0
    sc = 0.0
    for i, c in enumerate(C):
        se += np.linalg.norm(X[Rnk[:,i] == 1] - c)
        sc += np.sum(np.dot(X[Rnk[:,i] == 1], c)/(np.linalg.norm(c)*np.linalg.norm(X[Rnk[:,i] == 1], axis=1)))
        C[i] = Maximization(X[Rnk[:,i] == 1])

    SE.append(se)
    SC.append(sc)
    Cs.append(C)

    for i, c in enumerate(C):
        x_c = X[Rnk[:, i] == 1]
        plt.scatter(x_c[:, 0], x_c[:, 1], c=cm[i], alpha=.1)

    plt.scatter(C[:, 0], C[:, 1], c=cm[:K])
    plt.show()

plt.plot(SC)
plt.plot(SE)
plt.show()


