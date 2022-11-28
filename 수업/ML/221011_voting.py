import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns

data = load_breast_cancer(as_frame=True)
breast = data.frame

# breast.info()
# breast.describe()
# breast.target.value_counts()
sns.heatmap(breast.corr(), annot=True)
plt.show()

breast.boxplot(figsize=(10,5))
# plt.show()
# 전체 데이터가 outlier가 많다.

X_train, X_test, y_train, y_test = train_test_split(breast.iloc[:,:-1], breast.target, stratify=breast.target)

from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB, BernoulliNB, CategoricalNB, ComplementNB, MultinomialNB

rs = RobustScaler()

## 성능을 높이는- 방법, ensemble 여러 알고리즘을 조합하는 것
# - generative : naive bayes, bagging, boosting
# - non-generative : voting, stacking

# voting 예제 1
# voting = VotingClassifier([('knnn3', KNeighborsClassifier(n_neighbors=3)),
#                            ('knn5', KNeighborsClassifier(n_neighbors=5)),
#                            ('knn7', KNeighborsClassifier(n_neighbors=7)),
#                         ], voting='soft', weights=[2,1,3])


# voting.fit(X_train, y_train)
# voting.transform(X_test)
# # voting.get_params()
# grid = GridSearchCV(voting, {'weights', [[1,1,1], [1,2,3],[2,3,4]],
#                              'voting', ['soft', 'hard']})
# grid.fit(X_train, y_train)
#
# pd.DataFrame(grid.cv_results_).T

# voting 예제 2
# voting = VotingClassifier([('ber', BernoulliNB()),
#                            ('cate', CategoricalNB()),
#                            ('comp', ComplementNB()),
#                            ('gaus', GaussianNB()),
#                            ('mult', MultinomialNB()])
#                            ])
knn_pipeline = Pipeline([('knn', KNeighborsClassifier())])
lr_pipeline = Pipeline([('lr', LogisticRegression())])

# grid = GridSearchCV(voting, [{'knn_pipeline__knn': [KNeighborsClassifier(3),
#                                                     KNeighborsClassifier(4)]},
#                              {'lr__lr__C': [1,2,3]},
#                              {'weights': [[1,1,1]]}])
#
# grid.fit(X_train, y_train)
#
# pd.DataFrame(grid.cv_results_).T

voting = VotingClassifier([('knn_pipe', knn_pipeline),
                           ('lr', lr_pipeline),
                           ('nb', GaussianNB())], n_jobs=-1)
voting.fit(X_train, y_train)
voting.transform(X_test)
voting.estimators[0][1].steps[0][1]

from sklearn.model_selection import validation_curve
train_score, test_score = validation_curve(KNeighborsClassifier(), X_train,y_train, param_name='n_neighbors', param_range=range(2,8))

import sklearn_evaluation

sklearn_evaluation.plot.validation_curve(train_score, test_score, range(2,8))
plt.show()

# grid = GridSearchCV(voting, [{'knn_pipe__knn__n_neighbors': [2,3,4,5],
#                               'lr__lr__C': [1,2,3], 'voting':['soft', 'hard']}])
#
# grid.fit(X_train, y_train)
# pd.DataFrame(grid.cv_results_).T