import re
from requests import request, get
from bs4 import BeautifulSoup
#

url = 'https://pythonscraping.com/pages/page3.html'
response = get(url)
# print(response.text)
dom = BeautifulSoup(response.content, 'html.parser')
# print(dom.find(attrs={'id':'wrapper'}))
# print([_.name for _ in dom.find(attrs={'id':'wrapper'}).find_all(recursive=False)])

# footer에서 table찾기
footer =dom.find(attrs={'id':'footer'})

table = footer.find_parent().find('table', attrs={'id':'giftList'})
table_rows = [_ for _ in table.find_all('tr', attrs={'class':'gift'})]
# costs = [_ for _ in table_rows.find('td')]
# print(costs)

# 페이지의 내용중 이미지가 있다면 다운받기
from requests.compat import urljoin

for img in dom.find_all(attrs={'src':re.compile('\d[.]jpg$')}):
    # print(urljoin(response.url, img.attrs['src']))
    url = urljoin(response.url, img.attrs['src'])
    response = get(url)

    MIME = response.headers['Content-Type'].split('/')

    if MIME[0] == 'image':
        fp = open(response.url.split('/')[-1], 'wb')
        fp.write(response.content)
        fp.close()

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'https://www.google.com/search'
params = {'q':'한가인'}
response = get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')

for _ in dom.find_all(attrs={'class':'LC201b MBeuO DKV0Md'}):
    print(_.find_parent().attrs['href'])
    print(_.text.strip())
