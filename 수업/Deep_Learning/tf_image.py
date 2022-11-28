import tensorflow as tf
import PIL
from PIL import Image

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
print(X_train.shape)

# im_keras = tf.keras.datasets.imdb.load_data()
# tf.keras.preprocessing.image.img_to_array(im_kereas)

im = Image.open('../jsonWeb.jfif')
im.show()
# im.crop(())

from scipy import ndimage
import imageio
imageio.v2.imread('../jsonWeb.jfif')
ndimage