# OT - 유길상 교수님 
1. 앞으로의 강의 계획
-- 4개월 간 이론, 프로그래밍, 프로젝트를 모두 끝내야함
2. 수상받은 프로젝트 사례들
-- 최대한 많은 사람들이 쓸 수 있는 앱?을 목표로 할 것


# class am - 문근영 선생님
## 파이썬 기본
```a = 1```
왼쪽 항은 name space or identifier으로 부름. 그 이유는 파이썬의 특징 중 하나인 타입을 선언하지 않고 변수를 넣고 그 타입으로 알아서 설정됨
일부 name은 미리 정해진 타입 및 변수가 있다. - keyword
```keyword.kwlist
len(keyword.kwlist) -> 36개가 있다.```

error
name error - 이름을 붙일 수 없는 것에 이름을 붙이려 할 경우
syntax error - 문법에 맞지 않는 경우

이름 명명법 -  
- snake 방식 - 두 단어를 중간에 '__' 를 이용해 붙인다. function에 붙인다. steam_library 
- camel 방식 - 두 단어 중 뒷 단어를 대문자로 사용 - steamLibrary
- pascal/capsword - 두 단어 모두 대문자로 사용 - class에 붙인다. -SteamLibrary

네이버 면접 질문 pep8은 무엇인가
PEP 8 - Python Enhancement Proposals 파이썬 코딩 스타일 가이드

이름에 숫자로 시작하는 문자는 쓸 수 없다. 
```1a = 1 -> systaxs error```

```이름 =``` Assignment or Binding: 할당
	import antigravity - 파이선의 자료형 할당이 자유롭다는 것을 표현
내부적으로 '=' 뒤에 값(타입)에 따라 알아서 할당
Literals - data type을 표현하는 특수문자
없으면 정수, [] list, {} tuple 등등

-id(이름): 이름의 주소가 나옴
-type(이름): 이름의 타입이 나옴

```= expression``` : 식 또는 표현식 - 연산 결과에 의해 하나의 표현으로 reduction가능한 문장
파이썬에서 function은 first class function으로 부르고 "=" 다음에 올 수 있다.

-data : 0101 기계어 그 자체
-value : 기계어의 해석된 결과 - type을 다르게 두면 value가 바뀜


## 숫자형 타입 4가지 - Int, float, complex, bool - 정수, 부동소수, 복소수, true/false
builtins : 기본적으로 사용할 수 있는 것들 - 타입명 포함됨
파이선에서 int의 최대값이 존재하는데 그보다 더 큰 수를 할당해도 알아서 더 큰 범위의 int로 바꿔준다 - 무한대까지 가능
-> 타입을 알아서 바꿔주는게 개발 경험을 좋지만 속도를 느리게 한다 - 수치해석에 부적합한 언어

### int의 4가지 표현 : 기본이 10진법
```0b010
0b3 -> syntax error : 2진법에 어긋남
0b : 2진법
0o : 8진법
0x : 16진법```

### float : 부동소수 - 소수에는 부동소수와 고정소수가 있다. 파이선에서 부동소수만 씀.
컴퓨터는 0과 1로만 데이터를 표현하기에 소수를 완벽하게 나타낼 수 없다. 근사값을 - 부동소수, 고정소수의 문제가 발생
```0.1 +0.1+ 0.1 => 0.300000004```
부동 소수처리하는 룰 IEEE754
프로그래밍에서 float은 연속이다고 처리함 - 미분가능 - 무한대의 개념이 들어가 있다.
부동 소수의 가장 큰 값
```sys.float_info```
부동 소수의 최대값 근처에서는 inf: 무한대 처리함
```a = 1e+308
a == a+1
a*10 => inf```

소수로 만들어주는 literal "."
```.3 => 0.3
3. => 3.0
1e1 => 10.0 : 10^1```

연산 속도는 int가 float보다 빠르다

-nan : Not a number 파이선에서는 float으로 처리
```float('nan') => nan```

### complex : 복소수 
```1j*1j => -1+0j```

### boolean : True == 1 / False == 0
```type(True).__base__
issubclass(bool, int) => True - 다른 데이터 타입임에도 서로 연산이 되는 경우```

