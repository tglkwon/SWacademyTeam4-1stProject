## 여러 모델이 예측한 결과값을 새로운 학습 데이터로 사용하고 이를 반복하여 새로운 모델을 만든다.
## kaggle 1등 들이 가장 많이 사용하는 테크닉. meta learning
import pandas as pd
from sklearn.ensemble import StackingClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline

data = load_breast_cancer(as_frame=True)
breast = data.frame
X_train, X_test, y_train, y_test = train_test_split(breast.iloc[:,:-1], breast.target, stratify=breast.target)
stack = StackingClassifier([('knn', KNeighborsClassifier()),
                            ('nb', GaussianNB())],
                           LogisticRegression())

stack.fit(X_train, y_train)
stack.score(X_test, y_test)

#
# knn_pipeline = Pipeline([('knn', KNeighborsClassifier())])
# lr_pipeline = Pipeline([('lr', LogisticRegression())])
#
# voting = VotingClassifier([('knn_pipe', knn_pipeline),
#                            ('lr', lr_pipeline),
#                            ('nb', GaussianNB())], n_jobs=-1)
# voting.fit(X_train, y_train)
# voting.transform(X_test)
# voting = VotingClassifier(stack)
# grid = GridSearchCV(voting, [{'knn_pipe__knn__n_neighbors': [2,3,4,5],
#                               'lr__lr__C': [1,2,3], 'voting':['soft', 'hard']}])
#
# grid.fit(X_train, y_train)
# pd.DataFrame(grid.cv_results_).

