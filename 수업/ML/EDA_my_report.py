# 221016 Raw data에 대한 EDA
# 나만의 reporting

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pandas_profiling
import sklearn_evaluation
from sklearn.model_selection import train_test_split


iris = sns.load_dataset('iris')
iris.rename({'species': 'target'}, axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(iris.iloc[:,:-1], iris.target)

def my_report(df):
    print('-----------------------------------------------')
    print('-                  Info                       -')
    print('-----------------------------------------------')
    df.info()
    print('-----------------------------------------------')
    # print(df.head())
    print(df['target'].value_counts())

report = pandas_profiling.ProfileReport(iris)
# plt.show()

sns.pairplot(iris, hue='target')
plt.show()

# sns.boxplot(iris.iloc[:,:-1], iris.target)
# plt.show()

# 기본적인 성능 측정 후 holdout을 쓸지 crossvalid를 쓸지 결정한다.

from sklearn.model_selection import learning_curve
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
# 최소한의 기준 정확도를 잡아주는 바보 모델
dm = DummyClassifier()
# smtAallsin
dm.fit(X_train, y_train)
print(dm.score(X_test,y_test))
np.arange(1, 11) / 10
knn = KNeighborsClassifier()
lg = LogisticRegression()

# 기준점 - imbalanced data
train_size, train_score, test_score = learning_curve(knn, iris.iloc[:,:-1], iris.target)

sklearn_evaluation.plot.learning_curve(train_score, test_score, train_size)
plt.show()



from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, knn.predict(X_test))

confusion_matrix(y_test, knn(X_test), normalize=False)

from sklearn.metrics import classification_report
classification_report(y_test, knn.predict(X_test))


from sklearn.model_selection import (cross_val_score, cross_validate,cross_val_predict)
# 동작 시간 측정하는 툴 중 하나
# knn, lg, SVG
x_valid = cross_validate(knn, iris.iloc[:,:-1], iris.target)
pd.DataFrame(x_valid).boxplot()
plt.show()

cross_val_predict(knn, iris.iloc[:,:-1], iris.target)

############# pipeline
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
SS = StandardScaler()
pipe = Pipeline([('std', SS), ('knn', KNeighborsClassifier())])
pipe.get_params()
knn = KNeighborsClassifier()
pipe.fit(iris.iloc[:,:-1], iris.target)
# 모델을 만들 때처럼 모델을 사용해야 한다. 전처리 과정 등 그래서 파이프라인 개념이 나온 것

cross_val_score(pipe, iris.iloc[:,:-1], iris.target)

make_pipeline(StandardScaler(), KNeighborsClassifier())