-coercion (코어션)
같은 형의 두 인자를 수반하는 연산이 일어나는 동안, 한 형의 인스턴스를 다른 형으로 묵시적으로 변환하는 것. 예를 들어, int(3.15)는 실수를 정수 3으로 변환합니다. 하지만, 3+4.5 에서, 각 인자는 다른 형이고 (하나는 int, 다른 하나는 float), 둘을 더하기 전에 같은 형으로 변환해야 합니다. 그렇지 않으면 TypeError를 일으킵니다. 코어션 없이는, 호환되는 형들조차도 프로그래머가 같은 형으로 정규화해주어야 합니다, 예를 들어, 그냥 3+4.5 하는 대신 float(3)+4.5

```2 / 3 => 0.66666
2 // 3 => 0
2 % 3 => 1

-2 // 3 => -1 
-0.6666666 => -1 + 0.3333333
2 % -3 => -1

-round : 반올림하는 함수
round(1.5) => 2
round(2.5) => 2 - 실수를 정확히 표현 불가능하기 때문에
round(-1.5) => -2
round(-2.5) => -2
```
-decimal : 정확한 소수를 계산할 때 씀, fractions - ML은 정확한 값을 계산하는 게 아니라 추측하는거라 필요없음

-atomic : 숫자는 각 자리별로 쪼갤수 없다. 반대말로 쓸 수 있는 개념이 container : 여러개를 나눌 수 있는 거
다른 문자형은 쪼갤 수 있다.

```a = 'abcd'
len(a) => 4
```
-container :
  homo : 같은 데이터 타입만 담을 수 있는 경우. tensorflow는 data로 homo ex)문자열 'abcd' / hetero ex) List [1, 2, '3']
  sequence : indexing과 sliceing이 가능한 데이터 타입. 순서가 명확하다. sequence data type끼리 더할 수 있다.  ex) List / nonsequence ex) Dict
```b = [1,2,4] + [3,4,5] => [1,2,4,3,4,5]
b = [1,2,4]*4 = [1,2,4,1,2,4,1,2,4,1,2,4]```
mutable / immutable


## 문자 - str bytes, bytearray, memoryview
	str u'abcd' // 기본은 유니코드 문자열이고 그냥 쓰면 됨
	bytes b'abcd' // 아스키코드만 가능. 모든 문자열의 subset이기에 웹으로 전송하는 파일 등에 사용

### List : squence hetero mutable type 변형가능한 타입

파이선은 상수가 없다. 
```a = 1
a = 2
a => 2```
다시 선언하면 재할당하여 값이 바뀜

값을 재할당해도 주소가 바뀌지 않는 data type이 mutable
```a = [1,2,3]
id(a)
a.append(4)
id(a)```

### tuple : squence hetero immutable type - record, istance, data 변형되면 안되는 값을 저장할때 사용
```b = 1,2
b = (1,2)```

mutable data의 문제 - 얕은 복사, 깊은 복사
```c = d = [1,2]
c.append(3)
c => [1,2,3]
d => [1,2,3]
하나만 바꿔도 같이 바뀐다
c = d = [[1,2],[3,4]]
c[0][0] = 200
d => [[200,2],[3,4]]

e = [1,2]
f = e
f[0] = 100
e => [100,2]
e.copy()

이 상황을 처리하기 위한 방법
x = [1,2,3]
x[:] => [1,2,3]

import copy
f = copy.deepcopy(e)

a,b = 1,2 => a,b = (1,2)
b,a = a,b => (b,a) = (a,b) 
a => 2
b => 1

*a, b = 1,2,3
a => [1,2]
b => 3```

-duck-typing (덕 타이핑)
 올바른 인터페이스를 가졌는지 판단하는데 객체의 형을 보지 않는 프로그래밍 스타일; 대신, 단순히 메서드나 어트리뷰트가 호출되거나 사용됩니다 (“오리처럼 보이고 오리처럼 꽥꽥댄다면, 그것은 오리다.”) 특정한 형 대신에 인터페이스를 강조함으로써, 잘 설계된 코드는 다형적인 치환을 허락함으로써 유연성을 개선할 수 있습니다. 덕 타이핑은 type() 이나 isinstance() 을 사용한 검사를 피합니다. (하지만, 덕 타이핑이 추상 베이스 클래스 로 보완될 수 있음에 유의해야 합니다.) 대신에, hasattr() 검사나 EAFP 프로그래밍을 씁니다. 

