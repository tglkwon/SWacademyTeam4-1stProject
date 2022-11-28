# 스팸메일 분류기(이진 분류)
# 데이터 수집 -> D(정상메일+스팸메일) 최대한 balanced
# -> Requests(Session with Cookie)
# -> DHTML(AJAX) foldsSN

from requests.sessions import Session
from config import cookie
from html import unescape

session = Session()

for line in cookie.splitlines():
    if len(line) > 0:
        kv = line.split('\t')
        session.cookies.set(kv[0], kv[1])

# 네이버 스팸메일함을 누르면 돌아가는 request
spamURL = 'https://mail.naver.com/json/list/?page=1&sortField=1&sortType=0&folderSN=5&type=&isUnread=false&u=tglkwon'
resp = session.post(spamURL)

spamMailList = list()
for mail in resp.json()['mailData']:
    spamMailList.append(unescape(mail['subject']))

# 스팸메일의 본문들
spamReadURL = 'https://mail.naver.com/pv/read.jsp?mailsn={}&time=1666233308819'.format('mailSN')
resp = session.post(spamReadURL)