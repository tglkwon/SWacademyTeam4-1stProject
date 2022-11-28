from requests import get
from requests.compat import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup
import re

def robotParser(domain):
    url = urlunparse(urlparse(domain)[:2] + ('',) * 4)
    url += '/robots.txt'
    pathEnable = dict()
    resp = get(url)
    if resp.status_code == 200:
        agent = None
        for line in resp.text.splitlines():
            key, *value = line.split(':')
            key = key.strip()
            value = ':'.join(value).strip()

            if key.lower() == 'user-agent':
                agent = value
                if value not in pathEnable:
                    pathEnable[value] = dict()
            else:
                if key.lower() == 'allow':
                    pathEnable[agent][value] = True
                else:
                    pathEnable[agent][value] = False
    else:
        pathEnable['*'] = True

    return pathEnable


def canFetch(pathEnable, path):
    agent = '*'
    path = urlparse(path).path
    if agent in pathEnable:
        if path in pathEnable[agent]:
            return pathEnable[agent][path]
        else:
            if path == '/':
                return True
            else:
                return canFetch(pathEnable, '/'.join(path.split('/')[:-1]))
    else:
        return True


google = robotParser('https://www.google.com')
# print(google['*']['/search'])
canFetch(google, '/search/static?asdf')

url = 'https://news.naver.com'
urls = list()
urls.append((url, 0))  # 깊이 제한
seens = list()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

robots = dict()

while urls:
    # URLs Pool
    seed = urls.shift()  # Stack=DFS, .shift()로 하면 queue이고 BFS방식이 된다.
    seens.append(seed[0])  # 깊이 제한

    # #Robots.txt
    # if seed not in robots:
    #     robots[seed] = robotParser(seed)
    # rp = robots[seed]
    # print('[Robots.txt]', seed, canFetch(re, seed))

    # Focuesd Crawling
    if seed[1] > 2:  # 자의적 깊이 결정 => 휴리스틱
        continue

    resp = get(seed[0], headers=headers)  # 깊이 제한
    if resp.status_code == 200 and 'Content-Type'.lower() in resp.headers:
        if 'text/html' in [_.strip() for _ in resp.headers['Content-Type'].split(';')]:  # 나중에 수정할 예정
            dom = BeautifulSoup(resp.text, 'html.parser')
            aList = dom.select('a[role=menuitem]')
            hList = dom.select('a.cluster_text_headline')
            if len(aList) > 0:
                for _ in aList[1:6]:
                    url = _.attrs['href']
                    nextUrl = urljoin(seed[0], url)  # 깊이제한
                    urlParams = urlparse(nextUrl)

                    # URL 체크
                    if nextUrl not in seens and \
                            nextUrl not in [_[0] for _ in urls] and \
                            nextUrl.startswith('http'):
                        # javascript, #fragment 제외시켜야함
                        # Focused 특정 조건으로만
                        urls.append((nextUrl, seed[1] + 1))  # 깊이 제한
            if len(hList) > 0:
                for _ in hList:
                    url = _.attrs['href']
                    nextUrl = urljoin(seed[0], url)  # 깊이제한
                    urlParams = urlparse(nextUrl)

                    # URL 체크
                    if nextUrl not in seens and \
                            nextUrl not in [_[0] for _ in urls] and \
                            nextUrl.startswith('http'):
                        # javascript, #fragment 제외시켜야함
                        # Focused 특정 조건으로만
                        urls.append((nextUrl, seed[1] + 1))  # 깊이 제한

            news = dom.select_one('#ct #contents')
            # print(imgs.text)
            if news:
                fileName = re.search('(\d{10})[?]sid=(\d{3})', resp.url)
                with open('./news/{}-{}.txt'.format(fileName.group(2), fileName.group(1)), 'w', encoding='utf8') as f:
                    f.write(news.text.strip())

                for img in news.select_one('#img1'):
                    urls.append((urljoin(resp.url, img.attrs['data-src']), seed[1]+1))

        else:
            #image/jpeg
            ext = re.search(r'image/(.+?);', resp.headers['Content-Type'])
            if ext:
                # fileName = re.search('(\d{8}_\d{3})', resp.url)
                fileName = resp.url.split('/')[-1]
                fileName += '.'+ext.group(1)
                with open('./news/'+fileName, 'wb') as fp:
                    fp.write(resp.content)

        # else:
            print(resp.headers['Content-Type'])
    # break
    print(len(urls), len(seens))

print(seens)