### set : hetero nonsequence mutable
frozenset : hetero nonsequence immutable
set에는 mutable한 data를 넣을 수 없다. 중복이 안되고 순서가 내부적으로 강제됨.
```a = {1,1,1,2,2,2}
a => {1,2}

a = {1,2,[3]}
typeError : unhashable type 모든 구성물에 mutable한 data가 없음```

### Dictionary : key, value로 이루어진 mutable data
```{'a':1, 'a':2} => {'a': 2}```
중복되면 가장 마지막 것으로 됨
```1 in {'a':1, 'b':2} => False
for i in {'a':1, 'b':2}
	print(i)
=> a
	b
```

# 0902
```
import keyword
keyword.kwlist
```

파이선 복합문
## if문
```
if 조건문:
	print('a')
```
조건문에 literal을 넣을 수 있다. 파이선에서는 거의 모든것을 조건문에 넣을 수 있다.

파이선은 객체지향 방식 프로그래밍 언어

설명(help)에 나오는 []는 옵션, 기본값은 0
int([x]) 
list([iterable])

파이선에서 참/거짓은 0, [], 0.0 등 각 literal의 기본값이 아니면 참이다. None 또한 거짓. false =! None 이다.

## and/or
-and 파이선은 앞이 참이면 뒤를 반환, 앞이 거짓이면 앞을 반환
```3 and [] => []
	{} and 4 => {}```
-or 앞이 참이면 앞을 반환, 앞이 거짓이면 뒤를 반환
```3 or [] => 3
	{} or 4 => 4```

1/0 zero division error 0으로 나누라고 하면 에러가 난다
or에서 저런 에러 문제가 발생하더라고 다른것이 참이면 에러가 나지 않는다. 나중에 문제가 생길 여지가 많으니 주의.

```b = 5
4 if a > 5 else 5
=> 4
```

## 반복문
### iterable : 반복가능한, 순회가능한
특정 상황에서 iterator : 순서대로 앞에서부터 데이터를 하나씩 뽑아서 보낸다.
```
list("abcd") => ['a','b','c','d']
for i in "abcd":
	print(i)
=> a b c d
```
for문 안의 in 다음에는 iterable한 것들이 올 수 있다.

```
def a():
	for i in 1,3,4,5,6:
		print(i)

import dis
dis.dis(a)
```
파이썬에서 어셈블리어 단위로 실행이 되는 것을 볼 수 있는 구문

```
a = [1,2,3]
b = iter(a)

for a in iterable:
	실행
else:
	끝나고 실행

i = 5
while i > 1:
	print(i)
	i -= 1
else:
	print('end')	
```

for문 while문에 else 사용가능하다
while문이 for으로 대체가 안되는 경우 : 무한루프돌릴때 gui만들때 입력을 기다리는 방식에 사용한다.

-EAFP
 허락보다는 용서를 구하기가 쉽다 (Easier to ask for forgiveness than permission). 이 흔히 볼 수 있는 파이썬 코딩 스타일은, 올바른 키나 어트리뷰트의 존재를 가정하고, 그 가정이 틀리면 예외를 잡습니다. 이 깔끔하고 빠른 스타일은 많은 try와 except 문의 존재로 특징지어집니다. 이 테크닉은 C와 같은 다른 많은 언어에서 자주 사용되는 LBYL 스타일과 대비됩니다.

-LBYL
 뛰기 전에 보라 (Look before you leap). 이 코딩 스타일은 호출이나 조회를 하기 전에 명시적으로 사전 조건들을 검사합니다. 이 스타일은 EAFP 접근법과 대비되고, 많은 if 문의 존재로 특징지어집니다. 
 다중 스레드 환경에서, LBYL 접근법은 “보기”와 “뛰기” 간에 경쟁 조건을 만들게 될 위험이 있습니다. 예를 들어, 코드 if key in mapping: return mapping[key] 는 검사 후에, 하지만 조회 전에, 다른 스레드가 key를 mapping에서 제거하면 실패할 수 있습니다. 이런 이슈는 록이나 EAFP 접근법을 사용함으로써 해결될 수 있습니다.

