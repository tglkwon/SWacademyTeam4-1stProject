from bs4 import BeautifulSoup
import pprint

html = '''
<html>
    <head></head>
    <body>
        <div id="result">
            <p class="row">
                <p>
                    <div>
                        <a class="news_tit">link1</a>
                    </div>
                </p>
                <a class="news_tit">link2</a>
            </p>
            <p class="row">
                <a class="news_tit">link3</a>
            </p>
            <p class="row">
                <a class="news_tit">link4</a>
            </p>
        </div>
    </body>
</HTML>
'''
dom = BeautifulSoup(html, 'html.parser')
# dom.children # 아래 태그들이 나온다
dom.find('a', attrs={'class':'news_tit'}) == dom.a
# dom.findall()
dom.find('a', recursive=False) == dom.a
print(dom.find(string='link1').find_parent() == dom.a)
print(dom.find_all('a', limit=1))

cur = dom.a
print(cur.find_parents())

cur = dom.a.find_parent().find_parent()

cur = dom.find_all(attrs={'class':'row'})[1]
print(cur.find_previous_sibling(), cur.find_next_sibling())