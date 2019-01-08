#coding:utf-8
import tensorflow as tf
imgxy = 28
cen = 1
c1_size = 5
c1_kernel = 32
c2_size = 5
c2_kernel = 64
fc_size = 512
outnode = 10

def get_weight(shape, regularizer):
    w = tf.Variable(tf.truncated_normal(shape,stddev=0.1))
    if regularizer != None:
        tf.add_to_collection('losses', tf.contrib.layers.l2_regularizer(regularizer)(w))
    return w

def get_bias(shape):
    b = tf.Variable(tf.zeros(shape))
    return b

def conv2d(x,w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def forward(x, train, regularizer):
    conv1_w = get_weight([c1_size, c1_size, cen, c1_kernel], regularizer)#初始化第一层卷积核与偏置
    conv1_b = get_bias([c1_kernel])
    conv1 = conv2d(x, conv1_w)#卷积运算
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_b))#将偏置后的卷积输出作为激活函数的输入
    pool1 = max_pool_2x2(relu1)

    conv2_w = get_weight([c2_size, c2_size, c1_kernel, c2_kernel],regularizer) 
    conv2_b = get_bias([c2_kernel])
    conv2 = conv2d(pool1, conv2_w) 
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_b))
    pool2 = max_pool_2x2(relu2)

    pool_shape = pool2.get_shape().as_list() 
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3] 
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes]) 

    fc1_w = get_weight([nodes, fc_size], regularizer) #全连接层初始化
    fc1_b = get_bias([fc_size]) #初始化偏置项
    fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_w) + fc1_b)#将原向量与权重做矩阵乘法，加上偏置后通过激活函数
    if train:
        fc1 = tf.nn.dropout(fc1, 0.5) #随机舍弃一半神经元，减小过拟合
    fc2_w = get_weight([fc_size, outnode], regularizer)
    fc2_b = get_bias([outnode])
    y = tf.matmul(fc1, fc2_w) + fc2_b
    return y