## try
```
try:
	에러가 날 수 있는 구문
except 에러명:
	확실히 예상가능한 에러에서 실행될 구문
except:
	에러가 나면 대신 실행될 구문	
else:
	문제가 없으면 실행될 구문
finally:
	위의 모든
```

모든 에러명을 보자
```
import builtins
dir(builtins)
```

### accumulation pattern
 축적해서 결과를 낸다. reduction: 축적해서 합친 하나의 결과를 낸다.
 초기값을 두고 그 이후 iterator등을 축적시켜 결과를 내는 방식을 말한다.

```temp = []
for i in dir(builtins):
	if 'Error' in i:
		temp.append(i)
```		

### look and search pattern
 전체 중에 특정 패턴 찾기

```a = 'absdbvaawrevaseda'
temp = 0
for i in a:
	if i =='a':
		temp += 1

for i in a:
	if i == 'a':
		print(i)
		break
```

사용자에게 입력을 받는다. 테크닉
```
while True:
	try:	
		a = input("숫자 넣어주세요")
		b = int(a)
	except:
		continue
	else:
		print(b)
		break
```

## Assert : 중대한 에러라 서비스를 중단시키더라도 발생시키는 에러처리
a = 2
assert a==1 , 'a = 1 이어야 함'

## raise : 강제로 특정 에러(builtin error)를 발생시킬 수 있다.
if a == 0;
	raise Exception('나만의 에러')
	raise ArithmeticError
	
## 함수
파이선은 객체지향 언어이지만 함수형 프로그래밍 기법을 지원한다.
함수형 프로그래밍의 함수는 수학적 함수에 가깝다.
```def x():
	print('a')
	return None # 생략가능, 기본으로 붙는 return

def y():
	return 1
```	
입출력 둘다 없음
출력만 있음
둘다 함수의 조건을 만족시키지 못함

1. First Class Function > object(value)
파이선의 함수는 객체에서 만들어졌으므로 값이다.
- higher order function : 함수를 인자로 받고 return 할 수 있는 함수

2. callable
파이선에서 ()는 연산자이다. 함수의 return값을 계산해서 반환해준다.

- 정의(선언) / 캡슐화 (encapsulation)
 재사용하기 위해 정의, 선언한다. 재사용 안 하는 함수 lamda
 - 함수
 - 클래스

```
def x(a): # a를 파라미터(매개변수)라고 한다.
	print(a)

x(3) # 3을 argument(인자)
x(a) # Signature

def xx(a,b):
	return a+b
```

### 파라미터 입력 방식 5종
```
xx(2,3) # positional 방식: 값을 순서대로 넣는다.
xx(a=2, b=3) # keyword 방식: 순서에 대한 제약이 없다. 지원하지 않는 언어도 있다. => method overloading을 지원 안 할 경우가 많음
```
정의할 때 default값을 줄 수 있다.

```
def xx(a,b=3):
	return a+b
```
default는 파라미터의 뒤쪽으로 가야한다. 적은 인자가 왔을때 default가 없는 값부터 넣어야 작동하기 때문
positional 방식과 keyword방식은 혼용이 되기는 하나 한 번 keyword 방식을 쓰면 그 이후는 keyword 방식으로만 써야한다.

len(obj,/)
/ 이전 인자들은 무조건 positional 방식만 써야한다.

def t(x,*,t):
	return x+t
*이후 인자들은 무조건 keyword 방식만 써야한다.

def k(*a):
	return a
넣지 않아도 되고 여러 개 입력할 수 있다. 가변 positional 방식

def kk(**a):
	return a
가변 keyword 방식

**kwargs : 키워드 argument, 많이 쓰는 argument들을 모아놓은 거. 개발시 모든 경우를 고려할 수 없으므로 나중에 추가하기 용이한 장점이 있다.

# 220905 함수에 이어서

```def x(a:int) -> int:
	'''설명'''
	return a

help(x)
x.__annotations__
```
파라미터에 입력할 타입과 함수가 출력할 타입을 설명에 넣어둘 수 있다.

