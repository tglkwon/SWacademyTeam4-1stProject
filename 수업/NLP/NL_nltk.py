import nltk
# nltk.download('gutenberg')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import gutenberg

# Corpus(말뭉치) => 특정 시대에서 한 언어를 사용하는 사람들이 사용하는 말의 집합

emma = gutenberg.open(gutenberg.fileids()[0]).read()
# len(emma)

# 문헌(서) - 문단 - 문장 -어절 - 단어(품사) - 형태소 - 음절 - 자소(자음/모음)
# Split - Tokenizing - POS Tagger
# 어간 추출(stemming), 표제어 추출(Lemmatization), N-gram, WordPieceModel(BytePairEncoding)
# 품사 -> 구문 분석(Parse Tree/Grammar)
# 토큰 -> Vectorize(One-Hot, Dense, TF-IDF, Matrix Decomposition)
# 까지가 전처리
# => 모델(ML, DL) - classification, clustering + information Retrieval(빅데이터 생태계)
# embedding, vanilla RNN + LSTM/GRU, Attention, Transformer(Seq2Seq), BERT, BART, GPT-3

from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer, regexp_tokenize, punkt
print(len(emma.splitlines()), len(sent_tokenize(emma)))
print(len(word_tokenize(emma)), len(emma.split()))

tokenizer = TweetTokenizer()
# s  = 'Hi=)=(^^ㅠㅠㅜㅜㅡ'
# print(word_tokenize(s), tokenizer(s))

regexp_tokenize(emma, r'\b(.+?)\b')
# regexp_tokenize(s, r'\b([a-zA-z]+|[\^\=\(\)]{2,}\b')

from nltk.tag import pos_tag
# Penn Tree Bank, Brown => POS표
from nltk.help import brown_tagset, upenn_tagset
tags = pos_tag(word_tokenize(emma))
print(tags[:10])

# NNS, NNP, IN
# brown_tagset('NNP')
# upenn_tagset('VBP')

print(len(sent_tokenize(emma)), len(word_tokenize(emma)), len(tokenizer.tokenize(emma)), len(pos_tag(word_tokenize(emma, preserve_line=True))))

from nltk.text import Text
t = Text(word_tokenize(emma))
print(t.vocab().B(), t.vocab().N())
print(len(t.vocab().keys()), sum(t.vocab().values()))

# Zipf : 고빈도 순으로 정렬했을 때, 순위의 역순과 일치하더라, Heap's : 문서의 갯수가 늘어날 수록 유니크한 단어가 특정 법칙을 따른다

# t.vocab() == Counter
# 자주 사용하는 단어 상위 50개가 전체 단어 사용량의 50%를 차지한다
print(sum(map(lambda _:_[1], t.vocab().most_common(50))), t.vocab().N(), sum(map(lambda _:_[1], t.vocab().most_common(50)))/t.vocab().N())

# Boolean(one-hot, 빈도 상관없음), count(freq.)-based(count-matrix, 5%의 중요한 단어 중심), TF-IDF(weight-matrix, 보정)

t.collocations()
t.concordance('Emma')
t.dispersion_plot(['Emma', 'Frank', 'Weston'])
t.similar('Emma')

from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
bigram = BigramCollocationFinder.from_words(word_tokenize(emma))
bigram.nbest(BigramAssocMeasures().pmi, 10)

# N-gram: 1-Unigram, 2-Bigram, 3-Trigram, 4-Quard,...