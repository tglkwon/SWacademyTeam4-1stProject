from sklearn.datasets import fetch_openml
from sklearn.neighbors import KNeighborsClassifier
from sklearn import set_config

titanic, y = fetch_openml('titanic', version=1, as_frame=True, return_X_y=True)

titanic.drop(columns='name', inplace=True)
titanic.drop(columns=['cabin', 'boat', 'body', 'home.dest'], inplace=True)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ohe = OneHotEncoder(handle_unknown='ignore')
ohe.fit_transform(titanic[['sex']]).toarray()

str_num = Pipeline([('ohe', OneHotEncoder())])

from sklearn.impute import SimpleImputer
impute_std = Pipeline([('impute', SimpleImputer()), ('std', StandardScaler())])

pre = ColumnTransformer([('num', impute_std, ['pclass', 'age', 'sibsp', 'parch', 'fare']),
                         ('str', str_num, ['sex', 'ticket', 'embarked'])])

pipe = Pipeline([('preprocessing', pre), ('clf', KNeighborsClassifier())])
pipe.fit(titanic, y)