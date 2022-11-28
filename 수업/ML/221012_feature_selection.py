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
