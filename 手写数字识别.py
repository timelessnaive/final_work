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
import functions

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


def main():
    app = wx.App(False)
    frame = window(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
