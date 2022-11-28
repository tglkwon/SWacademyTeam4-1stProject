#  cpu, gpu를 효율적으로 처리하는 data format은 무엇일까 - scheduling
import tensorflow as tf

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

tf.data.Dataset.from_tensor_slices((X_train, y_train))

class MyModel(tf.keras.Model):
    def __init__(self):
        # super는 상속 쳬계 문제르 해결해주는 기능
        super().__init__()
    def call(self):
        pass
    # call 만 수정하면 되게 미리 만들어놓음 call
    # def build(self, input_shape):
    #     pass
    # def __call__(self, *args, **kwargs):
    #     self.build()
    #     self.call()