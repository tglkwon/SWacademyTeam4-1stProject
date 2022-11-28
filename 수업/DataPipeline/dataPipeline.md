# 220916
# 빅데이터 파이프라인 : 데이터를 모아서 내가 원하는 목적을 만들어주는 모델에 맞게 넣어주는 과정
데이터 처리량이 많기 때문에 최대한 동시에 많은 데이터를 많이 처리해야하고 그런 방법론이 많고 그 중 하나 배운 것이 함수형 패러다임
데이터 즉면에서는 동시에 여러 데이터를 처리할 수 있는 자료형(list, tuple) 등을 쓴다.

이러한 문제를 해결하기 위한 방법
1. 속도가 필요한 부부은 C언어로 처리하고, 대용량 데이터를 다루는 자료 구조 등을 c언어가 하는 방식 대로 처리
2. 데이터가 matrix가 기본 단위?이고 메트릭스만 빨리 처리해도 자료를 다루기(처리하기) 좋다.
3. matlab에서 사용하는 기능, 자료처리 기능 등을 모아서 새로 파이선으로 만들어 놓은 것이. numpy

# numpy : vector와 matrix를 처리하고 다루기 위해 서드파티로 만든 데이타 셋
파이선 자체에도 array가 존재하나 처리가 다르다. sequence, homogenius, mutable이라 연산자 처리가 원하는 바가 다르다.
element-wise 연산을 지원하지 않는다. 훨씬 c언어스러운 타입을 가진다. int16, int64 등

속도가 빠른 원인
1. data type의 범위 - 값의 범위를 줄이면 줄일 수록 연산 속도라 빠르다.
2. vectorization으로 연산할 수 있다.: thread 처럼 연산이 나눠져있는 묶음으로 각각을 연산하는 기능.

속도를 더 빠르게 할 수 있는 방법
1. 하드웨어 성능을 최적화 한다. (GPU, multi processor, 분할 컴퓨팅)
2. compiler를 사용한다. 다른 언어로 작동시키는 파이선. 파이선으로 만든 파이선도 있고 심지어 빠르다.
3. glue language의 특징을 이용해 다른 언어와 같이 사용하기 좋게한다.
4. 알고리즘 / data structure

### 용어 정리
- de facto : 사실상 표준, 밑에서의 표준
- standard : 위에서의 표준
- recommendation : 만든 사람은 추천, 받아드리는 사람은 표준

- domestic specific 언어 : 매트랩같이 특정 영역에 전문성을 가진 언어

## 속도가 빠른 원인 - 데이터 구조
ndarray는 데이터들의 주소가 기본적으로 연속적이고 head에 데이터 타입을 넣어서 다음값을 찾는 등의 연산이 없다.
다른 데이터 타입과 호환이 좋다. \_\_array__ 만 있으면 넘파이 데이터로 만들 수 있다.

## 속도가 빠른 원인 - Vectorization
데이터 크기가 작으면 넘파이로 변환하는 리소스가 더 커서 오히려 느린 경우가 있다. (배열 100개 이하)

numpy는 indexing과 slicing을 동시에 할 수 있다.
```
a = np.arange(25).reshape(5,5)
a[1] #=> array([4,5,6,7,8,9])
a[1,3:5] #=> array(8,9)
a[0,1] #=> 1

a[3:, [0,1,3]] #=> array([[15,16,18],
                        # [20,21,23])

a[2::2, ::2]    #=>array([[10,12,14],
                        # [20,22,24]])
# A[start:end:step]
# 2차원까지는 둘이 같다.
a[1,...]
a[1,:]
a = np.arange(24).reshape(2,3,4)
print(a[1,1,1])
print(a[:,:,3] == a[...,3])
```

# 220921
파이선은 기본적으로 type conversion 문법이 없다. 
명시적 변환 => 새롭게 생성
a = [1,2,3,4]
set(a)
=> {1,2,3,4}

```
import numpy as np
b = np.array([1,2,3])
# c언어 스타일 : 속도를 위해 c로 만든 부분이 많기때문
b.astype('float32') # type casting
```
## predicated function : 참/거짓을 반환하는 함수
issubclass, isinstance
```
np.fromfunction(lambda x,y: x+y, (2,2))

import pandas as pd
pd.DataFrame.from_dict()

# stride를 이용해 연산을 더욱 빠르게 하는 기법
np.lib.stride_tricks

import scipy
from scipy.ndimage import convolve
from scipy.ndimage import concolve2d
from scipy.cluster import hierarchy

a = np.array([1,2,3], dtype=np.uint8)
a + 256
=> array([257,258,259], dtype=uint16)
# 파이선은 타입 오버플로운 없이 타입 사이즈를 늘려준다.
np.add(a,256)
=> array([1,2,3], dtype=uint8)
```
넘파이에서 매트릭스를 다룰때 제일 주의할 것
데이터 타입과 shape
```
np.lookfor('convolution')
np.info
np.iinfo('int32')
=>min=-214, max=214
```

## interning : 자주 쓰는 값들은 특정 메모리에 미리 넣어 두고 쓰는 기법
```
import sys
sys.intern
```

# mixed precision : 딥러닝 모델을 압축시키는 기법

# structured array : 자신만의 datatype을 만드는 것
```
x = np.rec.array([('Rex', 9, 81.0), ('Fido', 3, 27.0)],
            dtype=[('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])
x[0]        =>('Rex', 9, 81.0)
x['name']   =>array(['Rex', 'Fido'], dtype='U10')
x.name      => .rec 를 붙여서 레코드 어레이로 만들면 다음과 같은것이 가능
```
table 기반 데이터를 만들 수 있다.

# indexer : pandas에서 

# 220922
# pandas : 파이선을 돌리는 엑셀

### fs.open으로 하면 문자열로 불러온다

tidi data: 연월날짜가 그냥 숫자 등으로 되어 있는 경우 날짜 전용 데이터로 변형하는 것

# pandas가 메인 데이터로 다루는 dataframe에서
첫줄은 header
왼쪽 첫줄은 indexer

dict의 테크닉컬한 활용
b.get('x',3)

# 220926
# tidy data
1. 각 변수는 column
2. 각 관측값, 결과값은 row
3. 각 관측값, 결과값의 종류에 따라 테이블을 만든다