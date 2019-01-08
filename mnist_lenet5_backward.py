#coding:utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_lenet5_forward
import os
import numpy as np

batch = 100
base_rate =  0.005 
decay_rate = 0.99 
regular = 0.0001 
step = 50000 
moving_ave = 0.99 
save_path="./model2/"
model_name="mnist_model" 

def backward(mnist):
    x = tf.placeholder(tf.float32,[
    batch,
    mnist_lenet5_forward.imgxy,
    mnist_lenet5_forward.imgxy,
    mnist_lenet5_forward.cen]) 
    y_ = tf.placeholder(tf.float32, [None, mnist_lenet5_forward.outnode])
    y = mnist_lenet5_forward.forward(x, True, regular) #调用前向传播过程
    global_step = tf.Variable(0, trainable=False) 

    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))#对输出层的输出求取某一类的概率，返回这一概率与实际label的交叉熵
    cem = tf.reduce_mean(ce) #求上面返回的交叉熵的平均值
    loss = cem + tf.add_n(tf.get_collection('losses'))#

    learning_rate = tf.train.exponential_decay( 
        base_rate,
        global_step,
        mnist.train.num_examples / batch, 
        decay_rate,
        staircase=True) 
    
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    ema = tf.train.ExponentialMovingAverage(moving_ave, global_step)
    ema_op = ema.apply(tf.trainable_variables())#实现滑动平均模型
    with tf.control_dependencies([train_step, ema_op]): 
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()
    with tf.Session() as sess: #创建会话
        init_op = tf.global_variables_initializer() 
        sess.run(init_op)
        for i in range(step):
            xs, ys = mnist.train.next_batch(batch) 
            reshaped_xs = np.reshape(xs,(  
            batch,
            mnist_lenet5_forward.imgxy,
            mnist_lenet5_forward.imgxy,
            mnist_lenet5_forward.cen))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys}) 
            if i % 100 == 0: 
                print("%d %g." % (step, loss_value))
                saver.save(sess, os.path.join(save_path, model_name), global_step=global_step)

def main():
    mnist = input_data.read_data_sets("./data/", one_hot=True) 
    backward(mnist)

if __name__ == '__main__':
    main()


