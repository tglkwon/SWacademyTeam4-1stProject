# Linear Regression

f = theta + sigma(theta_i * x_i)
두가지 특징 : 선형 weight sum(매트릭스 곱), 파라미터 theta

위의 식과 실제 결과 값의 차이 error를 가장 줄어드는 형태로 모델을 구성하게 된다.

당연히 한계가 있다.
이를 해결하기 위해
# multiple linear regression
f = sum(n)sum(m) * theta * phi * X

# sigmoid function, logistic function
bounded -1~1
differentiable 미분가능함
모든 실수에서 정의 가능한 구역에서 미분값이 양수 
$
f = 1/(1+\exp^-x)

logic function : logistic의 역함수

f = log(x/1-x)
$
