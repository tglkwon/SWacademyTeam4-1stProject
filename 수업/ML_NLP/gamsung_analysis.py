from requests import get
from bs4 import BeautifulSoup
from konlpy.tag import Okt, Komoran
from math import log

ma = Okt()

url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver'
params = {
    'code':201641,
    'type':'after',
    'onlyActualPointYn':'N',
    'onlySpoilerPointYn':'N',
    'order':'newest',
    'page':1
}

D = list()
for i in range(1,11):
    params['page'] = i
    resp = get(url, params)
    dom = BeautifulSoup(resp.text, 'html5lib')
    dom.select('.score_result > ul > li')
    for li in dom.select('.score_result > ul > li'):
        score = li.select_one('.star_score em').text.strip()
        reply = li.select_one('p span[id^=_filtered_ment]').text.strip()
        D.append((score, reply))

# print(resp.text)

def training(C, D):
    # Extract
    # V =  [row[1].split() for row in D]
    V = list()
    for d in D:
        for term in ma.nouns(d[1]):
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
        if i == 0:  # negative 평점이 5 이하인것 (str -> int로 변환)
            Dc = [d for d in D if int(d[0]) < 6]
        else:
            Dc = [d for d in D if int(d[0]) > 5]

        Nc = len(Dc)

        # Prior
        Prior[i] = Nc/N

        # Concat
        Tc = '\n'.join([d[1] for d in Dc])

        # CountTokensOfTerm
        Tct = dict()
        CondProb = dict()
        for t in V:
            Tct[t] = len([w for w in ma.nouns(Tc) if w == t])

        # CondProb
        for t in V:
            # Add-one Smoothing = laplace smoothing
            CondProb[t] = (Tct.get(t, 0) + 1) / (sum(Tct.values()) + len(Tct))

        GlobalCondProb.append(CondProb)

    return  V, Prior, GlobalCondProb

V, Prior, CondProb = training(['Negative', 'Positive'], D)

def testing(C, V, Prior, CondProb, d):
    # Extract
    W = list()
    for t in ma.nouns(d):
        if t in V:
            W.append(t)

    score = list([0]*len(C))
    for i, c in enumerate(C):
        # do score[c] =
        score[i] = log(Prior[i])

        # for each t ㅌ W
        for t in W:
            score[i] += log(CondProb[i][t])


    return score

for d in ['최근 5년 영화중 최악 웃긴 코드가 뭔지도 모르겠고 개연성도 없고 돈만 날림', '관람객 묵직했던 전편에 비해 이번엔 더 시원한 액션과 유쾌한 큰웃음까지 다 담긴 속편']:
    result = testing(['Negative', 'Positive'], V, [0.5, 0.5], CondProb, d)
    if result[0] > result[1]:
        print('Negative', result, result[0]-result[1])
    else:
        print('Positive', result, result[0]-result[1])