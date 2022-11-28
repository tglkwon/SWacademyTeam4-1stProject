import matplotlib.pyplot as plt
import numpy as np

corpus = [
    "This little kitty came to play when I was eating at a restaurant.",
    "Merley has the best squooshy kitten belly.",
    "Google Translate app is incredible.",
    "If you open 100 tab in google you get a smiley face.",
    "Best cat photo I've ever taken.",
    "Climbing ninja cat.",
    "Impressed with google map feedback.",
    "Key promoter extension for Google Chrome."
]
# Tokenizing + Stopwords + Regularization => V => CV => Vectorizing

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re

stop = stopwords.open('english').read()
V = list()
for d in corpus:
    for t in word_tokenize(d):
        if t.lower() not in stop and \
            not re.search(r'[{}]+'.format(punctuation), t.lower()) and \
            len(t) > 3:
            V.append(t.lower())

V = set(V)

i2t = {i:t for i,t in enumerate(V)}
t2i = {t:i for i,t in enumerate(V)}

X = np.zeros((len(corpus), len(V)))

for i, d in enumerate(corpus):
    for t in word_tokenize(d.lower()):
        if t in V:
            j = t2i[t]
            X[i,j] += 1

X = X * np.log(len(corpus)/X.sum(axis=0))

from kMeans import Maximization
K = 2
C = X[np.random.choice(X.shape[0], K)]
# C = np.random.rand(K, len(V))

def Expectation(X, C):
    Rnk = np.zeros((X.shape[0], K))
    for i, x in enumerate(X):
        k = np.argmax(np.dot(C, x) / (np.linalg.norm(C, axis=1) * (np.linalg.norm(x))))
        Rnk[i,k] = 1
    return Rnk

SE = list()

for _ in range(10):
    Rnk = Expectation(X, C)

    se = 0.0
    for i, c in enumerate(C):
        se += np.linalg.norm(X[Rnk[:, i] == 1] - c)
        C[i] = Maximization(X[Rnk[:, i] == 1])
    SE.append(se)

plt.plot(SE)
print(SE[-1])
plt.show()

for c in C:
    print([(i2t[i], c[i]) for i in c.argsort()[::-1][:5]])

from wordcloud import WordCloud

path = 'C:\Windows\Fonts\AppleGothic.ttf'
wc = WordCloud(font_path=path, max_words=30, background_color='white', repeat=True)

for c in C:
    wc.generate_from_frequencies({i2t[i]:c[i] for i in c.argsort()[::-1][:5]})
    wc.to_image()
