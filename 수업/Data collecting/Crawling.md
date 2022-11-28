# 220916
# Crawling : bots, programs, spiders, web crawlers
웹 인덱싱을 하는 것

목표 : 어느 페이지에 어떤 내용이 있었는가를 알고자 함
1. 하이퍼링크를 수집한다

# 220919 번외 개념
array : sequence homo mutable
list : sequence hetero mutable

정보 검색 개념
queue : FIFO : BFS : 검색사이트를 가장 연관성이 높은 것들을 먼저 볼 수 있다.
stack : LIFO : DFS :위키 사이트처럼 가장 밑바닥 페이지가 정보가 중요한 경우 

# 220921
# Selenium
브라우저 자동화, 개발자에게 빠른 피드백을 주기 위해 만들어진 툴

request를 쏘는 방식은 js를 해석하는 기능이 없으므로 클라우드 플레어의 방화벽 방식에 막힌다. 그럴때의 대체제
Xpath
paint(displaying) - Exp 특정태그. imp(document 전체). wait
                    => 네이버 로그아웃 버트
창 전환, DOM(iframe) 전화
switch_to.~ DOM
JS 해석할때, DDOS 방어벽을 넘을때 => Cookies
