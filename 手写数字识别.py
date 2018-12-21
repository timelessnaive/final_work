# coding:utf-8


import cv2
'''
import tensorflow as tf
import mnist_backward
import mnist_forward
import matplotlib.pyplot as plt
import os
'''
import numpy as np
import UI
import wx
import functions
f = 0
f1 = 0
# img = np.zeros((512, 512, 3), np.uint8)


def draw_line(img):
    def draw_circle(event, x, y, flags, param):
        global f, f1
        # cv2.CV_EVENT_FLAG_LBUTTON
        if (event == cv2.EVENT_LBUTTONDOWN):
            f = 1
        elif (event == cv2.EVENT_LBUTTONUP):
            f = -1
        if (f == 1):
            cv2.circle(img, (x, y), 10, (255, 255, 255), -1)

        if (event == cv2.EVENT_RBUTTONDOWN):
            f1 = 1
        elif (event == cv2.EVENT_RBUTTONUP):
            f1 = -1
        if (f1 == 1):
            cv2.circle(img, (x, y), 10, (0, 0, 0), -1)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    while (True):
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            cv2.imwrite('img.png', img)
            break

    cv2.destroyAllWindows()
    # functions.pre_high(img,1)
    cv2.imshow('img', img)
    img=cv2.bitwise_not(img)
    testPicArr = functions.pre_high(img, 1)
    preValue = functions.restore_model(testPicArr)
    return (preValue)
    #print(preValue)
    # cv2.waitKey(0)


def application(path):
    '''
    # 对路径下全部图形文件做识别
    path = input("input the number of test pictures:")
    for root, dirs, files in os.walk(path):
        for fle in files:
            f_path = root + "\\" + fle
            testPicArr = pre_high(f_path)
            preValue = restore_model(testPicArr)
            print("The prediction number is:", preValue)
    return preValue
    '''
    img=cv2.imread(path)
    testPicArr = functions.pre_high(img)
    preValue = functions.restore_model(testPicArr)
    return preValue


class window(UI.MyFrame1):
    def __init__(self,p):
        UI.MyFrame1.__init__(self,p)
    def main_button_click(self,event):
        path=self.m_textCtrl1.GetValue()
        self.m_textCtrl2.SetValue(str(application(path)))
    def pic_plot(self,event):
        while (True):
            try:
                img = np.zeros((512, 512, 3), np.uint8)
                draw_line(img)
            except ValueError:
                #print('exit')
                break


def main():
    app = wx.App(False)
    frame = window(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
