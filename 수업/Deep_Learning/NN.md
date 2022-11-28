# 221013
# Hypothesis : 가설
true function, target function과 비슷하다고 믿을만한 어떤 function. 
스팸 분류의 경우, 스팸과 아닌 것을 분류하는 규칙이 그러한 역할을 할 것이다.

# Model
기계학습 분야에서 가설과 모델은 서로 바꿔 쓸 수 있는 것처럼 사용한다. 다른 과학 분야에서는 그 둘이 다른 의미를 가진다.
가설은 과학자가 제시하는 "educated guess"이고 모델은 이 가설을 증명하기 위한 방법이다.

hypothesis ~ model ~ sckit-learn : estimator
algorithm : 특정 데이터로 학습시키기 이전에는 알고리즘, 학습 시킨 후에는 모델이라고 부른다.

# algorithm의 종류
## Linear vs. Non-Linear
## Generative vs. Discriminative
## Black box vs. descriptive
## First-principle vs. data-driven
## Stochastic vs. deterministic
## Flat vs. hierarchial
## Parametric vs. Non-parametric

# statistical modelling
## data modelling
y와 x의 관계를 설명하는 함수를 알고 있을때, 이 함수의 정확한 표현을 해주는 parameter를 찾는 연구.

## Algorithmic modelling
데이터의 특성에 맞게 알고리즘을 직접 구성한다. 정확도 예상하는 것으로 성능을 측정한다.

# Perceptron
뉴런의 모델링
 y= Phi(Weight*Xinput + bias) : Phi(action function)

perceptron을 포함한 linear 알고리즘의 결정적인 문제 - XOR 문제를 해결할 수 없다.

# MLP(multi layered perceptron)
input layer -> hidden layer -> output layer의 구조를 가진다.
기억 용량(memoraization capacity):layer와 그 안에 들어가는 perceptron이 많으면 많을 수록 좋다.

cf) 예측 (feed forword), 학습 (feedback)

# Activation function
NN의 성능을 올려주는 핵심 영역. 그래서 NN의 성능을 올리려면 Layer(Activation function의 연산)의 수를 늘리면 된다.
합성함수를 통해 데이터 셋의 space를 차원변환(외곡)하여 최종적으로 linear classification을 할 수 있게 만드는 것이 목표이다.

# UAT(Universal Approximation Theorem) : NN의 layer를 확장하면 모든 형태의 classification을 가능케하는 함수를 만들 수 있다.
NN이 각광받는 이유

# NN 학습법
objective function or loss function을 최소화하는 것. 최적화 문제
1. 미분 가능한 학습 방법 : 최종 합성 함수가 미분가능한 함수일 경우, dy/dx = 0인 지점이 locally 최소/최대인 지점이다. 
   실제 뉴런의 활동처럼 sigmoid function을 활용했었다. 단점: 저 함수 자체가 미분하기 귀찮다.
   gradient descent으로 수학적으로 미분하기 힘든 함수를 CS적으로 미분하는 것처럼 해결 할 수 있었다.


# gradient descent : 미분을 CS에서 간략화(쪼개서) 계산하는 방법
임의의 위치에서 편미분한 결과(=그 점의 미분값)에 일정 learning rate만큼 곱해서 다음 위치를 탐색하다 보면 
local maxima/minima에 수렴한다는 원리에 의한 계산 방법

# Back propagation (1986)
loss(error)의 최소값을 구하기 위해 layer의 역순으로 최소값을 구해 나가면서 weight를 업데이트 하는 방법

# 딥러닝이 나오기 전 가장 큰 문제
gradient vanicing : activation function의 합성도(layer수)가 늘어날 수록 gradient값이 0을 수렴해 버린다.

# NN은 graph 형태의 구조체로 간주할수 있다. 바꿀 수 있다.

# loss function : 문제해결하고자 하는 방법(classification, regression 등)에 따라 해결하기 좋은 loss function이 따로 있다.
MSE : regression
ACE : classification