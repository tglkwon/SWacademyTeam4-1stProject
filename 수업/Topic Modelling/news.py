from os import listdir
import numpy as np
from konlpy.tag import Okt
import re
from nltk.tokenize import sent_tokenize
# from kMeans_corpus import Expectation, Maximization
import matplotlib.pyplot as plt

ma = Okt()

def fileids(path, ext='txt'):
    fileList = list()
    path = path if path[-1] == '/' else path + '/'
    for fileName in listdir(path):
        if fileName.endswith(ext):
            fileList.append(path + fileName)

    return fileList

D = fileids('../Data collecting/news')

DTM = dict()
for i, d in enumerate(D):
    DTM[i] = dict()
    with open(d, encoding='utf-8') as fp:
        content = fp.read()
        ctext = re.sub(r'[^0-9가-힣.]+', ' ', content)
        ctext = re.sub(r'\s+', ' ', ctext)
        ctext = re.sub(r'(?:^|[ ])[0-9가-힣.](?:[ ]|$)', ' ', ctext)

        for s in sent_tokenize(ctext):
            for noun in ma.nouns(s.strip()):
                if noun not in DTM[i]:
                    DTM[i][noun] = 0
                DTM[i][noun] += 1

# print(ctext)

V = list()
for i, termList in DTM.items():
    V.extend(termList.keys())

V = set(V)

i2t = {i: t for i, t in enumerate(V)}
t2i = {t: i for i, t in enumerate(V)}

X = np.zeros((len(D), len(V)))

def Expectation(X, C):
    Rnk = np.zeros((X.shape[0], K))
    for i, x in enumerate(X):
        # 거리
        k = np.argmin(np.linalg.norm(C - x, axis=1))
        # cosine similarity
        # k = np.argmax(np.dot(C, x)/(np.linalg.norm(C, axis=1)*np.linalg.norm(x)))
        Rnk[i, k] = 1

    return Rnk

def Maximization(X_c):
    return np.average(X_c, axis=0)


for i, termList in DTM.items():
    for t, freq in termList.items():
        j = t2i[t]
        X[i,j] = freq

# TF
TF = X.T/np.max(X, axis=1)
TF = TF.T
# IDF
IDF = np.log(len(D)/np.sum(X, axis=0))

wX = TF * IDF

Topics = list()
for K in range(3,10):
# K = 2
# Clusters =  np.random.choice(len(D), K)
    C = wX[np.random.choice(len(D), K)]
    SE = list()

    for _ in range(10):
        Rnk = Expectation(X, C)

        se = 0.0
        for i, c in enumerate(C):
            se += np.linalg.norm(X[Rnk[:, i] == 1] - c)
            C[i] = Maximization(X[Rnk[:, i] == 1])
        SE.append(se)
    Topics.append(C)


for topic in Topics:
    print('K=', len(topic))
    for t in topic:
        for i in np.argsort(t)[::-1][:10]:
            print(i2t[i], t[i])
        print('=============')
plt.plot(SE)
plt.show()

u,s,vt = np.linalg.svd(X)
for K in range(2,11):
    print(K)
    idx = np.arsort(s*s.T)[:,::-1][:,:10]
    svt = vt[:K].T*s
    for i in range(idx.shape[0]):
        print('Topic', 1+i)
        # print([i2t[j] for j in ])