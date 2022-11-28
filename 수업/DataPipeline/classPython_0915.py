from itertools import (accumulate, chain, combinations,
                       count, cycle, groupby)
b = accumulate([1,2,3,4,5], lambda x,y:x+y, initial=5)
print('accumalate',next(b))

c = chain([1,2,3], [3,4,5])
print(next(c))

combi = combinations(range(10), 2)
print(next(combi))

cnt = count(5, 12)
print(next(cnt))

cyc = cycle(range(5))
print(next(cyc))

gb = groupby(range(5))
print(next(gb))

from functools import singledispatch
@singledispatch
def x():
    print('x')

@x.register(int)
def _x(a):
    print('int')

@x.register(dict)
def _x(a):
    print('dict')

from collections.abc import Sequence
class ExpandingSequence(Sequence):
    def __init__(self, it):
        self.it = it
        self.cache = []
    def __getitem__(self, index):
        pass

# a = ExpandingSequence()
#print(a) => __getitem__, __len__이 없으니 만들라는 오류가 뜬다

from pprint import pprint

# pprint(dir("str"), width=10)

from operator import add, sub, mul
add(1,2)
def add_4(x,y=4):
    return add(x,5)

print(add_4(3))

####################################################

import seaborn as sns
iris = sns.load_dataset('iris')
temp = [i+1 for i in iris.sepal_length]

iris.sepal_length.map(lambda x:x+1)


list(enumerate([1,2,3,4,5,6]))
# => [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)]

for i,j in enumerate([1,2,3]):
    print(i,j)

# decorator
def x(fun):
    def y():
        print('start')
        fun()
        print('end')
    return y

@x
def y():
    return 1

print(y())

### decorator 중급 ; 3단 구조
def z(m=3):
    def x(fun):
        def y(*args, **kwargs):
            print('decorator')
            fun()

        return y

    return x


@z(4)
def t():
    print('a')


print(t())
