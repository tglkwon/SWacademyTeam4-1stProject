import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import pandas as pd
data = load_wine(as_frame=True)

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)
input_ = tf.keras.Input(shape=(13,))
x = tf.keras.layers.Dense(64)(input_)
x = tf.keras.layers.Dense(3, activation='softmax')(x)
model = tf.keras.Model(input_, x)


class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        print(epoch+1)
        print('집에 가고 싶다')

class MyLayer(tf.keras.layers.Layer):
    pass



model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['acc'])
hist = model.fit(X_train, y_train, batch_size=30, epochs=5, validation_split=0.2, callbacks=[MyCallback()])
# callbacks 에 tf.keras.callbacks.CSVLogger('sun') CSV 저장하기, tf.keras.callbacks.TensorBoard()형 데이터로 저장하기 등 여러가지로 저장할 수 있다.

pd.DataFrame(hist.history).plot.line()
plt.show()


