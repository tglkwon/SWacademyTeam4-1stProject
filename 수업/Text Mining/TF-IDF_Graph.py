# https://ko.wikipedia.org/wiki/Tf-idf
from math import log
import matplotlib.pyplot as plt

freq = range(1,101)
maxfreq = max(freq)
sumfreq = sum(freq)

# TF(Term Frequency)
# boolean
tf1 = lambda t:[0 if f == 0 else 1 for f in t]
#
tf2 = lambda t:[f for f in t]
# sum frequency
tf3 = lambda t, sf:[f/sf for f in t]
# max frequency
tf4 = lambda t, mf:[f/mf for f in t]
# log scale
tf5 = lambda t:[log(1+f) for f in t]
tf6 = lambda t, mf, k: [k + (1-k)*f/mf for f in t]

plt.plot(tf1(freq)) # 회색
plt.plot(tf2(freq)) # 주황색
plt.plot(tf3(freq, sumfreq))    # 녹색
plt.plot(tf4(freq, maxfreq))    # 갈색 => maxfreq Normalization
plt.plot(tf5(freq)) # 보라색
plt.plot(tf6(freq, maxfreq, 0)) # 갈색
plt.plot(tf6(freq, maxfreq, 0.5))   #분홍색 => K = 0.5 Double Normalization
plt.plot(tf6(freq, maxfreq, 1)) # 회색
plt.ylim(0,2)
plt.show()

# IDF(Inverse Document Frequency)
# unary
idf1 = lambda df:[1 for f in df]
idf2 = lambda df, N:[log(N/f) for f in df]
idf3 = lambda df, N:[log(N/(1+f))+1 for f in df]
idf4 = lambda df, N:[log((N-f+1)/f) for f in df]

plt.plot(idf1(freq))    # 파란색
plt.plot(idf2(freq, maxfreq))   # 주황색
plt.plot(idf3(freq, maxfreq))   # 녹색
plt.plot(idf4(freq, maxfreq))   # 빨간색
plt.show()

# weight
# while > -1: