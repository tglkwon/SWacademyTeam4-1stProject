import builtins
from timeit import timeit


print(int())
# 기본값은 0
print(list())
# 기본값은 []
print(float())
# 기본값은 0.0
print(3 and [])
print({} and 4)
print(3 or [])
print({} or 4)

# print(sum(["a","b","c"]))

a = [1,2,3]
b = iter(a)
print(b)
print(next(b))

i = 5
while i > 1:
	print(i)
	i -= 1
else:
	print('end')	


try:
	a = 1/0
except:
	print('에러나면 대신 실행될 구문')
else:
	print('문제가 없으면 실행될 구문')
finally:
	print('')


print(range(10))

a = [i for i in dir(builtins) if 'Error' in i]
# print(a)
while True:
	try:	
		a = input("숫자 넣어주세요\n")
		b = int(a)
	except:
		continue
	else:
		print(b)
		break


def t(x,*,t):
	return x+t

print(t(5,t=1))

import matplotlib.pyplot as plt
# plt.hist([1,2,3,4,1,4,1,2,3,4,1,2,3,1,2,5,5,3,1,2,3,5,1,2,5,5,2,3,5,2,3,2,3,5,2,3,5,5,1,3])

def x(m):
	def y(n):
		return m+n
	return y


print( x(3)(4) )

import sys
# print(sys.version())
# dir(sys)


##### 클래스

class A:
	def __init__(self):
		print('A')

class B(A):
	def __init__(self): # overriding
		A.__init__(self)
		print('B')

class C(A):
	def __init__(self):
		A.__init__(self)
		print('C')

class D(B,C):
	def __init__(self):
		B.__init__(self)
		C.__init__(self)
		print('D')

d = D()
print(D.mro(), d)
	

class AA:
	def __init__(self):
		print('A')

class BB(AA):
	def __init__(self): # overriding
		super().__init__()
		print('B')

class CC(AA):
	def __init__(self):
		super().__init__()
		print('C')

class DD(BB,CC):
	def __init__(self):
		super().__init__()
		print('D')

dd = DD()
print(dd) 	