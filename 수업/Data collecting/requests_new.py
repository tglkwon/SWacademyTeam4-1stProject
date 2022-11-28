from requests_dom import request
import re
# get
# url = 'https://httpbin.org/get'
# resp = request('GET', url, params={'a':1, 'b':2})

# post
url = 'https://httpbin.org/post'
resp = request('POST', url, data={'가':'a', 'b':1}, params={}, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
# print(resp.url, resp.request.body)

from json import dumps, loads

# print(loads(resp.text)['args'], resp.json())


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'http://httpbin.org/image/jpeg'
resp = request('GET', url, headers=headers)
print(resp.headers['Content-Type'])

## 네이버에서 해보기

url = 'https://search.naver.com/search.naver'
params = {'where':'nexearch','sm':'top_hty','fbm':1,'ie':'utf8','query':'%ED%95%9C%EA%B0%80%EC%9D%B8'}
params['query'] = '박보경'
resp = request('GET', url, params=params, headers=headers)
# 중간 점검 코드
# print(resp.status_code, resp.url, resp.request.headers, resp.headers)
# print(resp.text)
# content = re.findall(r'<a href="(.+?)" class="news_tit" .+? title="(.+?)">.+?</a>', resp.text)
content = re.findall(r'<li class="bx" .+?<a href="(http.+?)" class="news_tit"', resp.text)
print(content)