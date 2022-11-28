import tensorflow as tf
from scikeras.wrappers import KerasClassifier
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, GridSearchCV
import pandas as pd
import sklearn_evaluation


data = load_wine(as_frame=True)

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)
input_ = tf.keras.Input(shape=(13,))
x = tf.keras.layers.Dense(64)(input_)
x = tf.keras.layers.Dense(3, activation='softmax')(x)
model = tf.keras.Model(input_, x)
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy())

# sklearn에서 사용하는 방식을 모두 사용가능함
kc = KerasClassifier(model, epochs=5)
t = cross_val_score(kc, X_train, y_train)
train_size, train_score, test_score = learning_curve(kc, data.data, data.target)

sklearn_evaluation.plot.learning_curve(train_score, test_score, train_size)
plt.show()

# 특정 파라미터 바꾸는 꼼수 다시 확인하기 중대사항
grid = GridSearchCV(kc, {'model__dense__units': [32,64,128]})
grid.fit(data.data, data.traget)
print(pd.DataFrame(grid.cv_results_).T)