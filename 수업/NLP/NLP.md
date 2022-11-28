# 220927
# empirical law : 경험적 법칙
# zipf's Law : 단어의 반복도는 반복도 랭킹의 역순에 비례한다?

f = 1/k^s * 1/sigma(1/n^s)
언어 종류에 상관없이 모든 텍스트(코퍼스)는 Zipf의 법칙을 따른다
빈도의 역순 = 순위의 역순
빈도만 가지고 전처리해 필요한 데이터만 모을 수 있다.
(한국어 - 조사 - 형식형태소/의존형태소)

# Heap's Law : 한 문서 안의 각 단어의 수를 문서의 길이에 대한 함수로 나타낸 것

V(n) = K* n^beta <=>  M = k* T^b

# N-Gram : 형태소 단위들의 조합(sequence)에서 나오는 의미를 찾기 위한 분석
contiguous sequence of n items from a given sample of text or speech

다음 단어를 예측하기 위함
P(xi|xi-(n-i)...xi-1)
P(A,B) = P(B|A)*P(A) # Bayes' theorem
Bi-gram

# 220928
- Feature (Unigram -> collocation) : Zipf
- tokenizing (쌍 ->)

wordDictionary = []
Out of Voca.  신조어 문제

Branch-Entropy, Cohesion Score => Tokenizer / unsupervised
Hamming, Leveinshitien => Edit Distance

현실적으로 오탈자, 잘못쓴거, 비속어, 띄어쓰기 안한거 => 등을 해결하기 위해 쓰는게 WPM

# Entropy : H(X) : 불확실성
X -> Y : 앞, 뒤로 2가지 경우일 때, 0.5, 0.5
0.2, 0.8로 확률이 바뀌면 불확실성이 낮아졌다고 표현한다

$$
H(X) = - sigma(n,X) { P(X) * log(P(X)) }
P(X) = 0 과 1에서 0인 표준정규분포
$$

# Cohesion Score
$$
CS = sqrt(P(X1)P(X2)...)
$$

# WPM : Word Piece Model : 하나의 단어를 내부 단어들로 분리하는  단어 분리 모델
byte pair encoding : 가장 높은 빈도의 단어 쌍을 찾는 알고리즘

# 음절 <- 자음/모음 <- 초성/중성/종성
```
ord('가'), ord('나'), ord('다')
44032 45208 45796
```

# 220928
유클리디안 distance
## Rochhio distance 
X           C1
A-----------B
## 멘하탄 distance
A
-|-|-|-|-|-|-
-|-|-|-|-|-|-
-|-|-|-|-|-|-B
D = |A-B|

## Haaming distace, 리헨슈타인
[True, True, False] XOR [False, False, False]

비교하는 두 단어의 길이가 같아야하는 단점이 있다.
중간에 글자가 추가되거나 삭제되면, 나머지 글자들도 False가 뜬다.
=> 리벤슈타인 distance가 이 단점을 해결함

## Levenshtein Distance
A:aaaaaa
B:bbbb
fn(A,B)
    if len(A) == 0, then len(B)
    if len(B) == 0, then len(A)
    if A[0] == B[0] then fn(A[1:], B[1:])
    else 1 + min (추가, 삭제, 수정)

# Text Normalization
punctucation 등을 처리할 때 처리하는 순서나 방법을 고려해야 한다.

## Stopwords : 불용어, 분석, 모델링 등에는 필요하지 않는 문법적인 단어나 대상을 가르키는 말 등
생각해봐야 할 점 : 'To be or not to be.' -> 이거 다 날아감
우리말에서는 조사
장점 : 불용어를 제거하면 complexity를 줄일 수 있다. 압축된 공간으로 x들을 표현
고유어(Feature)를 줄일 수 있고, Zipf의 고빈도 불용어 들을 제거할 수 있다.
비속어 처리 등에 이용할 수 있다.

# 이제까지의 내용
비정형데이터(텍스트) 수집 - DB저장
문자경계인식 - tokenizer(segmentation) - normalize + stopwords/조사+어미+욕+단어
            Feature Extraction
        구두점 기반, 감정표현, 정규식, stem추출, lemmatization(형태소 추출)
                                Branch-Entropy, Cohesion Score, Collocation - Bigram
                                BPE(WPM-SPM)                     
빈도, 길이, 품사 등을 기준으로 => 적절히 complexity를 줄일 수 있다.

# 220928
# Information retrieval : 정보 검색
search와 retrieval의 차이 : 규모가 정해져 있고 관리 가능한 범위에서 찾는다 전자, 후자는 바닷가의 모래알 찾기
information overload : 정보의 홍수

# 220930
# Search Engine Architecture
Deployment diagram : 통합 모델링 언어의 배포 다이어그램은 노드에서 아티팩트의 물리적 배포를 모델링한다. 예를 들어 웹 사이트를 설명하기 위해 배포 다이어그램은 존재하는 하드웨어 구성 요소, 각 노드에서 실행되는 소프트웨어 구성 요소 및 다른 부분이 연결되는 방법을 보여준다.

Crawler => Doc Analyzer-Doc Representation => Indexer-index => Ranker => Results

## 검색 - 탐색 전략 BF, DF
각각 장단점이 있지만 crawling에서는 너무 오래걸리고 언제 끝날지 모르는 문제가 있다.
Focused Crawling으로 : 찾고자 하는 대상을 제한해서 검색하는 전략

## html parsing
- shallow parsing : HTML 태그를 모두 삭제하고 텍스트로만 가져오는 방법
- jsoup 등 : dom 분석해서 정확히 우리가 원하는 내용만 추출하는 방법

## full text indexing
- 장점: 텍스트의 모든 정보를 보존할 수 있다. 자동화가 가능하다
- 단점: 계산해야 하는 양이 너무 많다

## solution : inverted index
각 단어 별 document로 연결한 구조로 자료를 만든다.
dict        ->  posting
information ->  doc1, doc2
retrieval   ->  doc1

DTM : |D|*|Controlled Voca|
TDM : |Controlled Voca|*|D|
      [voca1] = (1, |D|) => Time Complexity 낮춤
Key+Post : |Controlled Voca|*|L| => Space Complexity 낮춤

# linked-list
list[0]             [1]
    [0]             [10]            [?]
next:__-1__  <-  next:__-1__   <-next:__-1__
data:______      data:______     data:______

K:V(?)->next => [10]->next => [0]->next = -1
  V(?)->data        ->data
