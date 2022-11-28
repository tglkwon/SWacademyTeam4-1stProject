# 문제 인식 : iris의 종류를 분류하시오
# 전통적 방법: 전문가를 불러서 각 종의 특징을 찾아내고 그 기준을 알고리즘으로 하며 구분한다.
## 기계학습 방법: 현재 있는 데이터에서 각 종의 비슷한 값들을 찾고 이를 기준으로 구분한다.
    # : 정답 (지도) - supervisor : 분류(classification)
    #                           : 예측하고자 하는 값이 실수면 regression
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston, load_diabetes, load_wine
data = load_boston()

import pandas as pd

boston = pd.DataFrame(data.data, columns=data.feature_names)
boston['target'] = data.target


# seaborn  한두 줄로 통계적 그래프를 그리게 해줌
import seaborn as sns
iris = sns.load_dataset('iris')
sns.boxplot(x='sepal_length', y='sepal_width', hue='species', data=iris)
sns.violinplot(data=iris, x='species', y='sepal_length')
sns.violinplot(data=iris, y='species', x='sepal_length', orient='h')
plt.show()
sns.swarmplot(data=iris, x='species', y='sepal_length')
plt.show()

mpg = sns.load_dataset('mpg')
mpg.boxplot(figsize=(10,5))
plt.show()

import mglearn
# mglearn.plot_scaling.plot_scaling()
# plt.show()

# standard scalar : Z = (X-min)/sigma
# MinMaxScalar : (X-min)/(Max-min)

