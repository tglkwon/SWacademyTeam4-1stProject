from nltk.tokenize import sent_tokenize
from konlpy.tag import Okt
from corpusRead import fileids, ngram

path = '../Data collecting/news'
corpus = list()
for filePath in fileids(path):
    with open(filePath, encoding='utf8') as fp:
        corpus.append(fp.read())

posTagger = Okt()
textList = list()
for doc in corpus:
    sentList = list()
    for sent in sent_tokenize(doc):
        sentList.append(posTagger.pos(sent))
    textList.append(sentList)

# len(set([_[0]+'/'+_[1] for _ in textList])), sum([len(_) for _ in textList])

ngram1 = dict()
ngram2 = dict()
ngram3 = dict()

# [('형태소', '품사'), ...] : 형태소+품사 언어
for doc in textList:
    for gram in ngram(doc):
        if gram in ngram1:
            ngram1[gram] += 1
        else:
            ngram1[gram] = 1

for doc in textList:
    for gram in ngram([_[0] for _ in doc]):
        if gram in ngram2:
            ngram2[gram] += 1
        else:
            ngram2[gram] = 1

for doc in textList:
    for gram in ngram([_[0] for _ in doc]):
        if gram in ngram3:
            ngram3[gram] += 1
        else:
            ngram3[gram] = 1

list(sorted(ngram1.items(), key=lambda _:_[1], reverse=True))[:10]

# findUniFreq = lambda t:filter(lambda  _:_[0] == t, filter(lambda _:_[0][0] = t, ngram2.item)
# findBiFreq = lambda t:filter(lambda  _:_[0] == t, filter(lambda _:_[0][1] = t, ngram2.item)

ujUni = dict()
ujBi = dict()
for doc in corpus:
    for s in list(doc):
        if s in ujUni:
            ujUni[s] += 1
        else:
            ujUni[s] = 1

    for b in ngram(list(doc)):
        if ''.join(b) in ujBi:
            ujBi[''.join(b)] += 1
        else:
            ujBi[''.join(b)] = 1

print(len(ujUni), len(ujBi), sum(ujUni.values()), sum(ujBi.values()))

keys = ['대',]
N = 5
for _ in range(10):
    key = keys.pop(0)
    candidates = dict()
    keyCount = ujUni[key]
    for k,v in ujBi.items():
        if k[0] == key:
            if k in candidates:
                candidates[k] += v
            else:
                candidates[k] = v
    i = 0
    for k,v in dict(sorted(candidates.items(), key=lambda r:r[1], reverse=True)).items():
        print(k, v/keyCount)
        i += 1
        if i > N:
            break
