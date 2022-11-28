from bs4 import BeautifulSoup
from requests import request, get
from requests.compat import urljoin

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'https://www.google.com/search'
url_naver = 'https://search.naver.com/search.naver'
url_daum = 'https://search.daum.net/search'

params = {'q':'한가인'}
response = get(url_naver, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
print(dom.find_all('div', attrs={'class':'total_tit_group'}))
# lis = dom.find_all('li', attrs={'class':'bx'})
print(dom.find_all('a'))
# for _ in dom.find_all(attrs={'class':'news_tit'}):
#     print(_.find_parent().attrs['href'])
#     print(_.text.strip())

url_naver_webtoon = 'https://comic.naver.com/webtoon/detail?titleId=732036&no=162&weekday=fri'
response = get(url_naver_webtoon)
dom = BeautifulSoup(response.text, 'html.parser')

for img in dom.find(attrs={'class':'wt_viewer'}).find_all('img'):
    if img.has_attr('src'):
        print(urljoin(url_naver_webtoon, img.attrs['src']))