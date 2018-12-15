#coding=utf-8
import cv2
import numpy as np
import functions


def draw_circle(event,x,y,flags,param):
    global f,f1
    #cv2.CV_EVENT_FLAG_LBUTTON
    if(event==cv2.EVENT_LBUTTONDOWN):
        f=1
    elif(event==cv2.EVENT_LBUTTONUP):
        f=-1
    if (f == 1):
        cv2.circle(img,(x,y),10,(255,255,255),-1)

    if (event == cv2.EVENT_RBUTTONDOWN):
        f1 = 1
    elif (event == cv2.EVENT_RBUTTONUP):
        f1 = -1
    if (f1 == 1):
        cv2.circle(img, (x, y), 10, (0, 0, 0), -1)


f = 0
f1 = 0


def main():
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    while(True):
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            cv2.imwrite('img.png',img)
            break

    cv2.destroyAllWindows()
    #functions.pre_high(img,1)
    cv2.imshow('img',img)

    testPicArr = functions.pre_high(img,1)
    preValue = functions.restore_model(testPicArr)
    print(preValue)
    #cv2.waitKey(0)
if __name__ == '__main__':
    while(True):
        try:
            img = np.zeros((512, 512, 3), np.uint8)
            main()
        except ValueError:
            break
