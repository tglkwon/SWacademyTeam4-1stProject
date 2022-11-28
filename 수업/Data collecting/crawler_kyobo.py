import requests
from html import unescape

# url = 'https://search.kyobobook.co.kr/web/search'
url = 'https://ac.search.naver.com/nx/ac'
params = {
    "q": "ㅎ",
    "con": 0,
    "frm": "nv",
    'ans': 2,
    'r_format': 'json',
    'r_enc': 'UTF - 8',
    'r_unicode': 0,
    't_koreng': 1,
    'run': 2,
    'rev': 4,
    'q_enc': 'UTF - 8',
    'st': 100,
    '_callback': '_jsonp_0'
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
resp = requests.get(url, params=params)
print(resp.status_code)
resp.json()

# dom = BeautifulSoup(resp.text , 'html.parser')
# dom.select_one('#daumContent')


# for _ in resp.json()['data']['list']:
#     print(_['no'], unescape(_['title']))