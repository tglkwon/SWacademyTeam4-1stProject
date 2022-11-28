from os import listdir
import re
from nltk.tokenize import sent_tokenize
from konlpy.tag import Komoran
from struct import pack, unpack
from math import sqrt, log

ma = Komoran()

## Data collecting에서 모든 데이터 불러오기
path = '../Data collecting/news'
def fileids(path, ext='txt'):
    fileList = list()
    path = path if path[-1] == '/' else path + '/'
    for fileName in listdir(path):
        if fileName.endswith(ext):
            fileList.append(path + fileName)
    return fileList

D = fileids(path)

## token, feature 추출하기
def featureExtractor(file, query=None):
    terms = list()
    if query is None:
        with open(file, encoding='utf-8') as fp:
            doc = fp.read()
    else:
        doc = query

    doc = re.sub(r'\s{2,}', ' ', doc)

    # 어절
    tokens = doc.split()
    terms.extend(tokens)

    # 음절
    for token in tokens:
        terms.extend(list(token))

    # 바이그램 - 어절
    for i in range(len(tokens) - 1):
        terms.append(' '.join(tokens[i:i + 2]))

    # 바이그램 - 음절
    for token in tokens:
        for i in range(len(token) - 1):
            terms.append(''.join(token[i:i + 2]))

    # 형태소
    for sentence in sent_tokenize(doc):
        sentence = sentence.strip()
        if len(sentence) > 1:
            terms.extend(ma.morphs(sentence))

    # 명사
    for sentence in sent_tokenize(doc):
        sentence = sentence.strip()
        if len(sentence) > 1:
            terms.extend(ma.nouns(sentence))

    # 분절(Branch-entropy, Cohesion Score, BPE)
    # 구(Phrase)

    return terms

## feature들 중 Zipf's law에 따른 stopwords, 조사, 문법적 역할을 하는 단어 등 제거하기
def featureSelection(terms):
    termsDict = dict()

    for term in terms:
        if term in termsDict:
            termsDict[term] += 1
        else:
            termsDict[term] = 1

    N = sum(termsDict.values())
    ratio = 0.0

    # 저빈도 < ratio 삭제
    cFreq = 0
    for k, v in sorted(termsDict.items(), key=lambda kv: kv[1]):
        if cFreq / N > ratio:
            break

        cFreq += v
        # Edit Distance > threshold 이면 삭제
        del termsDict[k]

    # 고빈도 > ratio 삭제
    cFreq = 0
    for k, v in sorted(termsDict.items(), key=lambda kv: kv[1], reverse=True):
        if cFreq / N > ratio:
            break

        cFreq += v
        del termsDict[k]

    return termsDict

## 본격적 TDM 만들기. globalTDM은 모든 문서의 단어들을 담는 dictionary
globalTDM = dict()
## TDM을 담을 file 생성하기
fp = open('globalPOST.dat', 'wb')
fp.close()

## 실제 news 파일을 읽어서 TDM을 만드는 부분
for i, file in enumerate(D):
    ## localTDM은 한 문서 안의 단어들을 담는 dictionary
    localTDM = featureSelection(featureExtractor(file))

    with open('globalPOST.dat', 'ab') as fp:
        for k, v in localTDM.items():
            if k in globalTDM:
                pos = globalTDM[k]
                postData = (i, v, pos)
                newpos = fp.tell()
                fp.write(pack('iii', *postData))
                globalTDM[k] = newpos
            else:
                postData = (i, v, -1)
                pos = fp.tell()
                fp.write(pack('iii', *postData))
                globalTDM[k] = pos


print('\nTDM end')
# TF-IDF 정의하기
K = 0.5
N = len(D)

TF = lambda freq, maxfreq, K: K+(1-K)*(freq/maxfreq)
IDF = lambda df, N:log(N/df)

