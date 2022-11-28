# 220927
# 데이터의 종류
nominal : 이름
ordinal : 순서가 있는 (s, m, b 크기 등)
interval : 순서에 간격이 규칙적인(날짜, 시간 등)
Ratio : 비율, 절대 기준이 있는 데이터
후자로 갈 수록 정보가 많고 좋은 데이터이다.

양을 나타내는 데이터와 질을 나타내는 데이터가 있다.
discrete 
continuous

# 데이터 관련 정의
정답값 : class or target : class는 코딩시 문제 생길 수 있으므로 target : 보통 y로 표현(vector)
Feature : attributes, dimensions, columns : 보통 X로 표현(matrix형태라서)

## 딥러닝이 나오게 된 이유
전통적 알고리즘들은 빅데이터 영역에서 다뤄질 것을 전제 하지 않았기에 생각지 못했던 단점이 있었다.
어떤 전통적 알고리즘들이라도 성능이 어느 한계에서 수렴하는 듯한 현상
plateau in performance가 나타난다.
딥 러닝이 더 큰 빅데이터을 널어서 전통적 알고리즘의 성능을 추월하면서 각광받게 되었다.

## 차원의 저주
데이터의 차원이 증가할 수록, 학습에 필요한 데이터의 개수가 기하급수적으로 늘어나는 문제
데이터의 양이 부족하면 모델이 학습이 덜 되서 데이터의 전체 모집단의 데이터를 입력했는데 결과값의 편차가 커지는 
overfitting이 나타난다.


# feature selection : filter, wrapper, embedded
차원의 저주를 덜하게 하는 역할이 있다.

# 데이터의 품질을 측정하는 방법
## 충분성 : 데이터의 양이 학습하기에 충분한지 알 수있다. : 러닝커브를 이용한다.
## 대표성 : sampling noise : 우연에 의한 대표셩이 없는 데이터 : sampling bias가 생길 수 있다.


# 221004
# 전처리
## Data Cleaning : 분석 과정에서 가장 중요한 것. data cleaning and formatting data에 거의 모든 시간을 쓴다.

## 가정 
1. 내가 확보한 데이터는 정답 데이터이다.

## optimistic bias(낙관적 편향) : 학습한 데이터를 가지고 모델의 성능을 측정하면 실제 성능보다 더 높게 측정한다.
## holdout : 데이터의 일부는 모델을 만드는데, 나머지는 성능을 측정하는 데 사용한다.
데이터를 쪼개서 테스트 데이터를 만드는건 좋지만 데이터의 양이 줄어들어 더 좋은 모델을 만들지 못한다. 처음 데이터의 양에 따라 잘 판단해야 한다.
### data shift : 데이터가 작으면 테스트 데이터를 뽑는 것에서 치우침이 발생할 수 있다.
stratify : 위 문제를 해결하기 위해 y의 값을 최대한 종류별로 뽑을 수 있다.

전처리에는 필수적인 전처리와 성능을 높히기 위한 전처리가 있다.
- 필수적인 전처리 : 모든 데이터는 숫자가 되어야 한다. sklearn에서 y가 문자일 때 지원하는 method가 몇몇개 있다.
missing data가 있으면 안된다.
encoding : 문자를 숫자로 바꾸는 것
  - label encoding : 각 y value들을 숫자 또는 리스트의 위치로 바꾸는 방법. 단점으로 labelling에 따른 순서와 크기가 영향을 줄 수 있다. 
  X의 값들을 수정하고 싶을 때 문제가 생기기 쉽다.
  - one-hot encoding : 순서가 없는 데이터 처리하기 좋다. 단점으로 차원의 저주에 걸리기 좋다. 변수의 종류 수만큼 column이 늘어난다.
- 성능을 높히기 위한 전처리 :  

# 221005
# No Free Lunch
"세상에 공짜는 없다"
무언가 얻기 위해 무언가 대가를 지불해야 한다.
1. 우리의 모델은 현실세계를 단순화한 것이다.
2. 단순화를 하기 위해 몇 가지 가정을 한 것들이 있다.(model bias)
3. 특정한 상황에서는 실패하는 경우가 존재한다.
"어떤 상황에서도 최고의 성능을 내는 모델은 존재하지 않는다."


# Overfitting : High variance, Low bias : 정확도가 오락가락한다. 학습데이터로 한 테스트와 테스트 데이터로한 테스트의 결과가 큰 현상.
underfitting : low variance, high bias의 해결책은 모델을 바꿔본다. 모델의 목적, 가정과 다른 데이터를 학습시켜서 생기는 현상.

# 오컴의 면도날: 더 쉬운 설명이 더 좋은 설명이다. simplist is the best

# 더 좋은 모델을 선택하기 위한 평가 방법: 정확도 이외에도 있다.

# 221006
# 1종 오류, 2종 오류 , Metric?
1. 1종 오류 : 틀린 것을 맞다고 할 확률
2. 2종 오류 : 맞는 것을 틀리다고 할 확률

