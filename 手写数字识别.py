# coding:utf-8

import tensorflow as tf
import numpy as np
import cv2
import mnist_backward
import mnist_forward
import matplotlib.pyplot as plt
import os
import UI
import wx


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
def pre_high(name,flag=-1,ifplt=0):
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
    (_, res1) = cv2.threshold(res, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #print(res1)

    if(flag==-1):
        (_, res1) = cv2.threshold(res, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        _+=10   #测试出来比otsu算法阈值高10更好
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


def application(path):
    #对路径下全部图形文件做识别
    #path = input("input the number of test pictures:")
    '''
    for root, dirs, files in os.walk(path):
        for fle in files:
            f_path = root + "\\" + fle
            testPicArr = pre_high(f_path)
            preValue = restore_model(testPicArr)
            print("The prediction number is:", preValue)
    return preValue
    '''
    testPicArr = pre_high(path)
    preValue = restore_model(testPicArr)
    return preValue


class window(UI.MyFrame1):
    def __init__(self,p):
        UI.MyFrame1.__init__(self,p)
    def main_button_click(self,event):
        path=self.m_textCtrl1.GetValue()
        self.m_textCtrl2.SetValue(str(application(path)))


def main():
    app = wx.App(False)
    frame = window(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