# DocDictionary? 구할 때, maxFreq, docLength
maxfreqDict = dict()
for term, pos in globalTDM.items(): # 단어:위치
    with open('globalPOST.dat', 'rb') as fp:
        while pos > -1: # 처음위치 일 때까지 반복(-1)
            fp.seek(pos) # 위치 조정
            docID, freq, pos = unpack('iii', fp.read(12))
            if docID not in maxfreqDict:
                maxfreqDict[docID] = freq
            if freq > maxfreqDict[docID]:
                maxfreqDict[docID] = freq
# 문서 내 maxFreq만을 위한

fp = open('weightPOST.dat', 'wb')
fp.close()

print('maxfreq end')

weightTDM = dict()
docLength = dict()
for t, pos in globalTDM.items():
    tfList = list()

    with open('globalPOST.dat', 'rb') as fp:
        while pos > -1:
            fp.seek(pos)
            i, freq, pos = unpack('iii', fp.read(12))
            tfList.append((i, TF(freq, maxfreqDict[i], K)))

    df = len(tfList)
    idf = IDF(df, N)

    with open('weightPOST.dat', 'ab') as fp:
        weightTDM[t] = (df, fp.tell())
        for i, tf in tfList:
            fp.write(pack('if', *(i, tf*idf)))
            if i not in docLength:
                docLength[i] = 0.0
            docLength[i] += (tf*idf) ** 2

print('\nTF-IDF end')
#@@ TDM to DTM
DTM = dict()
for t, (df, pos) in weightTDM.items():  # 단어:(문서빈도,위치)
    with open('weightPOST.dat', 'rb') as fp:
        i = 0
        while i < df:
            fp.seek(pos + (i * 8))
            docID, weight = unpack('if', fp.read(8))
            i += 1

            if docID not in DTM:
                DTM[docID] = dict()

            DTM[docID][t] = weight

print('\nTDM to DTM end')
# euclidean distance 구하기
# queryVector = list()
# qterms = dict()
# for t in ma.morphs('윤석열 대통령은 김건희와 미국에 다녀왔다.'):
#     if t not in qterms:
#         qterms[t] = 1
#     else:
#         qterms[t] += 1
qterms = featureSelection(featureExtractor(D[0]))

queryVector = dict()
maxFreq = max(qterms.values())
for t, f in qterms.items():
    queryVector[t] = TF(f, maxFreq, 0) * IDF(weightTDM[t][0], N)

print('euclidean distance start')
eucDist = dict()
for docID, weights in DTM.items():
    # 벡터 구성은 차원 전체 (Controlled) Vocabulary t ㅌ V
    # weight가 특정 doc의 가중치 벡터
    for t, (df, pos) in weightTDM.items():  # 모든 단어를에 대해
        dv = weights[v] if v in weights else 0.0
        qv = queryVector[v] if v in queryVector else 0.0

        if docID not in eucDist:
            eucDist[docID] = 0.0

        eucDist[docID] += (qv - dv) ** 2

    eucDist[docID] = sqrt((eucDist[docID]))

print('euclidean distance end')
# cosine similarity 구하기
queryVL = sqrt(sum(map(lambda row: row[1]**2, queryVector.items())))

candidates = dict()
for t, w1 in queryVector.items():
    df, pos = weightTDM[t]
    with open('weightPOST.dat', 'rb') as fp:
        i = 0
        while i < df:
            fp.seek(pos+(i*8))
            docID, w2 = unpack('if', fp.read(8))

            if docID not in candidates:
                candidates[docID] = 0.0

            candidates[docID] += w1*w2  # 내적

            i += 1


for docID, ip in candidates.items():
    candidates[docID] = ip/(queryVL*sqrt(docLength[docID]))

print('\ncalc end')


########## ML_NLP 의 KNN을 돌려본 부분
import re

K = 7
result = dict()

for docID, cosSim in sorted(candidates.items(), key=lambda r:r[1], reverse=True)[:K]:
    className = re.search(r'(\d{3})-', D[docID]).group(1)
    if className in result:
        result[className][0] += 1
        result[className][1] += 1
    else:
        result[className] = [1, cosSim]


for k,v in result.items():
    print(k, v, v[1]/v[0], v[0]/K)