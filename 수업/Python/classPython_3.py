import matplotlib.pyplot as plt
#import matplotlib.pylab as plt
plt.plot([1,2,3],[4,5,6])
plt.title('title')
plt.figure(figsize=(5,5))
plt.axes((0,0,0.5,0.5))
plt.title('sun')
plt.axes((0.5,0.5,.5,.5))
plt.plot([1,2,3,5],[1,4,5,6])
plt.title('moon')

# plt.axes(share=True)
plt.subplot(1,2,1)
plt.subplot(1,2,2)
plt.title('sun')

# fig, (ax1, ax2) = plt.subplot(1,2)
# ax2.set_title('moon')
# ax1.set_title('sun')

plt.show()


def fibonacci(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    return fibonacci(n-1) + fibonacci(n-2)

import time
time.time()
def x(a=time.time()):
    return a
# 함수를 정의할 때 time()이 고정 되서 들어간다
print(x)
print(x)
# 같은 값이 나온다

temp = []
for i in range(5):
    temp.append(lambda m: m+i)
    #temp.append(lambda m,i=i: m+i) dump 안되게 하는 트릭

print(temp[1](5))
# 함수가 되기전에 dump가 되서 마지막 함수 m+4만 생성된다.
temp = [lambda m: m+i for i in range(5)]
print(temp[1](5))
# 결과가 다르다


class A:
    def __init__(self, m):
        self.m = m

    @staticmethod
    def y(n):
        # return self.m + n
        pass