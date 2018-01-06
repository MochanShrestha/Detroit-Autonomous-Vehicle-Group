
import tensorflow as tf
from tensorflow import keras

W = tf.Variable([.3], tf.float32)
b = tf.Variable([.2], tf.float32)
x = tf.placeholder(tf.float32)

linear_model = W*x + b

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    output = sess.run(linear_model, {x:[1, 2, 3, 4]})
    print(output)

    sess.run(W.assign_add([0.1]))
    output = sess.run(linear_model, {x:[1, 2, 3, 4]})
    print(output)
