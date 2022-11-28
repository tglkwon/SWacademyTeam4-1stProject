import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import visualkeras

# EDA : 데이터 탐색을 통한 분석
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

np.unique(y_train,return_counts=True)
plt.hist(y_train, width=0.5)
plt.show()

# preprocessing image skill 1. 차원을 맞춰준다. 1차원으로
# from sklearn.preprocessing import MinMaxScaler
# mm = MinMaxScaler()
#
# X_train = X_train.reshape(-1,28*28)
# X_test = X_test.reshape(-1,28*28)
# mm.fit_transform(X_train)

# 2. min max 이론 - X-m / M-n 그리고 이미지는 0~255의 범위를 가지기에
X_train = X_train / 255
X_test = X_test / 255

# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(128, input_shape=(28*28)),
#     tf.keras.layers.Flatten()
# ])
model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(10))

# softmax 마지막 레이어의 결과를 0,1사이의 확률로 표시해서 해석하기 좋게 만들어주는 방법

# model을 어떻게 구성했는지 확인하는 방법들
model.summary()
model.weights
model.layers
model.get_config()


visualkeras.layered_view(model, min_xy=40, min_z=40 ,legend=True).show()

# graph 구조로 만들어줌
# model.compile(loss=, optimizer='adam', metrics=)
# metrics에서 accuracy, precision 등 계산하게 할 수 있다.
