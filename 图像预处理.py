import tensorflow as tf
import mnist_backward
import mnist_forward
import os

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def mark(gray):
    gradX = cv2.Sobel(gray, cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, cv2.CV_32F, dx=0, dy=1, ksize=-1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
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

    #cv2.drawContours(gray, [box], -1, (0, 255, 0), 3)
    return ans


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
                print("No checkpoint file found")
                return -1


#opencv图像预处理
def pre_high(img,flag=-1,ifplt=1):
    #img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray=mark(gray)
    res = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
    (_, res1) = cv2.threshold(res, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #print(res1)
    if(flag==-1):
        (_, res1) = cv2.threshold(res, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #_+=10   #测试出来比otsu算法阈值高10更好
        (_, res1) = cv2.threshold(res, _, 1, cv2.THRESH_BINARY_INV)
    else:
        (_, res) = cv2.threshold(res, flag, 1, cv2.THRESH_BINARY_INV)
    im_arr = np.array(res1)
    #print(im_arr)
    #print(_)
    if(ifplt==1):
        plt.imshow(im_arr)
        plt.title('OPENCV')
        plt.axis('off')
        plt.show()
    nm_arr = res1.reshape([1, 784])
    nm_arr = nm_arr.astype(np.float32)
    #print(nm_arr)
    return nm_arr

path_head='D:/ACM/machine_learn/final_work/pic/testpic/test/'
path_tail='.png'
for i in range(1,10):
    path=path_head+str(i)+path_tail
    img=cv2.imread(path)
    p1=pre_high(img)
    print(restore_model(p1))


'''
path='D:/ACM/machine_learn/final_work/pic/testpic/6.png'
p1 = pre_high(path)
ans = restore_model(p1)
print(ans)
'''