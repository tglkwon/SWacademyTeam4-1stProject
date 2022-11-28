# text mining의 similarity.py의 뒷부분에 합치는 형태로

import re

K = 7
result = dict()

for docID, cosSim in sorted(candidates.items(), key=lambda r:r[1], reverse=True)[:K]:
    className = re.search()
    if className in result:
        result[className][0] += 1
        result[className][1] += 1
    else:
        result[className] = [1, cosSim]


for k,v in result.items():
    print(k, v, v[1]/v[0], v[0]/K)