## nested : 중첩
## LEGB : local Enclosing Global Builtin 순으로 변수를 찾는다.
로컬에 없으면 글로벌에서 변수를 찾아라. 역은 성립하지 않는다. encapsulation

```
a=1
def x(a):
	a = 2 # local variable
	return a

x()
```

## clouser 함수 안에 함수를 넣고
unboundLocalError : local 변수와 글로벌 변수를 같은 이름으로 선언하면 생기는 문제

```
a = 1
def x():
	global a
	a += 1
	return a


x() => 2
```

사용하기는 쉬우나 글로벌 변수 조작하다 생길 수 있는 문제가 많아서 자주 쓰지 않는게 좋다

enclosing
```
a=1
def x():
	a=2
	def y():
		nonlocal a
		a = a+1
		return a
	return y


x() => 3
```

builtin 함수도 새로 정의해버릴 수 있다.

```print < builtins :function
print = 1
print
=> 1
del print
```

# class
- assignment 할당 다른 이름으로 binding보다 더 복잡하면 다양한 기능을 할 수 있다.

할당과 관련된 개념들
 ```
 a = 1 ## assignment / binding
 a = b = 1
 a = b = [1,2]
 a, b= 1,2 # unpacking
 a, *b = 1,2,3 # star
 a += 1
 global
 nonlocal
 ```  

파이선에서는 data type을 class라고 한다. 따라서 새로운 class를 만드는 것은 새로운 data type을 만드는 것과 같다. 클래스 이름()하는 것으로 값을 만든다
설명에서 Init signature: 클래스에서 함수를 이용하여 값을 만들것을 암시한다.

meta

```
class A: # attrinbute 
	a = 1 # class attribute / variable
	def c(self): # instance method (attribute) > instance = object
		self.c = 2 # instance variable
		print('c')
	@class method
	def d(cls):
		print('d')


dir(A)  # class 정보가 다 나열된다

파이선의 모든 클래스는 object를 기본적으로 상속받고 시작한다.
class A(object):	# inheritance / 상속
__*__ dunder : double underbar / magic method
```
```
class T:
	def __iter__(self,x):
		return iter([1,2,3])


t = T()
for i in t:
	print(i)
```

```
import numpy as np
a = np.array([1,2,3])
np.array <- factory method(function) # design pattern
a = np.ndarray([1,2,3]) <- 진짜 클래스 
```

```
class B:
	bb = 1
	def cc(self, c):
		self.c = c
# class 변수는 클래스를 정의할 때 생성. 각각의 인스턴스들이 공유하는 값
# 인스턴스 변수는 인스턴스 메소드가 실행된 후 생성. 각각의 인스턴스들이 각자 가지고 있는 값
b1 = B()
b1.cc(3)
b2 = B()
b2.cc(4)

class C:
	def __init__(self,x): # initializor : 생성자 > 차후 new로 확장
		print('init')
		self.x = x

	def y(self):
		print(self.x)
# 인스턴스 변수는 클래스 내 에서 서로 사용 가능하다. 함수와 크게 다른 점 중 하나
c = C() => Error x값을 입력하도록 에러남
c = C(3) => init	# __init__ 실행
클래스 내에서 바로 실행되는 instance
vars(c) => {'x': 3}  # 현재 저장하고 있는 instance variable을 가르쳐준다
```		

## 함수와 클래스를 쓰는 경우 확인
 함수는 외부에서 접근할 수 없다. 클래스는 내외부에서 접근하고 바꿀 수 있다. 클래스는 값과 행동을 동시에 마음대로 다룰 수 있다.


 class A: # attrinbute 
	aa = 1 # class attribute / variable
	def c(self, x): # instance method (attribute) > instance = object
		self.x = x # instance variable
		print('c')


a.aa = 'sun'
vars(a) => {'t':4, 'aa': 'sun'}
b.aa => 1
# 인스턴스 변수에 없으면 클래스 변수를 찾는다.

