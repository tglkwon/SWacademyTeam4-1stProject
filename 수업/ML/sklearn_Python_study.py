from sklearn.neighbors import KNeighborsClassifier
# 거리 기반으로 가까운 점들을 찾는 방식
import seaborn as sns
# import numpy as np
iris = sns.load_dataset('iris')

knClassifier = KNeighborsClassifier()
# hyperparameter
knClassifier.fit(iris.iloc[:,:-1], iris.species)
knClassifier.predict([[6,3,5,2]])

mpg = sns.load_dataset('mpg')
mpg_new = mpg.drop(['horsepower', 'origin', 'name'], axis=1)

from sklearn.neighbors import KNeighborsRegressor
# 연비를 예측하는 모델링
knRegressor = KNeighborsRegressor()
knRegressor.fit(mpg_new.iloc[:,1:], mpg_new.mpg)

# 제조년을 예측하는 모델링
model_year = KNeighborsClassifier()
model_year.fit(mpg_new.iloc[:,:-1], mpg_new.model_year)
model_year.predict([[21,4,120,2800,20]])

from sklearn.model_selection import train_test_split
# len(train_test_split(iris))
train, test = train_test_split(iris)
# 원본 데이터를 랜덤하게 섞어서 75%, 25%로 나누었다.

# train, test data sampling/split
import numpy as np
import pandas as pd

train_iris = iris.sample(118)
set = set(iris.index) - set(train.index)
test_iris = iris.iloc[list(set)]

knn = KNeighborsClassifier()
knn.fit(train.iloc[:,:-1], train.species)
knn.predict(test.iloc[:,:-1]) == test.species.values

X_train, X_test, y_train, y_test = train_test_split(iris.iloc[:,:-1], iris.species, stratify=iris.species)
# y_test.value_counts() 로 종류별로 잘 나누어졌는지 알 수 있다.

from sklearn.datasets import load_wine
# load_data 데이터 크기가 작은
# fetch
data, target = load_wine(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(data, target, stratify=target)

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print(knn.score(X_test,y_test), (knn.predict(X_test) == y_test.values).sum())


# StandardScaler 로 데이터 스케일링
from sklearn.preprocessing import StandardScaler, MinMaxScaler
ss = StandardScaler()
mm = MinMaxScaler()

# ss.fit(data[['proline']])
# ss.transform(data[['proline']])
data['proline'] = ss.fit_transform(data[['proline']])

X_train, X_test, y_train, y_test = train_test_split(data, target, stratify=target)
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print(knn.score(X_test,y_test), (knn.predict(X_test) == y_test.values).sum())

# MinMax로 스케일링
data = load_wine(as_frame=True)
wine = data.frame
wine['proline'] = mm.fit_transform(wine[['proline']])

X_train, X_test, y_train, y_test = train_test_split(wine.iloc[:,:-1], wine.target, stratify=wine.target)
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print(knn.score(X_test,y_test), (knn.predict(X_test) == y_test.values).sum())


# labelling encoding
iris.species.map({'setosa':0, 'versicolor':2, 'virginica':5})

# pandas에서 다루는 방법 : category
iris['species'] = iris.species.astype('category')
iris.species.cat.codes

# sklearn label encoding
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
# 순서가 없는 데이터 encoding
label = LabelEncoder()
le = label.fit_transform(iris.species)
label.inverse_transform([0,1,2])
le[:,np.newaxis]

# 순서가 있는 데이터 encoding
oe = OrdinalEncoder()
oe.fit_transform(iris[['species']])

# one-hot encoding
iris.species.str.get_dummies()
pd.get_dummies(iris.species)
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder()
one_hot = ohe.fit_transform(iris[['species']])
one_hot.toarray()
print(one_hot)

# mpg로 encoding해보자
import tensorflow as tf
tf.keras.utils.to_categorical(le)
# to_categorical : label encoding => one-hot encoding
le = LabelEncoder()
# le.fit_transform(mpg['origin', 'name'])

# true false를 1 0 으로 바꾸는 꼼수
mpg['usa'] = mpg.origin == 'usa'*1

# for _ in mpg.origin.value_counts():
#     mpg[_] = mpg.origin == _*1