import re
from nltk.corpus import stopwords
from string import punctuation
from nltk.text import Text
from 음절 import tri2uni, uni2tri


stopwords = stopwords.open('english').read()

for w in re.sub(r'[{}]'.format(re.escape(punctuation)), ' ', "what're asdfas").split():
    print(w in stopwords)

from nltk.corpus import gutenberg
from nltk import word_tokenize
emma = gutenberg.open(gutenberg.fileids()[0]).read()
tokens = word_tokenize(emma)

newTokens = list()
for token in tokens:
    for ctoken in re.sub(r'[{}]'.format(re.escape(punctuation)), ' ', token).split():
        if ctoken not in stopwords:
            newTokens.append(ctoken)


len(set(tokens)), len(set(newTokens))
len(tokens), len(newTokens)
print(Text(tokens).vocab().most_common(50), Text(newTokens).vocab().most_common(50))


################ 한글의 stopwords

kstopwords = '은\n는\n이\n가\n께서\n에게\n을\n를\n에\nㄴ다'
s = '아버지 가 방 에 들어가신다.'
for w in s.split():
    print(w, w in kstopwords)


from konlpy.tag import Okt
ma = Okt()
for w in ma.morphs(s):
    print(w, w in kstopwords)


from konlpy.tag import Hannanum, Komoran
ma2 = Hannanum()
for w in ma2.pos('아버지가 방에 들어가신다. 들어가셨고, 들어가시네, 들어가십니다.'):
    print(w, w[1].startswith('J') or w[1].startswith('E'))


### 비속어 사전/처리
def stopfwords(fword):
    kstopwords = '시발\n'
    uinput = fword
    # uinput = input()

    result = list()
    for w in uinput.split():
        newToken = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', w)
        g = re.search('([ㄱ-ㅎㅏ-ㅣ])+', newToken)
        if g:
            re.sub('([ㄱ-ㅎㅏ-ㅣ])+', tri2uni(*list(g.group(1))), newToken)
        if newToken not in kstopwords:
            result.append(newToken)
        else:
            result.append(len(newToken)*'*')

    return ' '.join(result)
