import star as s
from star import _x, a
from star import * # "*"은 모든 것. "_"로 시작하는 private은 예외
import sys
# print(sys.path)

print(s._a)
print((s.__name__))
# print(globals()) # 내가 직접 접근이 가능한 것들을 모아둠

def x(**a):
    print(a)


b = {'a': 1, 'b': 2}
x(**b)

print(1000_000)

#예제
print(list(map(lambda x: x+2, [1,2,3,4,5])))

c = type('B', (int,), {})
print(c(1))

# 일부러 틀리는 코드

class A:
    def __new__(self):
        print('new')
        return super().__new__(self) # 이부분이 없으면 틀린다

    def __init__(self):
        print('init') # __init__는 return이 있으며 안된다.

    def __call__(self):
        print('c') #

a = A()
# print(A())
# print(a())

class S(type):
    x = None
    def __call__(self):
        if S.x is None:
            S.x = super().__call__()
        return x

class SS(metaclass=S):
    pass


s = SS()
print(s)

b = SS()
print(b)


from abc import ABCMeta, abstractmethod

class A(metaclass=ABCMeta):
    @abstractmethod
    def x(self):
        pass

class AA(A):
    def x(self):
        pass

a = AA()

print(a)
