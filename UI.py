# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"手写数字识别", pos=wx.DefaultPosition, size=wx.Size(500, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

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
        self.mainmenu = wx.MenuBar(0)
        self.menu = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.menu, wx.ID_ANY, u"绘制图片", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu.AppendItem(self.m_menuItem1)

        self.mainmenu.Append(self.menu, u"绘图")

        self.SetMenuBar(self.mainmenu)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.main_button_click)
        self.Bind(wx.EVT_MENU, self.pic_plot, id=self.m_menuItem1.GetId())

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def main_button_click(self, event):
        event.Skip()

    def pic_plot(self, event):
        event.Skip()


