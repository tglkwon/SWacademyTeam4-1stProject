import re
from readCorpus import fileids
from nltk.tokenize import sent_tokenize
from konlpy.tag import Okt
from math import log
# from gamsung_analysis import training, testing

ma = Okt()
path = '../Data collecting/news'

D = list()

for filename in fileids(path):
    with open(filename, encoding='utf-8') as fp:
        cate = re.search((r'(\d{3})'), filename).groups(1)[0]
        cleanText = re.sub(r'\s{2,}', ' ', fp.read().strip())
        s = list()
        for sentence in sent_tokenize(cleanText):
            s.append(' '.join(ma.nouns(sentence)))
        D.append((cate, '\n'.join(s)))


# print(D[:10])
def training_NB(C, D):
    # Extract
    # V =  [row[1].split() for row in D]
    V = list()
    for d in D:
        for term in d[1].split():
            if len(term) > 1: # 1 음절짜리 단어 제거
                V.append(term)
    V = list(set(V))

    # CountDocs
    N = len(D)

    # for each c ㅌ C
    Prior = list([0]*len(C))
    # CondProb
    GlobalCondProb = list()

    for i, c in enumerate(C):
        # CountDocsInClass
        Dc = [d for d in D if d[0] == c]

        Nc = len(Dc)

        # Prior
        Prior[i] = Nc/N
        # print(Nc, Prior[i])
        # Concat
        Tc = '\n'.join([d[1] for d in Dc])

        # CountTokensOfTerm
        Tct = dict()
        CondProb = dict()
        for t in V:
            Tct[t] = len([w for w in Tc.split() if w == t])

        # CondProb
        for t in V:
            # Add-one Smoothing = laplace smoothing
            CondProb[t] = (Tct.get(t, 0) + 1) / (sum(Tct.values()) + len(Tct))

        GlobalCondProb.append(CondProb)

    return  V, Prior, GlobalCondProb


def testing_NB(C, V, Prior, CondProb, d):
    # Extract
    W = list()
    for t in d.split():
        if t in V:
            W.append(t)

    score = list([0]*len(C))
    for i, c in enumerate(C):
        # do score[c] =
        # print(Prior[i])
        score[i] = log(Prior[i])

        # for each t ㅌ W
        for t in W:
            score[i] += log(CondProb[i][t])


    return score

news_classes = ['정치','101','102','103','과학']
V, Prior, CondProb = training_NB(news_classes, D)
print(len(V), Prior)

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
ct = list()
for s in sent_tokenize(d):
    ct.append(' '.join(ma.nouns(s)))
    
result = testing_NB(news_classes, V, Prior, CondProb, '\n'.join(ct))

print(news_classes[result.index(max(result))])