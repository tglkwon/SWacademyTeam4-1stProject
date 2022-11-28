# Bag-of-Words[BoW] -> Indepent(N-Gram)
# Tokeninzing/NLP/Normalization/Zipf -> Controlled BoW
# Documents-Terms Matrix(DTM) : Query마다 Bottle-neck
# Terms-Documents Matrix(TDM) : Space&Time Complexity 줄여줌
# TDM의 다른 구현 형태 -> Inverted Index
from os import listdir
import re
from math import log

path = '../Data collecting/news'
def fileids(path, ext='txt'):
    fileList = list()
    path = path if path[-1] == '/' else path + '/'
    for fileName in listdir(path):
        if fileName.endswith(ext):
            fileList.append(path + fileName)
    return fileList


BoW = list()
for file in fileids(path):
    with open(file, encoding='utf-8') as fp:
        doc = fp.read()
        # Split, Stemming, Lemmatization, 어절, 음절, N-gram, BPE, ...
        BoW.extend(doc.split())

# len(BoW), len(set(BoW))
BoW = list(set(BoW))
# len(fileids(path)), len(BoW)
DTM = [[0 for _ in range(len(BoW))]
       for _ in range(len(fileids(path)))]
# len(DTM), len(DTM[0])

for i, file in enumerate(fileids(path)):
    with open(file, encoding='utf-8') as fp:
        doc = fp.read()
        # Split, Stemming, Lemmatization, 어절, 음절, N-gram, BPE, ...
        for term in doc.split():
            DTM[i][BoW.index(term)] = 1

# sum(DTM[0]), len(DTM[0])  # => Sparse 문제가 발생
query = '디지털 전환'
searchResult = list()
for q in query.split():  # |query|
    result = list()
    for i, d in enumerate(DTM):  # |D|
        for j, t in enumerate(d):  # |V ㅌ d_i|
            if BoW.index(q) == j and t == 1:
                result.append(i)
                break
    searchResult.append(result)

# set(searchResult[0]).intersection(set(searchResult[1]))
D = fileids(path)
TDM = [[0 for _ in range(len(D))]
       for _ in range(len(BoW))]
len(TDM), len(TDM[0])  # Transpose
for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        # Split, Stemming, Lemmatization, 어절, 음절, N-gram, BPE, ...
        for term in doc.split():
            TDM[BoW.index(term)][i] = 1

# sum(TDM[0]), sum(TDM[100])
searchResult = list()
for q in query.split():  # |query|
    result = list()
    for i, d in enumerate(TDM[BoW.index(q)]):  # |L|
        if d == 1:
            result.append(i)
    searchResult.append(result)
# set(searchResult[0]).intersection(set(searchResult[1]))

# TDM의 다른 구현 형태 -> Inverted Index
# Controlled Voca.              Posting-Data
# -> Hash Table, B-Tree, Trie   -> Linked-List
# 대용량의 텍스트 데이터를 효과적으로 연산하기 위한 구조 -> Inverted Index(Doc.)
TDM = dict()  # Key:Term(Token), Value:Post[list형태]
for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        # Split, Stemming, Lemmatization, 어절, 음절, N-gram, BPE, ...
        for term in doc.split():
            if term not in TDM:
                TDM[term] = list()
            TDM[term].append(i)

# len(TDM['민족']), len(set(TDM['민족']))
searchResult = list()
for q in query.split():  # |query|
    searchResult.append(TDM[q])
set(searchResult[0]).intersection(set(searchResult[1]))

TDM = dict()  # K:Voca, V:POST 시작 위치
POST = list()  # Linked-list
for i, file in enumerate(D):
    with open(file) as fp:
        doc = fp.read()
        # Split, Stemming, Lemmatization, 어절, 음절, N-gram, BPE, ...
        for term in doc.split():
            pos = len(POST)
            POST.append((i, -1 if term not in TDM else TDM[term]))
            TDM[term] = pos

searchResult = list()
for q in query.split():  # |query|
    pos = TDM[q]
    result = list()
    while pos > 0:
        i, pos = POST[pos]
        result.append(i)
    searchResult.append(result)


globalTDM = dict()  # 단어:위치
globalPOST = list()  # (몇번째문서, 몇번나왔고, 다음위치)

for i, file in enumerate(D):
    localTDM = dict()

    with open(file) as fp:
        doc = fp.read()

        for term in doc.split():  # Tokeninzing
            if term in localTDM:
                localTDM[term] += 1
            else:
                localTDM[term] = 1

    for k, v in localTDM.items():
        if k in globalTDM:
            pos = globalTDM[k]
            postData = (i, v, pos)
            newpos = len(globalPOST)
            globalPOST.append(postData)
            globalTDM[k] = newpos
        else:
            postData = (i, v, -1)
            pos = len(globalPOST)
            globalPOST.append(postData)
            globalTDM[k] = pos

searchResult = list()
for q in query.split():  # |query|
    pos = globalTDM[q]
    result = list()
    while pos > 0:
        i, freq, pos = globalPOST[pos]
        result.append(i)
    searchResult.append(result)


from struct import pack, unpack

unpack('iii', pack('iii', *(1, 2, 3)))
globalTDM = dict()  # 단어:위치

with open('globalPOST.dat', 'wb') as fp:
    fp.close()  # 0bytes

