# Binary Classification
# Naive Bayes, KNN, Linear, Logisitic
# Precision / Recall / F1-score 측정
# Spam filtering -> complexity(Feature <= 잘 뽑고, 최대한 적게

import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
from math import log
from konlpy.tag import Kkma, Okt, Komoran
from sklearn.model_selection import GridSearchCV
from news_classify_NB import training_NB, testing_NB

kkma = Kkma()
okt = Okt()
komoran = Komoran()
grid = GridSearchCV()

from json import load
with open('spam_test.json') as fp:
    D = load(fp)

### NB
C = ['spam', 'ham']
V, Prior, CondProb = training_NB(C, D)
# nb_test = testing_NB(C, V, Prior, CondProb, '\n'.join())

plt.scatter(D[:,[0]], D[:,[1]], c='k', s=1)
plt.axhline(0, c='k')
Y = list()
bias = 0.0
variance = 0.0

for x in np.random.ranint(len(X), size=(100,2)):
    theta = np.linalg.inv()
    y = X[x].mean(axis=0)


g_hat = sum(Y)/len(Y)
print(bias, variance)