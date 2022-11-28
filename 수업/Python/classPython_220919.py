def decorator1(fn):
    print('decorator1') #함수가 만들어질 때 실행된다.
    def inner1(*args, **kkwargs):
        print('inner1')
        return fn(*args, **kkwargs)
    return inner1

def decorator2(fn):
    print('decorator2') #함수가 만들어질 때 실행된다.
    def inner2(*args, **kkwargs):
        print('inner2')
        return fn(*args, **kkwargs)
    return inner2


@decorator1
@decorator2
def x():
    print('x')

# stack으로 실행되는 경우 : super(), 다중 decorator
print(x())
# x = decorator1(decorator2(foo))
# 선언은 de2 de1 그리고 실행은 de1 de2

from dataclasses import dataclass
# 타입 힌트를 단축해서 만들 수 있다.
@dataclass
class Point:
    x:int
    y:int


p = Point(3,4)
q = Point('a','b')
print(p.x, q)