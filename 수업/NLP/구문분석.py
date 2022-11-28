from os import posix_fallocate
from nltk.tokenize import word_tokenize

s = 'the little yellow dog barked at the cat'

pos_tag(word_tokenize(s))

#DT + ( JJ + JJ )* + NN
parser = RegexParser('NP: {<DT><JJ>*<NN>}')

tree = parser.parse(pos_tag(word_tokenize(s)))
for node in tree:
    print(node)

from konlpy.tag import Komoran
ma = Komoran()

kparser = RegexParser('''
NP: {<N.+>+<J.+>}
VP: {<M.+>*<V.+><E.+>*}
''')

kparser.parse(ma.pos('내 친구는 잠을  진짜 엄청 많이 잔다.'))

### 영어로 해봅시다

ex1 = 'I shot an elephant in my pajamas.'
pos_tag(word_tokenize(ex1))

parser = RegexParser('''
NP: {<DT>?<PRP.*>?<NN>*}
PP: {<IN><NP>}
VP: {<V.+><NP|PP>}
VP: {<VP><PP>}
''')
tree = parser.parse(pos_tag(word_tokenize(ex1)), True)
tree.draw()
[_ for _ in tree.subtrees() if _.label() == 'NP']