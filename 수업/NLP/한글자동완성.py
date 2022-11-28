from corpusRead import fileids, ngram
from 음절 import uni2tri
import BytePair

path = '../Data collecting/news'
corpus = list()
for filePath in fileids(path):
    with open(filePath, encoding='utf8') as fp:
        corpus.append(fp.read())

# corpus to data
data = dict()
for news in corpus:
    for letters in news.split():
        if letters in data:
            data[tuple(letters)] += 1
        else:
            data[tuple(letters)] = 1

# bytepair by 한글
keyCand = dict()
for k,v in data.items():
    for bi in ngram(k):
        if bi in keyCand:
            keyCand[bi] += v
        else:
            keyCand[bi] = v


import re
merge = max(keyCand, key=keyCand.get)
mergeData = dict()
for k,v in data.items():
    newK = re.sub(' '.join(merge), ''.join(merge), ' '.join(k))
    mergeData[tuple(newK.split())] = v
