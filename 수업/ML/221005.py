import matplotlib.pyplot as plt
import seaborn as sns
import missingno as mino

mpg = sns.load_dataset('mpg')
# 빈 값을 채우는 방법
# mpg[mpg.horsepower.isna()]
mpg[['horsepower']].boxplot()
plt.show()
mino.matrix(mpg)
plt.show()
# 평균값으로 넣는다.
mpg.horsepower.mean()
# 주변값(앞(pad, ffill), 뒤(backfill, bfill))으로 넣는다.
mpg.horsepower.fillna(method='bfill')

from sklearn.impute import SimpleImputer, KNNImputer
sImputer = SimpleImputer()
kn = KNNImputer()
sImputer.fit_transform(mpg[['horsepower']])
kn.fit_transform(mpg.select_dtypes('number'))

from sklearn.datasets import load_wine

data = load_wine(as_frame=True)
wine = data.frame
print(wine.info())

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

X_train, X_test, y_train, y_test = train_test_split(wine.iloc[:,:-1], wine.target, stratify=wine.target)
knn = KNeighborsClassifier()
knn.fit(X_train,y_train)
print('KNeighborsClassifier train data score: {}'.format(knn.score(X_train,y_train)))
print('KNeighborsClassifier test data score: {}'.format(knn.score(X_test,y_test)))

from sklearn.linear_model import LogisticRegression
logisticRegression = LogisticRegression()
logisticRegression.fit(X_train, y_train)
print('logisticRegression train data score: {}'.format(logisticRegression.score(X_train, y_train)))
print('logisticRegression test data score: {}'.format(logisticRegression.score(X_test, y_test)))


import mglearn
mglearn.plot_cross_validation.plot_cross_validation()
plt.show()

cross_val_score(knn, wine.iloc[:,:-1], wine.target).mean()

# cross_val_score(logisticRegression.plot)

from sklearn.naive_bayes import GaussianNB
g  = GaussianNB()

# hyperparameter tuning : 모델의 성능을 최적화 하는 파라미터 값을 찾는다.
# hyperparameter에 따라 성능이 달라진다
kn3 = KNeighborsClassifier(n_neighbors=3)
kn4 = KNeighborsClassifier(n_neighbors=4)
kn5 = KNeighborsClassifier(n_neighbors=5)
kn6 = KNeighborsClassifier(n_neighbors=6)

kn3.fit(X_train, y_train)
kn4.fit(X_train, y_train)
kn5.fit(X_train, y_train)
kn6.fit(X_train, y_train)

print(kn3.score(X_test, y_test), kn4.score(X_test, y_test), kn5.score(X_test,y_test), kn6.score(X_test,y_test))

temp = []
for i in range(3,21):
    knn = KNeighborsClassifier(i)
    knn.fit(X_train, y_train)
    temp.append((i, knn.score(X_test, y_test)))


