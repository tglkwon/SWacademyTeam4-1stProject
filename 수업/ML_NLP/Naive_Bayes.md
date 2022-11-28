# 221011
# Naive Bayes
one of supervised learning models

자연어 처리는 discrete classification(supervised), clustering(unsupervied)

## optimal classifier
오답을 낮추는 식으로 만드는 것이 bayes classifier

모든 조합을 다 알 수 있을 정도로 데이터를 모으는 것이 어렵다.
심지어 그만큼 데이터를 모으면 반대로 계산이 불가능할 정도로 큰 단위가 되어버린다.
이를 해결하기 위해 한 가지 가정을 한다.
## conditional independence : (계산의 편의성을 위해) 특정 조건 하에서 확률이 독립적이다라고 가정한다.
$$
P(X,Y) => P(X)P(Y)

f(X) = argmax_(Y=y) * P(Y=y) * PHI(P(X_i = x_i | Y = y))
$$

incorrrect probability estimates in MLE(Maximum Likelihood Estimation), 충분치 않은 데이터.
                                 in MAP(Maximum A Posterior), stupid prior

## laplace smoothing
확률이 0이 되는 경우(train data에 없는 것을 찾는 경우)에 대한 해결하기 위핸 수학적 테크닉
$$
P(t|c) = T / sum(T_t,c)
=> (T+1) / (sum(T_t,c)+1)
$$
