from requests import Session, get
from requests.compat import urlencode
from bs4 import BeautifulSoup
from config import c

session = Session()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
resp = get('https://nid.naver.com/nidlogin.login')
dom = BeautifulSoup(resp.text, 'html.parser')
form = dom.select_one('form')
inputList = form.select('input[name]')

for _ in c:
    if len(_) > 0:
        tokens = _.split('\t')
        # print(tokens)

    cookies = {_.split('\t')[0]: _.split('\t')[1] for _ in c if len(_) > 0}

resp = get('https://mail.naver.com', headers=headers, cookies=cookies)

for k, v in cookies.items():
    session.cookies.set(k,v)

print(session.get('https://mail.naver.com', headers=headers).text)
# [.name _ccr(1st.from)]  [.subject ]

url = 'https://mail.naver.com/json/list/'
params = {
    "page":1,
    "sortField":1,
    "sortType":0,
    "folderSN":0,
    "type":"",
    "isUnread":"false",
    "u":"tglkwon"
}

resp = session.post(url+'?'+urlencode(params), headers=headers)
print(resp.headers)

# mail names
mailUrl = 'https://mail.naver.com/json/list/'
mailParams = {
    'charset': '',
    'prevNextMail': 'true',
    'threadMail': 'true',
    'folderSN': 0,
    'listScrollPosition': 0,
    'mailSN': 0,
    'previewMode': 2,
    "u": "tglkwon"
}

resp = session.post(mailUrl+'?'+urlencode(mailParams), headers=headers)

for mail in resp.json()['mailData']:
    print(mail['mailSN'], mail['subject'])
    mailParams['mailSN'] = mail['mailSN']
    data = session.post(mailUrl+'?'+urlencode(mailParams), headers=headers)
    body = BeautifulSoup(data.json()['mailInfo']['body'], 'html.parser').text.strip()
    print(body)