A.s = 'moon'
a.s => 'moon' # 내부적으로 __get__이 실행된다
a.s = 4 # 내부적으로 __set__이 실행된다
``` 

클래스에는 두 가지 연산을 지원한다.
. : 참조 연산자
() : 생성 연산자
float을 만드는 .과 구분할 필요가 있으면 띄어쓰기를 추가한다.
```
-1 .__abs__()
```

# 220906 inheritance 상속 :다른 사람이 이미 만든 클래스를 받아와서 
- 변경(Overriding) : 완전히 변경 할 수도 있고, 부분만 변경할 수 있다.
- 추가
- 삭제 (delegate 때문에 불가능) : 자식 클래스에 없는 것을 명령하면 부모 클래스에서 실행시킴
- 그대로 사용하는 것

## class inheritance (delegate) : 자식에 없는 건 부모에서 찾는다.

```
클래스.__main__ : 현재파일에서 정의했다는 것을 알려줌
클래스.__bases__ : 현재 클래스의 상속 받은 부모 클래스들을 알려줌
클래스.__base__
클래스.__mro__
클래스.__mro__
```

## 다중상속 : diamond 문제 등. 일반적으로 다른 프로그래밍 언어는 문제가 일어날 소지가 있어서 다중상속을 금지한다. 파이선은 허용한다
class A(X,Y):
	pass

## method vs function
사용 주체에 따라서 method도 되고 function이 될 수도 있다.

self : 객체 자체를 대신해준다
aa = A() : aa가 self

```
class A:
	def sun(self):
		print('sun1')

class B(A):
	def sun(self):
		print('sun2')

class C(B,A):
	pass

# 다중상속으로 개족보 상속이 생기는 경우에 생기는 문제를 diamond 문제라 부른다.
# 이를 해결하는 파이선의 방법은 mro을 이용하여 안되는 다중 상속을 금지시킨다. diamond 문제가 있을 수 없다.
## metaclass : class의 class
## mro : method resolution order 

# 클래스의 기본 옵션
class E(object, metaclass=type):
	pass

class E:
	pass
```

## 부모 클래스의 method 변경/ 일부 변경
```
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
print(d) => A B A C D
```
super() <- # 부모의 instance를 (상속 체계를 고려하여) 반환한다
일을 처리하는 방식이 stack이다. <- mro 순서의 역순처럼 보이는 이유
```
class A:
	def __init__(self):
		print('A')

class B(A):
	def __init__(self): # overriding
		super().__init__()
		print('B')

class C(A):
	def __init__(self):
		super().__init__()
		print('C')

class D(B,C):
	def __init__(self):
		super().__init__()
		print('D')

d = D()
print(d) => A C B D
```


```
class A:
	def xx(self):
		print('xx')

class B(A):
	pass
```
# 상속을 대신하는 합성 (1)
```
class C:
	x = A.x
	def __init__(self):
		self.a = A()
	
	def xx(self):
		self.a.xx()
```
# 상속을 대신하는 합성 (2)
```
class D:
	def __init__ (self):
		self.a = A()	# compos

	def __getattr__(self, x):	# attribute error 발생시 실행, try/except
		return getattr(self.a, x)
```
# 다형성 
- override : python은 function/method 이름만 맞추면 가능하다
- 일반적으로 다른 언어들은 override signature를 맞춰야 한다.

# Overloading
- function overloading : python에서 제공하지 않는다. / 대신 generic을 제공
``` 
# function overloading이 지원된다면 다른 함수로 간주하는 개념 (parameter/type이 다르기 때문에)
def x(int a):
	print(a)

def x(str a):
	print(a)

def x(a,b):
	print(a,b)

x(1)
x(1,2)
가 가능하게 되는것이 overloading
```

- operator overloading : 연산자의 기본 기능을 변경. 같은 클래스 내에서 사용 (overriding은 다른 함수(상속)로부터 온 것을 바꾸는 경우)

```
type(tips)
type(tips['tip'])

tips.describe() # 다형성을 지원하지 않는다면 describe_dataframe() 이런 식으로 이름을 다르게 해야한다
tips['tip'].describe()
# 이 둘의 결과가 다른 것이 overloading의 예시
```

## generic : 특정 data type에 따라서 다르게 처리

## dispatch : 전파, delegate와 비슷한 개념
```
from functools import singledispatch
# 기본적으로 python에서는 multi dispatch를 지원하지 않는다.
# 예시에서는 x를 generic function이라고 부른다
@singledispatch
def x(a):
	print(a)

