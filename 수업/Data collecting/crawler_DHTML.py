from requests import get
from html import unescape
from requests.compat import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup
import re

url = 'https:/api.brunch.co.kr/v1/search/article'
params = {
    'q': '한지민',
    'page': 1,
    'pageSize': 20,
    'highlighter': 'y',
    'escape': 'y',
    'sortBy': 'accu'
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
resp = get(url, params=params, headers=headers)

# dom = BeautifulSoup(resp.text , 'html.parser')
# dom.select_one('#daumContent')
print(resp.json())

for _ in resp.json()['data']['list']:
    print(_['no'], unescape(_['title']))