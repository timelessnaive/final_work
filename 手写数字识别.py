# coding:utf-8
import cv2
import numpy as np
import UI
import wx
import functions
f = 0
f1 = 0
model_flag=0

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
    testPicArr = functions.pre_high(img)
    if(model_flag):
        preValue = functions.restore_model(testPicArr)
    else:
        preValue = functions.restore_model_lenet5(testPicArr)
    #preValue = functions.restore_model(testPicArr)
    #preValue = functions.restore_model_lenet5(testPicArr)
    #print(preValue)
    return (preValue)
    #print(preValue)
    # cv2.waitKey(0)


def application(path):
    img=cv2.imread(path)
    testPicArr = functions.pre_high(img)
    global model_flag
    if (model_flag):
        preValue = functions.restore_model(testPicArr)
    else:
        preValue = functions.restore_model_lenet5(testPicArr)
    return preValue


class window(UI.MyFrame1):#继承UI文件中MyFrame1类
    def __init__(self,p):
        UI.MyFrame1.__init__(self,p)
    def main_button_click(self,event):#识别按钮绑定的函数
        path=self.m_textCtrl1.GetValue()#获取输入框中的字符串
        ans=application(path)
        self.m_textCtrl2.SetValue(str(ans[0]))#将识别的结果送入输出框
    def model_switch(self,event):
        index = event.GetEventObject().GetSelection()
        global model_flag
        model_flag=index
    def pic_plot(self,event):
        while (True):
            try:
                img = np.zeros((512, 512, 3), np.uint8)#创建一张空画布
                ans=draw_line(img)#调用绘图程序
                self.m_textCtrl2.SetValue(str(ans[0]))  # 将识别的结果送入输出框
            except ValueError:#如果画布是空的，抛出错误并捕获，然后跳出循环
                #print('exit')

                break


def main():
    app = wx.App(False)
    frame = window(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
