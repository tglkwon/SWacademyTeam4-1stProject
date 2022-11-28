import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

iris = sns.load_dataset('iris')
knn = KNeighborsClassifier(n_neighbors=3) # hyperparameter 세팅하는 가장 일반적인 방법
lr = LogisticRegression(n_jobs=-1) # -1 내가 가진 최대 컴퓨터 자원
knn.get_params()
lr.get_params()
knn.set_params(n_neighbors=7) # hyperparameter 세팅하는 방법 2

# 알고리즘 별로 중요한 변수가 있다.

X_train, X_test, y_train, y_test = train_test_split(iris.iloc[:,:-1], iris.species, test_size=0.1)

# hyper parameter를 찾을 때는 3-way 방식을 사용한다.
X_train,X_val,y_train,y_val = train_test_split(X_train, y_train)
###################################################################################################################
# sklearn에서 grid search cv라는 테크닉, 굳이 직접 만들어 쓰지 않는 이유 : 다른 알고리즘과 비교할 수 없다.
temp = []
for i in range(2,21):
    for j in ['uniform', 'distance']:
        for k in range(1,3):
            knn = KNeighborsClassifier(n_neighbors=i, weights=j, p=k)
            knn.fit(X_train,y_train)
            temp.append((i,j,k, knn.score(X_test,y_test)))

import pandas as pd
result = pd.DataFrame(temp, columns=['n_neighbors', 'weight','p','score'])
result.sort_values('score', ascending=False).head(10)
######################################################################################################################

from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(KNeighborsClassifier(), {'n_neighbors': range(2,21),
                                             'weight': ['uniform', 'distance'],
                                             'p': range(1,3)})
grid.fit(X_train, y_train)

# best estimator, params, score
print(grid.best_estimator_, grid.best_params_, grid.best_score_)

result = pd.DataFrame(grid.cv_results_)

# Hyper parameter를 찾은 후에 그 hyper parameter를 이용해서 다시 학습시킨다. X_train과 X_val을 합쳐서 다시 학습시킨다.
# 데이터가 아주 작지 않으면 일반적으로 데이터 풀이 커져도 성능이 유지된다.

from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
pipe = Pipeline([('preprocessing', LabelEncoder(), ('clf', KNeighborsClassifier()))])
pipe.get_params()

grid = GridSearchCV(pipe, param_grid=[{
                                    'clf': [KNeighborsClassifier()],
                                    'preprocessing': [StandardScaler(), MinMaxScaler()],
                                    'clf__n_neighbor': range(2,21)
                                    },{
                                    'clf': [LogisticRegression()],
                                    'preprocessing': [StandardScaler(), MinMaxScaler()],
                                    'clf__C': [1.0,2.0,3.0]
                                     }]
                    )

from sklearn import set_config
set_config(display='diagram')
from sklearn.utils import _estimator_html_repr