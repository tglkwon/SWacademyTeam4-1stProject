from os import listdir
import re
from nltk.tokenize import sent_tokenize
from konlpy.tag import Komoran
from struct import pack, unpack

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

# len(globalTDM)

## 만든 TDM에서 특정 단어, 단어구 있는지 확인하기
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
# print(list(sorted(cleanResult)))

###########################################################################################
## globalCollection은 어떤 의미인지 모르겠습니다.
###########################################################################################
globalCollection = dict()
fp = open('globalPOST.dat', 'wb')
fp.close()

for i, file in enumerate(D):
    localTDM = featureSelection(featureExtractor(file))
    globalCollection[i] = max(localTDM.values())

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
