
import tensorflow as tf

a = tf.constant(3.0, tf.float32)
b = tf.constant(4.0)
c = tf.multiply(a,b)

#print(node1 + node2)

#sess = tf.Session()
#print (sess.run([node1 + node2]))
#sess.close()

with tf.Session() as sess:
    output = sess.run(c)
    print(output)