for i, file in enumerate(D):  # 문서집합에서 i번째, file 하나씩 가져오고
    # 각 파일별 작업
    localTDM = dict()  # 문서별 단어의 빈도정보 저장하기 위한 임시 변수

    with open(file) as fp:  # 개별 문서 1개 열어서
        doc = fp.read()  # 읽고

        for term in doc.split():  # Tokeninzing(어절)
            if term in localTDM:  # 단어:빈도
                localTDM[term] += 1
            else:
                localTDM[term] = 1

    # 글로벌 POST 업데이트
    with open('globalPOST.dat', 'ab') as fp:  # 옵션 0bytes -> append bytes
        for k, v in localTDM.items():  # k:단어, v:빈도
            if k in globalTDM:  # 글로벌 해시테이블 k(단어)가 있으면,
                pos = globalTDM[k]  # 마지막 POST에 저장된 위치
                postData = (i, v, pos)  # (몇번째문서, 단어빈도, 이전위치)
                newpos = fp.tell()  # 글로벌 POST의 fp의 현재위치
                fp.write(pack('iii', *postData))
                globalTDM[k] = newpos  # 글로벌 해시테이블 k:위치 갱신
            else:  # 없으면 - 최초 등록
                postData = (i, v, -1)  # (몇번째문서, 단어빈도, 다음위치=-1)
                pos = fp.tell()  # 글로벌 POST의 fp의 현재위치
                fp.write(pack('iii', *postData))  # 구조체 12bytes 저장(Bytes)
                globalTDM[k] = pos  # 글로벌 해시테이블 k:위치

searchResult = list()  # 키워드별 검색결과
for q in '윤석열 대통령부터'.split():  # |query|
    if q in globalTDM:  # 검색어가 기존에 해시테이블 있으면,
        pos = globalTDM[q]  # 위치정보 불러오고
        result = list()
        while pos > 0:  # 위치정보가 마지막일때까지 반복
            with open('globalPOST.dat', 'rb') as fp:  # POST 파일 열어서
                fp.seek(pos)  # POST 파일의 fp 위치 pos로 변경시켜주고
                i, freq, pos = unpack('iii', fp.read(12))  # 12bytes 읽고,
                result.append(i)  # bytes -> tuple(숫자, 숫자, 숫자)
        searchResult.append(result)
        print(q, result)
# A B => A and B => 키워드별 각각 결과 => 교집합
# A B => A or B => 결과.extend
# A - B => A - B => set(A) - set(B)
# => 검색알고리즘, 단어별로 가중치 같은가? 다음 시간
cleanResult = set(searchResult[0])  # 첫 번째꺼 set해서 집합A
for result in searchResult[1:]:  # B, C, D, ...
    cleanResult = cleanResult.intersection(set(result))  # 기존과 교집합
# print(cleanResult)

# len(globalTDM)
from nltk.tokenize import sent_tokenize
from konlpy.tag import Komoran

ma = Komoran()


def featureExtractor(file, query=None):
    terms = list()
    if query is None:
        with open(file) as fp:
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


globalTDM = dict()

fp = open('globalPOST.dat', 'wb')
fp.close()

for i, file in enumerate(D):
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
len(globalTDM)

searchResult = list()
for q in '윤석열 대통령'.split():
    result = list()

    for subq in featureSelection(featureExtractor(None, q)):
        if subq in globalTDM:
            pos = globalTDM[q]
            while pos > 0:
                with open('globalPOST.dat', 'rb') as fp:
                    fp.seek(pos)
                    i, freq, pos = unpack('iii', fp.read(12))
                    result.append(i)
            searchResult.append(result)

cleanResult = set(searchResult[0])
for result in searchResult[1:]:
    cleanResult = cleanResult.intersection(set(result))
print(list(sorted(cleanResult)))

globalCollection = dict()
fp = open('globalPOST.dat', 'wb')
fp.close()

for i, file in enumerate(D):
    localTDM =featureSelection(featureExtractor(file))
    globalCollection[i] = max(localTDM.values)

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


## TF-IDF
K = 0
N = len(D)

TF = lambda freq, maxfreq, K: K+(1-K)*(freq/maxfreq)
IDF = lambda df, N:log(N/df)

fp = open('weightPOST.dat', 'w')
fp.close()

weightTDM = dict()

for t, pos in globalTDM.items():
    df = 0
    tfList = list()
    while pos > 0:
        with open('globalPOST.dat', 'rb') as fp:
            fp.seek(pos)
            i, freq, pos = unpack('iii', fp.read(12))
            maxfreq = globalCollection[i]
            df += 1

            tf = TF(freq, maxfreq,0)
            tfList.append([i, tf])

    idf = IDF(df, N)

    with open('weightPOST.dat', 'ab') as fp:
        weightTDM[t] = (df, fp.tell())
        for i, tf in tfList:
            fp.write(pack('if', *(i, tf*idf)))


# test
for m in ma.morphs('윤석열 대통령은 김건희와 미국에 다녀왔다.'):
    df, pos = weightTDM[m]
    print(m, df)
    j = 0
    with open('weightPOST.dat', 'rb') as fp:
        while df > 0:
            fp.seek(pos+(8*j))
            i, w = unpack('if', fp.read(8))
            print('\t{} - {}'.format(i, w))
            df -= 1
            j += 1