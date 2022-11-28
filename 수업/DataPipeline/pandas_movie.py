import pandas as pd

user = pd.read_csv('./ml-1m/users.dat', delimiter="::", header=None,
                   names=['UserID','Gender','Age','Occupation','Zip-code'])
movies = pd.read_csv('./ml-1m/movies.dat', encoding='latin1',sep="::", header=None,
                     names=['MovieID','Title','Genres'])
ratings = pd.read_csv('./ml-1m/ratings.dat', encoding='latin1',sep="::", header=None,
                      names=['UserID','MovieID','Rating','Timestamp'])

# user.rename(columns={0:'UserID', 1:'Gender', 2:'Age', 3:'Occupation', 4:'Zip-code'})
# user.info()
# user.Gender.describe()
# user.Gender.value_counts() # series에서만 쓸 수 있음   # 한 줄짜리 데이터프레임 => series라고 부른다

# join의 느낌으로 합치는 방법 # ratings.merge(movies).merge(user)
re_ratings = ratings.drop(columns='Timestamp')
# re_ratings.describe()
# re_ratings['Rating'].value_counts()

re_ratings.set_index('UserID').unstack()

# 첫번째 인자에 인덱스, 두번재 인자에 상관관계를 볼 다른 변수, 세번째 인자에 관계성을 나타내는 변수가 들어간다
temp = re_ratings.pivot('UserID', 'MovieID', 'Rating')
ratings_pivot = temp.fillna(0)

# stack : columns의 내용을 index로
re_ratings.set_index('UserID').stack()
recommendation = re_ratings.set_index(['UserID', 'MovieID']).unstack().fillna(0).T.corr()

# return nearest UserID to input UserID
def nearestUser(userID):
    # return recommendation[userID].sort_values(ascending=False).index[1]
    return recommendation[userID].nlargest(2).index[-1]

# nsmallist(n) 가장 작은 거 n개, default =5
# UserID가 본 영화 목록
def movieListUserID(userID):
    return ratings[ratings.UserID == userID].MovieID.values

# nearest는 보고 userID는 안 본 영화 목록
def movieRecommend(userID):
    near = nearestUser(userID)
    near_view = movieListUserID(near)
    my_view = movieListUserID(userID)
    return set(near_view) - set(my_view)

recommend3 = movieRecommend(3)
# recommendList = movies[movies.MovieID.isin(recomend3)]

# rating이 4이상인 영화 목록
temp = ratings[ratings.MovieID.isin(recommend3)]
recommendListRatingOver5 = temp[(temp.Rating == 5) & (temp.UserID == nearestUser(3))].MovieID.values
names = movies[movies.MovieID.isin(recommendListRatingOver5)]

# ratings.corr()

## 구글에 접속하는 함수

# 각 데이터의 값 분포를 보는 방법들
# import numpy as np
# import tensorflow as tf
# (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
# set(y_train)
# np.unique(y_train)
#
# import matplotlib.pyplot as plt
#
# plt.hist(y_train)

# index가 x축이다.