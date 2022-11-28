# knn 실습 - 스팸 분류(이진), 뉴스 분류(다중)
# Lazy learning -> Non Parametric -> Learning X (대신, Indexing으로 해결)
# Top K Retrieval 결과 이용(Relevance - Similarity) Distance / Angle 존재
# K 적절히 선택해서(분류 짝수 -> K 홀수, 분류 홀수 -> K 짝수) 분류기 만들기
# K-Nearest 선택 후 class 판단할 때,
# 갯수, Relevance, 평균 등 여러가지 방법이 있다. 확률로 표현하고 싶으면 MLE로 P만들면 됨

from readCorpus import fileids
from nltk.tokenize import sent_tokenize
from konlpy.tag import Okt
import re
from math import log,sqrt
from struct import pack, unpack


ma = Okt()

doc = list()
path = '../Data collecting/news'
for fileName in fileids(path):
    with open(fileName, encoding='utf-8') as fp:
        cate = re.search((r'(\d{3})'), fileName).groups(1)[0]
        cleanText = re.sub(r'\s{2,}', ' ', fp.read().strip())
        s = list()
        for sentence in sent_tokenize(cleanText):
            s.append(' '.join(ma.nouns(sentence)))
        doc.append((cate, '\n'.join(s)))
        

cate_news = ['정치', '101', '102', '103', '과학']

globalTDM = dict()
## 실제 news 파일을 읽어서 TDM을 만드는 부분
for i, file in enumerate(doc):
    ## localTDM은 한 문서 안의 단어들을 담는 dictionary
    localTDM = file[1]

    for term in localTDM.split():
        if term not in globalTDM:
            globalTDM[term] = list()

        globalTDM[term].append(i)

# TF-IDF 정의하기
K = 0.5
N = len(doc)

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


# 테스트하고 싶은 기사 내용
d = '''
구글 클라우드가 내년부터 가상화폐로도 결제를 받겠다고 선언했다. 아마존과 마이크로소프트 등 주요 클라우드 업체 가운데 가상화폐 결제를 허용하는 것은 구글이 처음이어서, 관련 업계에 미칠 파장이 상당할 것으로 전망된다.

구글 클라우드는 11일(현지시간) 연례 기술 콘퍼런스인 ‘구글 클라우드 넥스트 22’에서 이 같은 내용의 업그레이드 버전을 소개했다.

우선 구글은 미국 최대 가상화폐 거래소인 코인베이스와 제휴해 2023년 초부터 가상화폐로 클라우드 서비스를 결제할 수 있게 하기로 했다. 구글은 가상화폐 결제를 통해 치열하고 빠르게 성장하는 클라우드 서비스 시장에서 최첨단 기업들을 유인할 수 있을 것이라고 밝혔다.

코인베이스는 이번 제휴를 계기로 데이터 관련 애플리케이션을 기존 아마존에서 구글 클라우드로 옮기기로 했다.

구글 클라우드는 또 데이터 센터를 더 안전하고 효율적으로 하기 위해 인텔과 공동 설계한 칩을 출시했다고 밝혔다.

마운트 에번스(Mount Evans)라는 코드명의 E2000 칩은 메인 컴퓨팅을 하는 중앙처리장치(CPU)로부터 네트워킹을 위한 데이터 패키징 작업을 한다. 이를 통해 클라우드에서 CPU를 공유하는 고객 간에 더 나은 보안을 제공한다.

구글은 이와 함께 기업이 자사 메인프레임의 디지털 복사본을 만들어 구글 클라우드에서 동시에 실행할 수 있는 ‘듀얼 런’(Dual Run)과 팀이나 조직, 국경을 넘어서도 민감한 데이터를 사용해 협업을 촉진할 수 있도록 하기 위한 ‘비밀 공간’(Confidential Space) 서비스도 소개했다.

토마스 쿠리안 구글 클라우드 CEO는 “올해 클라우드 산업은 변곡점을 맞았다”며 “클라우드 컴퓨팅 시대에 디지털 전환은 필수가 됐으며 데이터와 인공지능(AI)은 모든 것을 변화시키고 있고, 개방적이고 연결된 생태계는 필수가 됐다”고 강조했다.

실제로 지난 7월 알파벳(Alphabet)이 발표한 2분기 실적에서 구글 클라우드는 전년 동기 대비 36% 증가한 62억7600만 달러의 매출을 기록했다.

지난해 구글 클라우드의 전체 매출은 192억 달러였다. 알파벳 전체 매출에서 차지하는 비중은 3년 전에는 6%도 되지 않았으나 현재 10%에 육박한다.
'''