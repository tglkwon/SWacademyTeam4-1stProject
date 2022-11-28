from corpusRead import fileids, ngram

data = {
    'low':5,
    'lowest': 2,
    'newer': 6,
    'wider': 3
}
# data = {
#     '대통령실': 5,
#
# }

newData = dict()
for k,v in data.items():
    newData[tuple(k)] = v #('<\w>',)] = v

keyCand = dict()
for k,v in newData.items():
    for bi in ngram(k):
        if bi in keyCand:
            keyCand[bi] += v
        else:
            keyCand[bi] = v


import re
merge = max(keyCand, key=keyCand.get)
mergeData = dict()
for k,v in newData.items():
    newK = re.sub(' '.join(merge), ''.join(merge), ' '.join(k))
    mergeData[tuple(newK.split())] = v


