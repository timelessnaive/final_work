# -*- coding: utf-8 -*-
import wx
import wx.xrc
import numpy
import wx.lib.plot as wxPyPlot
# 导入绘图模块,并命名为wxPyPlot

###########################################################################
## Class MyFrame1
###########################################################################
def MyDataObject():
    # 50 个点的sin函数,用蓝色圆点表示
    data1 = 2. * numpy.pi * numpy.arange(100) / 100.
    data1.shape = (50, 2)
    data1[:, 1] = numpy.sin(data1[:, 0])
    markers = wxPyPlot.PolyMarker(data1, legend='Green Markers', colour='blue', marker='circle', size=1)

    # 50个点的cos函数,用红色表示
    data2 = 2. * numpy.pi * numpy.arange(100) / 100.
    data2.shape = (50, 2)
    data2[:, 1] = numpy.cos(data2[:, 0])
    lines = wxPyPlot.PolySpline(data2, legend='Red Line', colour='red')

    GraphTitle = "Plot Data(Sin and Cos)"

    return wxPyPlot.PlotGraphics([markers, lines], GraphTitle, "X Axis", "Y Axis")

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"手写数字识别", pos=wx.DefaultPosition, size=wx.Size(500, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        '''
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"输入图片文件路径", wx.DefaultPosition, wx.Size(1000, 30), 0)
        self.m_staticText1.Wrap(-1)
        self.m_staticText1.SetFont(wx.Font(20, 70, 90, 90, False, wx.EmptyString))

        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"识别", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        '''
        self.mainmenu = wx.MenuBar(0)
        self.menu = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.menu, wx.ID_ANY, u"绘制图片", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu.Append(self.m_menuItem1)

        self.mainmenu.Append(self.menu, u"绘图")

        self.SetMenuBar(self.mainmenu)
        self.Bind(wx.EVT_MENU, self.pic_plot, id=self.m_menuItem1.GetId())
        self.Centre(wx.BOTH)
        self.pc = wxPyPlot.PlotCanvas(self)
        # Connect Events
        #self.m_button1.Bind(wx.EVT_BUTTON, self.main_button_click)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def main_button_click(self, event):
        #path = self.m_textCtrl1.GetValue()
        #self.m_textCtrl2.SetValue(path)
        #self.pc.Draw(MyDataObject())
        pass

    def pic_plot(self, event):
        self.pc.Draw(MyDataObject())
if __name__ == '__main__':
    app = wx.App()
    tf = MyFrame1(None)
    tf.Show()
    app.MainLoop()
