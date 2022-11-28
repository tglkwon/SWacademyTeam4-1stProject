import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris

mlp = MLPClassifier()
a = tf.constant([1,2,3])
b = tf.Variable([1,2,3])
## tensorflow의 특징
# 1. immutable data가 기본
# 2. gpu 지원
c = np.array([1,2,3])

print(tf.add(c,c), np.add(a,a))
# tensor로 변형 후 연산(resource가 든다)
# tensor 나 sklearn등 numpy 계열 framework 자료를 numpy 연산시킬 때는 리소스가 덜 든다.


data = load_iris()

mlp.fit(data.data, data.target)
print(mlp.score(data.data, data.target))

# composition 합성함수
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(4,)),
    tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
    tf.keras.layers.Dense(3)
])

# feed forward, predict
model(data.data)

# 관례상 layer당 perceptron 수를 2의 배수로 한다. 분할 연산을 고려한 결과
model.summary()

# layer와 그 perceptron 수를 정하는 방식이 2~3가지있다.
# tensorflow 2.0 keras
tf.keras.activations.relu
tf.nn.relu

print(tf.keras.utils.to_categorical(data.target))

# (실제값 - 예측값) = error(loss, or cost)가 최소가 되게 하는 문제해결 방식 = optimazation

model.compile(loss=tf.keras.losses.MeanSquaredError())
history = model.fit(data.data, data.target, epochs=10)

import pandas as pd
pd.DataFrame(history.history).plot.line()
plt.show()