from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

data = load_iris(as_frame=True)
iris = data.frame

# KMneans
km = KMeans(n_clusters=3)
km.fit_transform(iris.iloc[:,:-1])

# DBSCAN
dbscan = DBSCAN(eps=0.5)
dbscan.fit(iris.iloc[:,:-1])
print(dbscan.labels_)

# Agglogmerative Clustering : 가장 가까운 2개부터 묶어보면서 거리를 늘려가는 방식
agg = AgglomerativeClustering(n_clusters=3)
agg.fit(iris.iloc[:,:-1])
print(agg.labels_)

# pca
pca = PCA(3)
X = pca.fit_transform(iris.iloc[:,:-1])
X_train, X_test, y_train, y_test = train_test_split(X, iris.target)

knn = KNeighborsClassifier()

knn.fit(X_train, y_train)
print(knn.score(X_test,y_test))
