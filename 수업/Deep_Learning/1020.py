import tensorflow as tf
# tf.keras.models.Sequential, Model
# tf.keras.layers
# tf.keras.losses
# tf.keras.callbacks

# 처음과 마지막 layer의 size, shape를 지정해야 한다.

# reshape
input_ = tf.keras.layers.Input(shape=(28,28))
x = tf.keras.layers.Flatten()(input_)
x = tf.keras.layers.Dense(32, activation='relu', kernel_initializer='glorot_uniform')(x)
x = tf.keras.layers.Dense(10, activation='softmax')(x)

model = tf.keras.Model(input_, x)
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['acc'])
model.summary()

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()


## 학습 저장하는/불러오는 법
# model.save_weights
# model.load_weights
# Netron으로 모델 구조 이미지화 할 수 있음
# model.save('sun.h5')

class MyCallback(tf.keras.callbacks.Callback):
    def on_predict_end(self, epoch, logs=None):
        t = f'{epoch}번째 epoch'
        tt = '{}번째 epoch'.format(epoch)
        print(tt)


# result = model.fit(X_train, y_train, batch_size=100, epochs=5, callbacks=[MyCallback()])
result = model.fit(X_train, y_train, batch_size=100, epochs=5, callbacks=[tf.keras.callbacks.ModelCheckpoint('{epoch}.ckp', save_weights_only=True)])

x = tf.Variable([1,2,3], dtype=tf.float32)
# gradient의 중간값을 저장하는 tape
with tf.GradientTape() as t:
    y = x*x

s = t.gradient(y, x, unconnected_gradients='zero')