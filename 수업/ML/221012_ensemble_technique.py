## bagging(bootostrap aggregation) : random sampling with replacement - overfitting을 줄일 수 있다.
#  boosting : random sampling with replacement and over weighted data
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
import pandas as pd
from sklearn.datasets import load_digits

bc = BaggingClassifier()

data = load_digits()
print(pd.DataFrame(data.data))

import tensorflow as tf

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
# X_train.shape
# tf.keras.layers.flatten()(X_train)

(train_data, train_labels), (test_data, test_labels) = tf.keras.datasets.imdb.load_data()
print(train_data)