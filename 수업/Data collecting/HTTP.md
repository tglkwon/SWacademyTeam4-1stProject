# 220914
# HTTP : hyper text transfer protocol

웹브라우저 <-> 웹서버 <-> 저장시스템
         HTTP


CS 구조 : client(Frontend)와 server(Backend)가 서로 일정한 규칙(HTTPS)를 따르며 데이터를 주고 받을 수 있는 시스템

## URL : uniform resource locator
https://www.example.com:80/index.html

protocol : HTTPS : Hyper Text Transfer Protocol Secure
Server : www.example.com
Port : 80
File : index.html

로 나타나는 사이트을 표현하는 방식? 언어? 규칙?이 HTML : hyper text markup language

## request
Header 와 Body로 구성되어있다.

Header
    Get /index.html  HTTP/1.1
    Hoest www.example.com
    Accept text/html */*
    Accept-Language en-us
    Accept-Charset ISO-8859-1,utf-8 : 언어 인코딩 설정, 한글을 보고 싶으면 utf-8인지 확인 필요
    User-agent  Mozilla/5.0 : 클라이언트/브라우저의 신분?

## Method
safe methods : GET(DB에서 SELECT), HEAD
message with body : POST(UPDATE), PUT(INSERT INTO), DELETE 정도까지

## REST API : 백엔드 개발에 많이 쓰이는 개발 방식
REST : REpresentational State Transfer
CRUD : Create, Read, Update, Delete

RESTful : REST 방식스러운 상태
GET : /board       get list of movies
GET : /board/:id   find a movie by its ID
POST : /board      create a new movie
PUT : /board       update an existing movie
DELETE : /board    delete an existing movie

## Legal Issues : 법적인 사안들
### Opt-in vs Opt-out
Opt-in : 정보수집을 __명시적으로 동의__ 할 때에만 정보수집 __가능__ ; Whitelist
Opt-out : 정보수집을 __명시적으로 거부__ 할 때에만 정보수집 __중단__ ; Blacklist

정보 수집을 하고 최소한 출처는 확인해야 나중에 지워달라고 할 때 지울 수 있다.
기본적으로 정보 수집은 합법이다.(Opt-out) 따라서 검색엔진, 가격비교 서비스가 가능한 이유
위법이 되는 조건은 사이트 운영자가 의사에 반하는 경우. 지워달라면 지워줘야 한다.

- 불법이 될 수 있는 요소 
  - 크롤링으로 데이터를 긁다 보면 DoS가 되는 수가 있다. 트래픽 터뜨리지 않게 주의해야 한다.
  - 다른 사람의 DB는 법적으로 저작물로 인정된다. DB는 개인정보가 저장되기도 하기에 함부로 가져가면 문제가 된다.

### 사례
잡코리아 vs 사람인 : 1등 기업인 잡코리아의 정보를 검색엔진인 네이버를 통해 얻은 정보로 사람인이 사이트를 구성한 사건. 
잡코리아의 승소 + 크롤링의 법적 기준 정립된 사건 
야놀자 vs 여기어때 : 합의로 끝난듯

### 이용방침
이용방침을 준수 : 사이트 정보 이용에 대한 방침(안내, 약관 등) 미리 확인


### robots.txt : 크롤러와 같은 봇의 접근을 제어하기 위한 규약. 대상 봇, 수집 여부, 수집 범위 등을 기술함
```
User-agent: *    모든 user-agent(봇)
Disallow: /       루트 아래 모든
Allow: /$         url 아래 모든 
```

### 정리 : ~~어떤 사이트~~ 를 수집 하느냐보다는, 어떤 데이터를 수집하느냐가 문제!
1. robots.txt : 접근 제약 규칙 준수
2. Crawl delay :  사이트에 최대한 부담 지양(초당 1회 정도)
3. Term of use : 사이트 이용방침(약관) 준수
4. Public content : 지적재산권 침해 여부 주의
5. Authentication-based sites : 민감한 정보 수집 주의

Tips
builtwith : detect the technology used by a website
whois : Retrieving WHOIS information of domains

## urllib : url handing module
urllib.requst   : opening and reading urls
.error          : containing the exceptions raise 
.parse          : parsing urls
.robotparser    : robots.txt를 parsing해서 True/False로 뱉음
.response
```
from urllib import request
```
request - response
# Status code
알아야 할 코드 
- 200 : 정상
- 400번 대 : 클라이언트(내) 문제
- 500번 대 : 서버의 문제

text/html => byte -> string(utf-8/euc-kr)
application/xml+json, images/jpeg+png+webp.. , audio/video

request를 보내는 양식의 종류
GET / POST / PUT / DELETE
%Encoding(%16진수 => 1Byte)
&Encoding(&__;)
QS(Bytes) => urlencode(dict, tuple) => parse

## traffic control
```
import time
time.sleep(1) # 초 단위로 일시정지하는 코드
```

# JSON : javascript Object Notation
{"key1": "value1", "key2": 2, "key3":None, "key4": True, "key5": {"key6":[1,2,3]}}
가능한 타입
NULL, INTEGER, TEXT, BOOLEAN, ARRAY, JSON

```
from json import dumps, loads
js = dumps({"key1": "value1", "key2": 2, "key3":None, "key4": True, "key5": {"key6":[1,2,3]}}
)
```

# DOM : document object model
```
html = '''
<html>
    <head></head>
    <body>
        <div id="result">
            <p class="row">
                <a class="news_tit">link1</a>
            </p>
            <p class="row">
                <a class="news_tit">link2</a>
            </p>
        </div>
    </body>
</HTML>
'''
dom = BeautifulSoup(html, 'html.parser')
dom.children # 아래 태그들이 나온다
dom.find()
dom.findall()
```

## 웹 페이지를 읽는 4가지 방법
1. RE
2. DoM
3. Selector
4. lxl??


# 220920
# Dynamic HTML : react, angular, vue 등등

# cookie : client들의 정보를 저장하는 방식
requests 에서 Session을 이용함
