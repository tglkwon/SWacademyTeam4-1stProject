import pandas as pd
import seaborn as sns
import numpy as np
import csv

tips = sns.load_dataset('tips')
tips.iloc[0,0]
tips['size']
tips[['size', 'sex']]

# np.s_[2::2] # slice의 단축표현을 만들어준다

data = pd.read_csv('incheon_yeonsugu_covid.csv', encoding='cp949')
print(data.info())
data.head(10)
data.tail()
data.sample()

# with open('incheon_yeonsugu_covid.csv', newline='') as f:
#     t = csv.reader(f)
#
#     print(next(t))
#
#
# np.loadtxt('incheon_yeonsugu_covid.csv', skiprows=1, delimiter=',')
#
# np.genfromtxt('incheon_yeonsugu_covid.csv', skip_header=True, delimiter=',', dtype='int32')
#
# print(data.valuess)

import missingno
# print(dir(missingno))
missingno.matrix(data)

data[~data['사망자수'].isnull()]

data.describe()
data.boxplot()
# outlier 를 찾고 그 의미를 아는 방법 : boxplot

import seaborn as sns
iris = sns.load_dataset('iris')
# print(iris.datainfo(), missingno.matrix(iris))
# iris.boxplot()
pd.plotting.scatter_matrix(iris)

sns.pairplot(iris)

# Exploratory Data Analysis(EDA) 위까지의 과정

a = pd.DataFrame({'b': [1, 2, 3, 4, 5], 'c' : ['3','4','5','23','3']})
a.info()

iris['sepal_length']    # structured arrary
iris.sepal_length       # recode array
iris.select_dtypes('int64')
iris[iris.columns[:-2]]
iris[['sepal_length', 'petal_length']]

tips.dtypes
tips.select_dtypes('category')
tips.filter(regex='^t')

# rows
# iloc : 파이선 인덱스 뽑듯 쓰는것
iris.iloc[2:5]
# loc : label

t = data.sample(frac=0.2)
t.iat[1,1]
# t.at[4, '확진자 수']
t.iloc[2:4,3:5]

iris['x'] = 1

# np.append 1차원으로 펼치고 맨 뒤에 추가한다
a = np.array([1,2,3])
bb = np.array([[[1,2,3], [4,5,6]]])
ccc = np.array([[[1,2,3]]])
np.append(a,3)
np.append(bb,3)
np.append(ccc,3)

# iris.join()
pd.concat([iris, iris], ignore_index=True, axis=0)

# column 명 바꾸기
iris.rename({'sepal_length':'a'}, axis=1)
iris.rename(columns={'sepal_length': 'a'})
iris.rename(index={0:'a'})

# 지우기 drop
iris.drop('x', axis=1)
iris.drop(columns=['x', 'species'])
#iris.drop_duplicates # 중복 데이터 지우기

# sort
