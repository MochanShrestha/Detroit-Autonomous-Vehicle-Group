
import tensorflow as tf

a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)

c = a + b

with tf.Session() as sess:
    output = sess.run(c, {a: [1.0, 2.0], b:[3.0, 4.0]})
    print(output)