# 음절, 어절, 형태소, 품사, 어간/어근, 어미 ...
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import gutenberg
from nltk.text import Text
from konlpy.corpus import kobill, kolaw # 의사회의록, 헌법
from konlpy.tag import Okt
import matplotlib.pyplot as plt

corpus = kolaw.open(kolaw.fileids()[0]).read()
kol = Text(Okt().pos(corpus))

def ngram(tokens, n=2):
    result = list()
    for i in range(len(tokens)-(n-1)):  # Markov Assumption(N=2, 1st)
        result.append(tuple(tokens[i:i+n]))
    return result

ngram(word_tokenize('아버지가 학교에 가신다.'))

posLM = dict()
for _ in ngram(list(map(lambda _:_[0], kol.tokens))):
    if _ in posLM:
        posLM[_] += 1
    else:
        posLM[_] = 1

    for token in _:
        if (token,) in posLM:
            posLM[(token,)] += 1
        else:
            posLM[(token,)] = 1

plt.plot([1/_ for _ in range(1,51)])
# list(map(lambda _:_[0], posLM[_]), filter(lambda _:len(_) == 1, posLM))

plt.plot([_[1]/172 for _ in sorted(
    map(lambda _:(_, posLM[_]),
       filter(lambda _:len(_) == 2, posLM)),
        key=lambda _:_[1], reverse=True)[:50]])
plt.show()

# posLM[max(filter(lambda k,v:len(k) == 1, posLM.items()))]

uniMax = sorted(
    map(lambda _:(_, posLM[_]),
       filter(lambda _:len(_) == 1, posLM)),
        key=lambda _:_[1], reverse=True)[0]
biMax = sorted(
    map(lambda _:(_, posLM[_]),
       filter(lambda _:len(_) == 2, posLM)),
        key=lambda _:_[1], reverse=True)[0]

# for k,v in posLM.items():
#     if len(k) == 1:
        # print(k[0], v/uniMax[1])


def calcProb(token):
    if (token,) in posLM:
        return posLM[(token,)]/uniMax[1]

calcProb('에')

def calcConProb(token1, token2):
    if (token1, token2) in posLM:
        return posLM[(token1,token2)]/posLM[(token1,)]
    

print(calcProb('유구'), calcProb('한'), calcConProb('유구', '한'))

