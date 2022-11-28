from bs4 import BeautifulSoup
from requests import request, get
from requests.compat import urljoin

url = 'https://pythonscraping.com/pages/page3.html'
dom = BeautifulSoup(get(url).text, 'html.parser')

# print(dom.select_one('#wrapper'))
# body > div > img + h1 # img tag 옆에 있는 h1 tag
# <div>
#     <img>
#     <h1></h1>
# </div>
dom.select('tr > td:nth-child(3)')
dom.select('img[src]')
zzzzzzzzzzzzzzzzzzzzzz
## google

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'https://www.google.com/search'
params = {'q':'한가인'}
response = get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')

# print(dom.select('.LC201b.MBeuO.DKV0Md'))
#
# for _ in dom.select('.LC201b'):
#     print(_.name, _.text)
#     print(_.find_parent().attrs['href'])
#
#
# for _ in dom.select('a:has()> .LC201b'):
#     print(_.attrs['href'])
#     print(_.name, _.text)

## naver
url_naver = 'https://search.naver.com/search.naver'
params_naver = {'where':'nexearch','query':'한가인'}
dom = BeautifulSoup(get(url_naver, params=params_naver, headers=headers).text, 'html.parser')

# for _ in dom.select('.news_tit, .link_tit, .total_tit[href]'):
#     print(_.attrs['href'], _.text)

## 뽐뿌
response = get('https://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard')
# print(response.text)
dom = BeautifulSoup(response.text, 'html.parser')

# print(dom.select('a:has(> font.list_title)')[1:])
for _ in dom.select('a:has(> font.list_title)')[1:]:
    content = BeautifulSoup(get(urljoin(response.url, _.attrs['href'])).text, 'html.parser')

    break

# print(content.select_one('.board-contents'))
print(len(dom.select('a[href], iframe[src], form[src]')))