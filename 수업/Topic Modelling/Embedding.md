# 221128
# Embedding : data를 컴퓨터가 이해할 수 있는 숫자(int, float 등)로 변환하는 것 
- Language Model : 자연어를 컴퓨터가 이해할 수 있게 만드는 방법. N-gram이 가장 간단한 모델이다.   P(t3|t1,t2) -> NNLM

## NNLM 
t1
t2       X       W_1       tanh    W_2    Softmax
...
tn
Vector(one-hot)                          Vector(one-hot)              
N * N            N * Dim        Dim * N
- Lookup table 은 순서, 시계열이 아님 -> 각 배열이 독립적이라는 가정으로 출발해 만들어진 방법이기 때문

# W2V(google, 2015) : 단어 -> 벡터 -> NN의 초깃값 만들기
NNLM에서 tanh빼고, window size 내의 단어와 이외의 단어를 찾는 모델로 변경
   
CBOW <-> Skip-gram은 구조가 서로 반대
- SVD가 언어모델로 좋지만 못 씨는 이유 : 모든 단어를 메모리에 올릴 수 없고, 연산량이 어마어마함

## CBOW(continuous bag-of-words)
... W_t-2, W_t-1, W_t, W_t+1, W_t+2, ... 
    window size   center

Input         Hidden     Output
O               |  |     
O        W1     |  |      W2
O               |  |
N*N  N*Hidden Hidden*1  Hidden*N
$\frac{\partial L}{\partial \bar{Y}} \frac{\partial \bar{Y}}{\partial w_2} = w_2$
$\frac{\partial L}{\partial \bar{Y}} \frac{\partial \bar{Y}}{\partial Hidden} \frac{\partial Hidden}{\partial w_1} = w_1$

- Lookup table 특징을 이용한 변환
Input         Hidden     Output
O                    
O        W1     (+)      W2
O               
N*N  N*Hidden Hidden*1  Hidden*N
$\frac{\partial L}{\partial \bar{Y}} \frac{\partial \bar{Y}}{\partial w_2} = w_2$
$\frac{\partial L}{\partial \bar{Y}} \frac{\partial \bar{Y}}{\partial w_1} = w_1$

w1 = np.random.rand(N,H), win = 2
w2 = np.random.rand(H,N), Docs => t2i, i2t

## Skip-Gram
                       -> O
x       ->        O    -> O
one-hot                -> O ->multi-hot
(1,N)   (N,H)   (1,H)  (H,N) (1,N)

## Negative Sampling : N이 항상 겁나 크다. Mask : 이진분류로 바꿈
w1   H             w2    N
N (3     )         H  (      )
  (      )            (      )
win_siz에 있는가 없는가
3 O(vector)   *    1 O(vector)  = scalar -> 1
17 O(vector)  *                 = scalar -> 0