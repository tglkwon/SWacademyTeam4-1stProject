# 정보 검색
search와 retrieval의 차이 : 규모가 정해져 있고 관리 가능한 범위에서 찾는다 전자, 후자는 바닷가의 모래알 찾기
information overload : 정보의 홍수

DTM: | D | * | Controlled
Voca |
TDM: | Controlled
Voca | * | D |
[voca1] = (1, | D |) = > Time
Complexity
낮춤
Key + Post: | Controlled
Voca | * | L | = > Space
Complexity
낮춤

  # Linked-List
list[0][1]
[0][10][?]

prev: ______
next: __ - 1
__ < - next: __[0]
___ < - next: ___[10]
___
data: ______
data: ________
data: __________
K: V(?)->next = > [10]->next = > [0]->next = -1
V(?)->data        ->data
[POST
 0: (값, 주소:-1)
1: (값, 주소:0)
...
100: (값, 주소:1)
]
len() = 101
C.V
단어: 100 = > POST[100] = (값, 주소=1) = > POST[1] = (값, 주소=0) = > POST[0] = 주소 - 1

실습: Tokenizer = > 교체, 검색을
수행해보세요
단, 토크나이저
별로
전체
Controlled
Vocaburary
확인, 몇
개까지
늘어났는지
== == >