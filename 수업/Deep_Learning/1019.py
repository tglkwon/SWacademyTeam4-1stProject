import tensorflow as tf
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split


tf.keras.models.Model

input_ = tf.keras.Input(shape=(28,28))
x = tf.keras.layers.Flatten()(input_)
x = tf.keras.layers.Dense(128)(x)
x = tf.keras.layers.Dense(10)(x)

model = tf.keras.models.Model(input_, x)
# model.summary()
## 멀티 인풋, 멀티 아웃풋

data = load_wine(as_frame=True)
wine = data.frame

X_train, X_test, y_train, y_test = train_test_split(wine, data.target)
input_ = tf.keras.Input(shape=(13,))
x = tf.keras.layers.Dense(128)(x)
x = tf.keras.layers.Dense(3)(x)
model = tf.keras.Model(input_, x)
# model.summary()

model.compile(loss=tf.keras.Categonicalcross)
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy())

# model.compile(loss='')
input_ = tf.keras.Input(shape=(13,))
x = tf.keras.layers.Dense(128)(x)
x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
model = tf.keras.Model(input_, x)

# regression.
input_ = tf.keras.Input(shape=(13,))
x = tf.keras.layers.Dense(128)(x)
x = tf.keras.layers.Dense(2, activation='softmax')(x)
x = tf.keras.layers.Dense(2, activation=tf.keras.activations.sigmoid)(x)

model = tf.keras.Model(input_, x)

# parameter 변경하는 법
# 1. 클래스에 직접 넣는다.T
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True))
# 2. 함수의 내부에 넣는 partial을 사용
from functools import partial
t = partial(tf.keras.losses.binary_crossentropys, from_logits=True)
model.compile(loss=tf.keras.losses.binary_crossentropys)
# 3. text로 넣으면 파라미터 변경 불가
model.compile(loss='binary_crossentropys')


model.compile(loss=tf.keras.losses.MeanSquaredError, optimizer='rmsprop')

model.fit