@x.register(int)
def _(a):
	print('int')
	print(a)

@x.register(str)
def _(a):
	print('str')
	print(a)

```

# 220907
객체지향 프로그래밍 -> 이미 만들어진 클래스를 활용/수정하여 나에 딱 맞는 기능을 만들어내는 방식이다.

파이선은 함수, 클래스 외부에서 내부 요소에 접근하지 못하는 것은 없다
하지만 관례상 다른 언어들처럼 private처럼 쓰고 싶다면 _% 이런 식으로 쓴다.

파이선에서는 파일도 객체로 읽어온다

"*"의 활용
```
2*2 => 4
2**3 => 8
[1,2,3]*4 => [1,2,3,1,2,3,1,2,3,1,2,3]
a, *b = 1,2,3

def x(a, *b): # 별표 뒤에는 keyword 방식으로 쓴다
    pass

def x(*a): # 가변 positional
    pass
    
def x(**a): # dictionary
    pass
    
from s import *
```

```
a = [1,2,3]
x(a) => ([1,2,3],)
x(*a) => (1,2,3)

def x(**a):
    print(a)
    
b = {'a':1, 'b':2}
x(**b) # 
x(*b) # key

b = {'a':1, 'b':2}
c = {'a':3, 'c':4}
d = {**b, **c}
=> {'b':2,'a':3, 'c':4}
```

package import할 때 __all__이 정의되어 있으면 그 부분만 import한다.

### '_'의 활용 1000_000
숫자에 _는 아무때나 붙일 수 있다. 시각적으로 큰 수를 끊어읽기 위한 도구

가장 최근 결과값을 _로 알 수 있다.
변수의 앞에 _를 붙이면 관례상 private으로 취급한다.
관례상 변수명을 쓰기 싫을때, 사용되지 않는 변수를 _로 쓴다
```
for i,_ in [1:2,3:4].items():
    print(i) 
```

## 다형성 복습 (Polymorphism)
- 상속
- overloading (function overloading: python에선 generic으로 구현, operator overloading)

## metaclass : 클래스의 클래스, 클래스의 행동을 결정한다.
*클래스는 object(instance)의 행동을 결정한다.
type()은 익명 클래스를 만드는 식으로 볼 수 있다. 메타 클래스이다.

### lamda : 익명 함수 또는 함수식
```
lamda x: 3
def a(x):
    return 3
# 둘이 같은 기능을 하는 함수이다.    
```
1회성으로 사용할 때 사용한다.

### 추상화 : 파이선의 추상화는 metaclass를 이용하여 구현한다.
````
# 클래스의 기본적으로 정의되어 있는 것들
class A(object, metaclass=type):
    pass

object와 metaclass    
````

### singleton : python의 클래스는 인스턴스를 무한히 만들 수 있지만 단 하나의 인스턴스를 만드는게 메타클래스의 시작
```
class A:
    def __new__(self):
        print('new')
        return super().__new__(self) # 이부분이 없으면 틀린다

    def __init__(self):
        print('init') # __init__는 return이 있으며 안된다.

    def __call__(self):
        print('call') #
```


메타클래스를 만드는 3단계
1. type을 상속해서 메타클래스를 만든다.

```
class S(type):
    def __call__(self):
        print('call')
```
싱글톤

추상 클래스를 만드는 방법
```
from colections.abc import ABCMeta, abstractmethod

class A(metaclass=ABCMeta):
    @abstractmethod
    def x(self):
        pass
```

문제상황 : Sequence 데이터 타입을 받게 클래스를 만듦
일일이 체크하는 것을 다 안 만듦. 일부 아예 안 만듦.
```
class A:
    def __getitem__(self, x):
        pass
    def __len__(self):
        pass
```
저 두가지가 있으면 squence 데이터 타입으로 본다

덕 타이핑을 쓰면 실수할 수 있지만. 메타클래스를 이용해 사용을 특정 상황으로 강제한다.

```
import tensorflow as tf
import inspect
print(inspect.getsource(Squence))
```

메타 클래스 없이 쓰기 위해 만든 모듈
```
from abc import ABC
class A(ABC):
    @abstractmethod
    def x(self):
        pass
```