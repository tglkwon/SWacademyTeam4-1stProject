from nltk.tokenize import word_tokenize
from os import listdir
from corpusRead import fileids, ngram

path = '../Data collecting/news'
corpus = list()
for filePath in fileids(path):
    with open(filePath, encoding='utf8') as fp:
        corpus.append(fp.read())


BE = dict()
for doc in corpus:
    tokens = word_tokenize(doc)
    for token in tokens:
        l = len(token)
        for i in range(1,l):
            k = token[:i]
            if k in BE:
                BE[k] += 1
            else:
                BE[k] = 1


# print(BE['대'])
from math import log2, sqrt

entropy = 0.0
for k, v in BE.items():
    if k.startswith('대') and len(k) == 2:
        p = v/BE['대']
        entropy += (p * log2(p))

print('대', -entropy)

entropy = 0.0
for k, v in BE.items():
    if k.startswith('대통') and len(k) == 3:
        p = v/BE['대통']
        entropy += (p * log2(p))

print('대통', -entropy)

entropy = 0.0
for k, v in BE.items():
    if k.startswith('대통령') and len(k) == 4:
        p = v/BE['대통령']
        entropy += (p * log2(p))

print('대통령', -entropy)

entropy = 0.0
for k, v in BE.items():
    if k.startswith('대통령이') and len(k) == 5:
        p = v/BE['대통령이']
        entropy += (p * log2(p))

print('대통령이', -entropy)


##############################

cs = 0.0
for k,v in BE.items():
    if k.startswith('대'):
        p = v/BE['대']
        print(k, sqrt(p))
        
for token in ['대통', '대통령', '대통령실']:
    print(token, sqrt(BE[token]/BE['대']))    
