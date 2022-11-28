import numpy as np
import array

a = np.array([1,2,3], dtype=np.int32)
# 훨씬 c언어스러운 타입을 가진다. int16, int64 등 # perfomance를 높이는 요소
print(a, type(a), a.dtype)  # 기본 정수 데이터 타입은 int32라 따로 보여주지 않는다.
#numpy.ndarray : class명을 타입명처럼 만듬 # factory method

# 같은 데이터 타입으로 이루어짐
#x = array.array('i', [1.,2,3,4])
x = array.array('i', [1,2,3,4])


a = np.arange(24).reshape(2,3,4,1)
print(a, a.dtype, a.shape, a.ndim, a.itemsize, a.size)
# a라는 np.array의 데이터 구조를 알게 도와주는 것들, .dtype, .shape, .dim, .itemsize, .size

a = np.arange(25).reshape(5,5)
a[1] #=> array([4,5,6,7,8,9])
a[1,3:5] #=> array(8,9)
a[0,1] #=> 1

a[3:, [0,1,3]] #=> array([[15,16,18],
                        # [20,21,23])

a[2::2, ::2]    #=>array([[10,12,14],
                        # [20,22,24]])
# 2차원까지는 둘이 같다.
a[1,...]
a[1,:]
a = np.arange(24).reshape(2,3,4)
print(a[1,1,1])
print(a[:,:,3] == a[...,3])
import tensorflow as tf
# hold out
# (X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()
# print(X_train[0, ...] == X_train[0])

a = np.arange(48).reshape(3,4,4)
# print(a[...,2], a[0:2,1:3,1])
np.zeros((2,3)), np.ones((2,3))
np.full((3,3), 5), np.eye(4, k=-1), np.identity(3)
np.tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], 1)
np.triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], 1)

# 행렬곱을 하고 싶으면 shape이 같아야 한다.
a = np.array([[1,2],[3,4]])
# broadcating 기법, 모양이 다를 때 모양을 맞춰주는 기법, 연산 속도도 빠르다
# 한 쪽의 차원이 1일 때 그 차원을 복사해서 늘려주어 계산을 할 수 있게 shape을 맞춰주는 기법
print(a + 3)
a + np.array([1,2])

a = np.array([1,2,3])
b = np.array([2,3,4])
np.dot(a,b)
a.dot(b)
a.__matmul__(b)

aa = np.array([[1,2],[3,4]])
bb = np.array([[1,2],[3,4]])
# 행렬곱
np.dot(aa,bb)
aa@bb

aaa = np.mat([[1,2],[3,4]])
bbb = np.mat([[1,2],[3,4]])
print(aaa*bbb)

# array에서는 *로 element wise 곱이 가능하고, @로 행렬곱이 가능한데
# mat에서는 *가 행렬곱이다.

# ufunc 타입에 상관없이 같은 연산이 가능한 연산자
a = np.arange(10)

a.reshape(2,5)
np.reshape(a,(2,5))

## 파이선 관례상 실행했을때 output(return)이 없으면 자기 자신이 변경된다.
## 반대로 return 이 있으면 보통 바뀌지 않는다.

a = np.array([[1,2],[3,4]])
b = a
b[0,0] = 100
b = a.copy()    # numpy의 copy는 기본적으로 deep copy # view 가 shallow copy

b = a.flat
next(b)

a.flatten() # copy
a.ravel()   # view

a = np.array([1,2,3])
b = np.array([4,5,6])
np.concatenate((a,b), axis=0)

aa = np.array([[1,2,3]])
bb = np.array([[4,5,6]])
np.concatenate((aa,bb), axis=1)

# 한 차원을 높여서 붙여줌
np.stack([aa,bb])

a = np.array([[1,2],[3,4]])
a.reshape(1,2,2)
a.reshape(2,1,2)
a.reshape(2,2,1)

np.expand_dims(a,0)

a[None] == a[None,...]
a[:,None,:]

np.newaxis == None

np.vstack((aa,bb))
np.hstack((aa,bb))
np.column_stack((aa,bb))

np.r_[aa,bb]
np.c_[aa,bb]

# 자르기, 차원 낮추기
a = np.arange(36).reshape(4,9)
np.vsplit(a,2)
np.hsplit(a,3)
np.split(a,2, axis=0)
# 1 보다 작을때 1,2 사이일때, 2 이상일때
np.split(a,(1,2), axis=0)

