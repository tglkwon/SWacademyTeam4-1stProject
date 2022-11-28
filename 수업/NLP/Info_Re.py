# Bag-of-Words
# tokenizing/NLP/Normalization/Zipf - > Controlled BoW
# Documents-Terms Matrix (DTM) : query마다 bottle-neck이 생김
# Terms-Documents Matrix (TDM) : Space&Time Complexity를 줄여준다
# TDM의 다른 구현 형태 -> inverted Index

from operator import le
from os import listdir
import re
from unittest import result
from corpusRead import fileids

BoW  = list()
path = '../Data collecting/news'
D = fileids(path)
for file in D:
    with open(file) as fp:
        doc = fp.read()
        BoW.extend(doc.split())

# DTM
DTM = [[0 for _ in range(len(BoW))] for _ in range(len(D))]

for i, file in enumerate(D):
    with open(file) as fp:
        # Split, Stemming, Lemmatization
        for term in doc.split():
            DTM[i][BoW.index(term)] = 1

query = '민족 체험관'
searchResult = list()
for q in query.split(): # |query|
    for i, d in enumerate(DTM): # |D|
        for j, t in enumerate(d): # |V ㅌ d_i|
            if BoW.index(q) == j and t == 1:
                searchResult.append(i)
                break

# TDM
TDM = [[0 for _ in range(len(D))] for _ in range(len(BoW))]

for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        for term in doc.split():
            TDM[BoW.index(term)][i] = 1

searchResult = list()
for q in query.split(): # |query|
    for i, docList in enumerate(TDM[BoW.index(q)]): # |D|
        for d in docList: # |V ㅌ d_i|
            if d == 1:
                result.append(i)
        searchResult.append(result)


# TDM의 다른 구현 형태 -> inverted index
# 대용량의 텍스트 데이터를 효과적으로 연산하기 위한 구조
# python의 dictionary를 이용한 구조
TDM = dict()
for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        for term in doc.split():
            if term not in TDM:
                TDM[term] = list()
            TDM[term].append(i)

searchResult = list()
for q in query.split():
    searchResult.append(TDM[q])


# 다른 언어에서도 사용 가능한 방법 : Linked-list
TDM = dict() # K: Voca, V: POST 시작위치
POST = list() # linked-list
for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        for term in doc.split():
            pos = len(POST)
            POST.append((i,-1 if term not in TDM else TDM[term]))
            TDM[term] = pos

searchResult = list()
for q in query.split():
    pos = TDM[q]
    result = list()
    while pos > 0:
        i, pos = POST[pos]
        result.append(i)
    searchResult.append(result)