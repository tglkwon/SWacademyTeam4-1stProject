from math import log

trainingData = [
    (1, "Chinese Beijing Chinese", True),
    (2, "Chinese Chinese Shanhai", True),
    (3, "Chinese Macao", True),
    (4, "Tokyo Japan Chinese", False)
]

testData = [
    (5, "Chinese Chinese Chinese Tokyo Japan"),
    (6, "Chinese Chinese Chinese"),
    (7, "Tokyo Japan")
]

def training(C, D):
    # Extract
    # V =  [row[1].split() for row in D]
    V = list()
    for d in D:
        for term in d[1].split():
            V.append(term)
    V = list(set(V))

    # CountDocs
    N = len(D)

    # for each c ㅌ C
    Prior = list([0]*len(C))
    # CondProb
    GlobalCondProb = list()

    for i, c in enumerate(C):
        # CountDocsInClass
        Dc = [d for d in D if d[-1] == c]
        Nc = len(Dc)

        # Prior
        Prior[c] = Nc/N

        # Concat
        Tc = '\n'.join([d[1] for d in Dc])

        # CountTokensOfTerm
        Tct = dict()
        CondProb = dict()
        for t in V:
            Tct[t] = len([w for w in Tc.split() if w == t])

        # CondProb
        for t in V:
            # Add-one Smoothing = laplace smoothing
            CondProb[t] = (Tct.get(t, 0) + 1) / (sum(Tct.values()) + len(Tct))

        GlobalCondProb.append(CondProb)

    return  V, Prior, GlobalCondProb

V, Prior, CondProb = training([True, False], trainingData)

def testing(C, V, Prior, CondProb, d):
    # Extract
    W = list()
    for t in d.split():
        if t in V:
            W.append(t)

    score = list([0]*len(C))
    for i, c in enumerate(C):
        # do score[c] =
        score[i] = log(Prior[i])

        # for each t ㅌ W
        for t in W:
            score[i] += log(CondProb[i][t])


    return score


print(testing([True, False], V, Prior, CondProb, testData[0][1]))

## test
for test in testData:
    score = testing([True, False], V, Prior, CondProb, test[1])
    print(score)