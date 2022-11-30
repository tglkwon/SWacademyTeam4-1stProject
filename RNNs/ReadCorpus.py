import re
from os import listdir
import pandas as pd
from sklearn.model_selection import train_test_split
# from nltk.tokenize import sent_tokenize
# from konlpy.tag import Okt
#
# ma = Okt()

def fileids(path, ext='txt'):
    path = path if path[-1] == '/' else path + '/'
    fileList = list()
    for fileName in listdir(path):
        if fileName.endswith(ext):
            fileList.append(path + fileName)
    return fileList


path = '../../SWacademy/Data collecting/news'

D = list()

for filename in fileids(path):
    with open(filename, encoding='utf-8') as fp:
        cate = re.search((r'(\d{3})'), filename).groups(1)[0]
        cleanText = re.sub(r'\s{2,}', ' ', fp.read().strip())
        # s = list()
        # for sentence in sent_tokenize(cleanText):
        #     words = ma.morphs(sentence)
        #     s.append(' '.join(words))
        D.append((cate, cleanText))
#%%
D = pd.DataFrame(D)
# D.describe(), D.value_counts()
#%%
train, test = train_test_split(D, stratify=D[0])