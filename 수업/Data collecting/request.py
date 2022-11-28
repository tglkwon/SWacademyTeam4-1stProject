from urllib import robotparser
parser = robotparser.RobotFileParser()
parser.set_url('https://news.naver.com/robots.txt')
parser.read()
# print(parser.can_fetch('*',  '/main/imagemontage')) # => False
# print(parser.can_fetch('Yeti',  '/main/imagemontage')) # => True


from urllib.request import Request, urlopen
response = urlopen('https://www.google.com')
# print(type(response))
content = response.read()

from html import escape, unescape
# HexaDecimal -> Ampersand Encoding
# 16진 코드    -> Escape(html entities)
#             <- unescape
# 문자열 <-> 바이트(encoding/decoding)과 비슷하다.
url = unescape(content.decode('utf8'))
# print(url)

url = 'https://www.google.com/search?q=%ED%95%9C%EA%B0%80%EC%9D%B8&rlz=1C1CHBF_enKR819KR819&oq=%ED%95%9C%EA%B0%80%EC%9D%B8&aqs=chrome..69i57j69i61l2.1079j0j15&sourceid=chrome&ie=UTF-8'
# 구글은 가져가지 말라고 되어 있고 403 forbidden을 보내온다
# url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%95%9C%EA%B0%80%EC%9D%B8'
# 네이버는 가져가지 말라고 되어 있고 실제적 조치가 없음
url_daum = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q=%ED%95%9C%EA%B0%80%EC%9D%B8'
# 다음도 가져가지 말라고 되어 있고 캡챠 사이트로 리다이렉트 시킴
request = Request(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
response = urlopen(request)
response.getheaders()
# 요청 받은 것에 대한 정보들
# print(type(response), response.bstatus, response.reason, response.getheaders())

# 요청 받은 내용을 사람의 언어로 바꾸는 과정
read = unescape(response.read().decode('utf-8', errors='ignore'))
# print(read)

import re
# retxt = re.findall(r'<div class="yuRUbf"><a href="(.+?)"', read)
# print(retxt)


##########
from urllib.parse import parse_qs, urlencode
url = 'https://www.google.com/search'
qs = parse_qs('q=한가인&rlz=1C1CHBF_enKR819KR819&oq=한가인&aqs=chrome..69i57l2j69i60l3.1229j0j7&sourceid=chrome&ie=UTF-8')
print(qs)

request = Request(url+'?'+urlencode(qs), headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
response = urlopen(request)
content = response.read().decode('utf-8')
retxt = re.findall(r'<div class="yuRUbf"><a href="(.+?)"', content)
print(retxt)
