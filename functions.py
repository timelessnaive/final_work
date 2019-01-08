import tensorflow as tf
import numpy as np
import cv2
import mnist_backward
import mnist_forward
import mnist_lenet5_forward
import mnist_lenet5_backward
import matplotlib.pyplot as plt

def restore_model_lenet5(testPicArr):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32, [
            1,
            mnist_lenet5_forward.imgxy,
            mnist_lenet5_forward.imgxy,
            mnist_lenet5_forward.cen])
        #y_ = tf.placeholder(tf.float32, [None, mnist_lenet5_forward.outnode])
        y = mnist_lenet5_forward.forward(x, False, None)
        ans = tf.argmax(y, 1)
        ema = tf.train.ExponentialMovingAverage(mnist_lenet5_backward.moving_ave)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)

        #correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(mnist_lenet5_backward.save_path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)

                reshaped_x = np.reshape(testPicArr, (
                    1,
                    mnist_lenet5_forward.imgxy,
                    mnist_lenet5_forward.imgxy,
                    mnist_lenet5_forward.cen))
                ans = sess.run(ans, feed_dict={x: reshaped_x})
                return ans
                #print(ans)
            else:
                print('没有找到模型')
                return

def restore_model(testPicArr):
    with tf.Graph().as_default() as tg:
        x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
        y = mnist_forward.forward(x, None)
        preValue = tf.argmax(y, 1)

        variable_averages = tf.train.ExponentialMovingAverage(mnist_backward.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(mnist_backward.MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)

                preValue = sess.run(preValue, feed_dict={x: testPicArr})
                return preValue
            else:
                print("没有找到模型")
                return -1

def mark(gray,flag=-1):#输入必须是一张灰度图
    if(flag==-1):
        gradX = cv2.Sobel(gray, cv2.CV_32F, dx=1, dy=0, ksize=-1)#计算x方向上的算子
        gradY = cv2.Sobel(gray, cv2.CV_32F, dx=0, dy=1, ksize=-1)#计算y方向上的算子
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
    else:
        gradient=gray
    #cv2.imshow('gray',gradient)
    blurred = cv2.blur(gradient, (9, 9))
    #cv2.imshow('blurred', blurred)
    #cv2.imshow('blurred', gray)
    (_, thresh) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closed0', closed)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    #cv2.imshow('closed', closed)
    (i, cnts, j) = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=lambda x: cv2.contourArea(x))
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    ans = gray[y1:y1 + hight, (x1 + width // 2 - hight // 2):(x1 + width // 2 + hight // 2)]
    #cv2.imshow('ans', ans)
    #cv2.drawContours(gray, [box], -1, (0, 255, 0), 3)
    return ans

#opencv图像预处理
def pre_high(img,mf=-1,flag=-1,ifplt=1):
    #img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray=mark(gray,mf)
    (_, res1) = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #cv2.imshow('res1', res1)
    res1 = cv2.resize(res1, (28, 28), interpolation=cv2.INTER_AREA)
    #res = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
    #(_, res1) = cv2.threshold(res, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #print(res1)
    im_arr = np.array(res1)
    #cv2.imshow('res1', res1)
    #print(im_arr)
    #print(_)
    if (ifplt == 1):
        plt.imshow(im_arr)
        plt.title('OPENCV')
        plt.axis('off')
        plt.show()
    nm_arr = res1.reshape([1, 784])
    nm_arr = nm_arr.astype(np.float32)
    cmp = np.zeros((28, 28, 1), np.uint8)
    cmp = cmp.reshape([1, 784])
    if((nm_arr==cmp).all()):
        #print('yes')
        raise ValueError
    #print(nm_arr)
    return nm_arr



