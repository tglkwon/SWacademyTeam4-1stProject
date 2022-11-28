from requests import Session, get
from config import instagram, headers
from datetime import datetime

# get token and login
session = Session()
resp = session.get('https://www.instagram.com', headers=headers)

print(resp.status_code, resp.cookies.get('csrftoken'))

url = 'https://www.instagram.com/accounts/login/ajax/'
params = {
    'enc_password': None,
    'username': 'tglkwon@naver.com',
    'optIntoOneTap': 'false'
}
params['username'] = 'tglkwon@naver.com'
params['enc_password'] = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), instagram['password'])
headers['x-csrftoken'] = session.cookies.get('csrftoken')
resp = session.post(url, data=params, headers=headers)
print(resp.status_code, resp.cookies.get('csrftoken'), resp.json())

# get insta pages
url = 'https://i.instagram.com/api/v1/tags/web_info/'
params = {
    'tag_name': None
}
params['tag_name'] = '한지민'
headers['x-csrtftoken'] = session.cookies.get('csrftoken')
headers['x-ig-app-id'] = '936619743392459'

result = session.get(url, params=params, headers=headers)
print(result.status_code, result.headers['content-type'], result.text)
print(result.json())
for _ in result.json()['data']['most']['section']:
    for media in _['layout_content']['medias']:
        print(media['media']['image_version2']['candidates'][0]['url'])