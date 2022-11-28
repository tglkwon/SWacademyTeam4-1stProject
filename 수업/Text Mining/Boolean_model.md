# 221004
# Boolean Model
검색을 위해 쿼리를 잘 만들어야 원하는 정보를 찾을 수 있다.
조건이 많은 쿼리는 그 조건에 맞는 문서가 거의 없을 수 있고 너무 조건이 없다면 거의 모든 문서가 대상이 될 수 있다.

## Document Filtering vs Ranking
filtering이 boolean model을 이용한 검색 방식
ranking은 쿼리와 문서의 연관도를 이용한 순서 검색 방식
- probability ranking algorithm - BM25(best match)

## Notion of relevance
1. similarity
2. probability of relevance
3. probabilistic inference

### intuitve understanding of relevance
### Notatins
Vocabulary V = {w1,w2,...,wn}
Query q= t1,t2,...
Document d = t1,t2,...
Collection C = {d1,d2,...}
Rel(q,d) : doc d와 query q의 연관성
Rep(d) : TDM
Rep(q) : query를 TDM화 한것. 당연히 거의 대부분의 값이 0일 것이다.

# Vector Space Model - Relevance = Similarity로 계산 하는 방법
- 가정
  - 쿼리와 문서는 같은 형식(TDM)으로 표현된다.
  - relevance(d,q) ~ similarity(d,q)
- query/document를 어떻게 표현할 것인가
- similarity를 어떻게 정의할 것인가 - distance

## VS model에서 말하지 않은 것
- 기본 개념의 정의, 모든 consepts은 orthogonal하다(서로 독립적이다)
- weight를 어떻게 만들 것인가
  - query의 weight는 사용자가 필요로 하는 정보를 잘 나타내는 값이다.

### 좋은 concept이란 무엇인가
- 상호 독립적(orthogonal) : non-overlapping, 모호함이 없다.
- weight를 정확하고 자동화해서 계산할 수 있다.

### weight를 어떻게 붙일 것인가
- 왜?
  - query side : 모든 단어는 중요한 정도가 똑같지 않다.
  - doc side : 특정 단어는 content에 대해 더 많은 정보를 가진다.
- 어떻게?
  - 두 가지 휴리스틱을 사용한다
  - TF(Term Frequency) = Within-doc-frequency
  - IDF(Inverse Document Frequency)

## TF : 단어의 빈도수로 가중치를 구하는 방법
doc 길이의 두 가지 관점
- 도배로 문서의 길이가 길 수도 있고 정말 좋은 내용이지만 내용이 많아서 문서의 길이가 길어질 수도 있다.
Raw TF는 정확하지 않다.

문서 길이에 따른 패널티를 과하게 주는 경우를 줄이자.

1. sublinear TF scaling(log를 이용한 방법)
2. Maximun TF scaling : query만들 때 많이 쓴다. 쿼리는 길이가 짧기에
   tf(t,d) = alpha + (1-alpha) * f(t,d) / max(f(t,d))


## IDF
아이디어 DF가 낮은 값은 특정 문서를 대표하는 단어일 가능성이 있다. 이를 찾아내는 방법을 알아보자
IDF(t) = 1 + log(N / df(t))

## TF-IDF weighting
- 문서에 자주 나오는 단어 -> tf가 높음 -> 높은 weight
- 문서 집합에서 잘 안나오는 단어 -> IDF가 높음 -> 높은 weight
- weight = TF(t,d) * IDF(t)

C = {d1,d2,...}
V = {w1,w2,...}
DTM = |C|*|V|
TDM = |V|*|C| => complextiy 낮음
              => inverted Index(hash + post(linked-list))
TDM =   d1  d2  d3  ...
      w1
      w2
      w3
      ...

d = {w1, w2, ...}, BoW
=> weight = TF-IDF(TF: most common in doc, IDF: rare term in collection) Zipf
TF = Double-Normalization K = K + (1-K)freq(t,d)/maxFreq(t,d)
IDF = raw IDF = log(N/df(t))

ti = (단어, 포스팅 파일 위치) => globalTDM => Lexicon
while >-1
  몇번 반복: df(t_i)
  (몇번 문서, 몇회, 다음 파일 위치)
        freq(t_i)

N = len(D)
=> Documents|Collection
  (1번 문서, 최대 빈도수)

Summation(t ㅌ (C)V)     t ㅌ d_i
TDM: {단어: 위치}
문서1에 대한 모든 단어의 가중치를 구하려면?

# weight
1. euclidean distance : query vetor와 TDM matrix간의 거리를 이용해 similarity를 측정하는 방법
2. cosine similarity : query vetor와 TDM matrix간의 각도를 이용해 similarity를 측정하는 방법
    V_q * V_d
- 빠른 계산식 cosine(Vq, Vd) = Vq * Vd/|Vd| : query는 weight를 계산할 때는 고정된 값이기 때문이다.