예측 |  참    | 거짓
참   |       | 2종 오류 
거짓 | 1종오류 | 

- Recall or sensitivity : 실제 맞는 것 중에 맞춘 것
- Precision : 예측한 것 중에서 맞춘 것
- Accuracy : 예측이 정확한 경우 모두(참을 참으로, 거짓을 거짓으로 판단한 경우)

## Efficiency 속도의 문제
학습하는 데 걸리는 시간과 예측하는 데 걸리는 시간이 각각 문제가 된다.
딥러닝은 학습이 오래걸리지만 예측은 빠르다.
KNeighbor는 학습은 빠르지만 예측이 느리다.
시간을 측정하는 방법
```
import timeit
여러번 돌려서 성능(동작 시간)의 평균값을 찾아주는 방법
```

# 221007

# 상대적으로 큰 비율의 테스트 세트의 비관적 편향
- 테스트 세트의 크기를 줄이면
모델 성능 추정에 상당한 분산이 발생, 
훈련 세트에 있는 샘플과 테스트 세트에 있는 샘플에 의존적이기 때문, 
데이터를 리샘플링할 때마다 샘플 분포 통계를 변경
- 성능 추정은 물론 대부분의 분류와 회기의 지도 학습 모델은 데이터셋이 샘플링된 모집단을 대표한다고 가정
- 계층 샘플링은 데이터셋을 나눌 때 클러스터의 비율을 유지
특성에 내재된 샘플 통계값의 변화는 여전히 문제가 된다. 특히 작은 데이터셋으로 작업할 때 더욱 문제가 된다.

# 3-way해서 가장 좋은 hyperparameter를 찾고 다른 모델에서도 좋은 hyperparameter를 찾아서 비교해야 한다.
KNN 1등, LR 1등, DT 1등으로 결승전 해야한다.
최종적으로 hyper parameter와 모델은 결정했다면 모든 데이터를 다 넣어서 학습시킨다.

# Pipeline의 개념에는 어떤 전처리를 했을 때 성능이 좋을까라는 점이 포함된다.

# 221011
## overfit을 해결하는 방법
1. 더 많은 데이터를 구한다.
2. 차원의 저주에 걸린 경우면 상관관계가 떨어지는 변수를 제거한다.
3. regulazition으로 모델이 학습 데이터를 너무 잘 맞추지 못하게 한다.

# 221012
# feature selection
```
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
import seaborn as sns

data = load_wine(as_frame=True)
wine = data.frame


## 1. knowledge based feature selection : 지식 기반 특성 선택
# wine.info()

sns.heatmap(wine.corr(), annot=True)
plt.show()

# data leakage : y가 X_i에 포함되서 생기는 문제. 다중공선성(multicollinearity)


## 2. filtered feature selection : 변수와 목표간의 통계적 상관관계를 확인하여, 그 상관관계가 낮은 변수를 제거하는 방법

from sklearn.feature_selection import SelectKBest, chi2

skb = SelectKBest(chi2, k=7)
skb.fit_transform(wine.iloc[:,:-1], wine.target)
# vars(skb)
# dir(skb)

## 3. wrapper feature selection : 알고리즘을 함께 고려해서 상관관계를 확인함. 모든 알고리즘을 사용할 수는 없다.
from sklearn.feature_selection import RFE   # recursive feature elimenation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

rfe = RFE(DecisionTreeClassifier(), n_features_to_select=7)
rfe.fit_transform(wine.iloc[:,:-1], wine.target)

print(vars(rfe))

## 4. embeded feature selection : 알고리즘 자체가 변수의 중요도를 측정함
dt = DecisionTreeClassifier()
dt.fit(wine.iloc[:,:-1], wine.target)
print(dt.feature_importances_)

# 샘플이 iid라고 가정한다: indepencnt and identically distributed라고 가정
```
# ensemble technique
```
## bagging(bootostrap aggregation) : random sampling with replacement - overfitting을 줄일 수 있다.
#  boosting : random sampling with replacement and over weighted data
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
import pandas as pd
from sklearn.datasets import load_digits

bc = BaggingClassifier()

data = load_digits()
print(pd.DataFrame(data.data))
```
# 전통적인 ML에서 하는 기본적인 가정과 비정형 데이터의 문제
1. na, 빈 데이터가 없어야 한다.
2. 모든 데이터는 숫자로 처리해야 한다.
3. 모든 변수(차원, column)간 독립적이다.
정형 데이터와 비정형 데이터를 구분하는 테크닉 : columns의 순서를 바꿔도 문제가 생기기 않으면 정형데이터(column간 독립적임)

# y값(정답 데이터)가 없을 때 전통적인 ML이 해결하는 방법 : clustering


# 주제
## 목표 : 핵심 방법
고양이 꼬리 보고 (input) 고양이 기분 맞추기 (output)
- 머신러닝을 사용하지 않는 방식 : 도메인 지식이 제일 중요함: rule based
데이터 수집 (labeling) > 데이터셋 구축
- 기계학습
- 딥러닝

시스템화