# 다음에서 검색 링크 가져와서
# url + qs
# request 객체 생성
# Urlopen(Request 보내고, Response 받고)
# Response  헤더 확인 후
# Response.read().decode('utf8')에 임시저장
# 임시저장 텍스트에서 RE 찾고

from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen
import re

url = 'https://search.daum.net/search'
qs = parse_qs('w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q=%ED%95%9C%EA%B0%80%EC%9D%B8')
qs['q'] = '박보영'
qs['w'] = qs['w'][0]
qs['DA'] = qs['DA'][0]
qs['t__nil_searchbox'] = qs['t__nil_searchbox'][0]
print(qs)

req = Request(url+'?'+urlencode(qs), headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
res = urlopen(req)

content = res.read().decode('utf8')
retxt = re.findall(r'<a href="(.+?).+?class="tit_main[^>]+?>(.+?)<"', content)
print(retxt)
