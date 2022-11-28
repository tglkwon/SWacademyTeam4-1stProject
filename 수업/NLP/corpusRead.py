from os import listdir

def fileids(path, ext='txt'):
    path = path if path[-1] == '/' else path+'/'
    fileList = list()
    for fileName in listdir(path):
        if fileName.endswith(ext):
            fileList.append(path+fileName)
    return fileList


def ngram(tokens, n=2):
    result = list()
    for i in range(len(tokens)-(n-1)):  # Markov Assumption(N=2, 1st)
        result.append(tuple(tokens[i:i+n]))
    return result