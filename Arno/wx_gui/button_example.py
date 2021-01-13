import wx

########################################################################
class MyPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.btns = 1

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        add_btn = wx.Button(self, label='Add')
        add_btn.Bind(wx.EVT_BUTTON, self.add_button)

        self.main_sizer.Add(add_btn, 0, wx.CENTER|wx.ALL, 5)
        self.SetSizer(self.main_sizer)

    #----------------------------------------------------------------------
    def add_button(self, event):
        """"""
        new_btn = wx.Button(self, label="Remove %s" % self.btns)
        new_btn.Bind(wx.EVT_BUTTON, self.remove_button)
        self.btns += 1
        self.main_sizer.Add(new_btn, 0, wx.CENTER|wx.ALL, 5)
        self.main_sizer.Layout()

    #----------------------------------------------------------------------
    def remove_button(self, event):
        """"""
        btn = event.GetEventObject()
        print ("Deleting %s button") # % btn.GetLabel()
        self.main_sizer.Hide(btn)
        self.main_sizer.Remove(btn)
        self.main_sizer.Layout()


########################################################################
class MyFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Buttons")
        panel = MyPanel(self)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()