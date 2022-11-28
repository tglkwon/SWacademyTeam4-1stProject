from konlpy.tag import Kkma
from konlpy.utils import pprint
# kkma = Kkma()
# pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))
# pprint(kkma.nouns(u'질문이나 건의사항은 깃헙 이슈 트래커에 남겨주세요.'))
# pprint(kkma.pos(u'오류보고는 실행환경, 에러메세지와함께 설명을 최대한상세히!^^'))

from konlpy.tag import Okt
pprint(Okt().pos('아버지가 방에 들어가신다.'))

from konlpy.corpus import kobill, kolaw # 의사회의록, 헌법
corpus = kolaw.open(kolaw.fileids()[0]).read()

from nltk.tokenize import sent_tokenize, word_tokenize
print(len(corpus.splitlines()), len(sent_tokenize(corpus)))

print(len(word_tokenize(corpus)))

from nltk.text import Text
t = Text(word_tokenize(corpus))
print(t.vocab().B(), t.vocab().N())

from nltk.corpus import gutenberg
emma = Text(word_tokenize(gutenberg.open(gutenberg.fileids()[0]).read()))
list(zip(t.vocab().most_common(10), emma.vocab().most_common(10)))
print(t.vocab().most_common(10))

kol = Text(Okt().pos(corpus))
list(zip(t.vocab().most_common(10), kol.vocab().most_common(10)))

print(t.vocab().B(), kol.vocab().B())


from konlpy.tag import Hannanum, Komoran
ma1 = Kkma()
ma2 = Hannanum()
ma3 = Komoran()
ma4 = Okt()

list(zip(ma1.tagset, ma2.tagset, ma3.tagset, ma4.tagset)), \
    len(ma1.tagset), len(ma2.tagset), len(ma3.tagset), len(ma4.tagset)

from nltk.stem import PorterStemmer
porter = PorterStemmer()

for _ in ['played', 'swiss']:
    print(porter.stem(_))


import matplotlib.pyplot as plt
plt.plot([1/_ for _ in range(1,51)])
plt.plot([_[1]/12012 for _ in emma.vocab().most_common(50)])
plt.plot([_[1]/357 for _ in t.vocab().most_common(50)])
plt.show()

list(zip(emma.vocab().most_common(10), t.vocab().most_common(10), kol.vocab().most_common(10)))

sum(map(lambda _:_[1], emma.vocab().most_common(50)))/emma.vocab().N(),\
sum(map(lambda _:_[1], t.vocab().most_common(50)))/t.vocab().N(),\
sum(map(lambda _:_[1], kol.vocab().most_common(50)))/kol.vocab().N()

50/emma.vocab().B(), 50/t.vocab().B(), 50/kol.vocab().B()

threshold = .2
freq = 0
totalFreq = sum(emma.vocab().values())
termlist = list()


for _ in sorted(emma.vocab().items(), key=lambda _:_[1]):
    freq += _[1]
    if freq/totalFreq > threshold:
        break
    else:
        termlist.append(_)


emma.vocab().B(), emma.vocab().N(), len(termlist), termlist[:10]

doc =''
uniqTerms = list()
totalTerms = list()
from konlpy.corpus import kobill
for fileName in kobill.fileids():
    doc += kobill.open(fileName).read()
    _t = Text(ma4.morphs(doc))
    print(_t.vocab().N(), _t.vocab().B())
    uniqTerms.append(_t.vocab().B())
    totalTerms.append(_t.vocab().N())

# K = 10~100, beta = 0.4~0.6
plt.plot(uniqTerms)
plt.plot([10*(_**0.52)for _ in totalTerms])
plt.show()

s = '''
최유정 "돌싱남? 만날 수 있어"…리콜돌싱남, 급발진 프러포즈에 당황 ('이별리콜') [종합]
6일 방송된 KBS2TV ‘이별도 리콜이 되나요?’ 에서는 최초로 돌싱리콜남이 등장해 X와의 재회를 준비하는 모습이 그려졌다. 

이날 리콜남은 X를 만나기 전에 이혼한 경험이 있다고 말했다. 리콜남은 "가장으로서 돈을 버는 게 우선이라고 생각했다. 전처가 산후 우울증이 그렇게 심한 줄 몰랐다. 결국 이혼하게 됐다"라며 "포기하려고 할 때 운 좋게 여자친구를 만났고 그 친구를 만나면서 안정을 찾았다"라고 말해 눈길을 끌었다. 리콜남은 "고민을 많이 했지만 다시 만나야 할 사람이라고 생각했다"라고 말했다. 
'''
s = '아버지가방에들어가신다.'
pprint(list(zip(ma1.pos(s), ma2.pos(s), ma3.pos(s), ma4.pos(s))))
print(ma1.nouns(s), ma2.nouns(s), ma3.nouns(s), ma4.nouns(s))