import wx

class history_frame(wx.Frame):
    def __init__(self, title, prev_frame):
        wx.Frame.__init__(self, None, title = title, size= (350,200))
        self.prev = prev_frame
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn = wx.Button(panel, -1, "back")
        hbox1.Add(self.btn,1,wx.ALIGN_CENTER|wx.ALL,5)
        self.btn.Bind(wx.EVT_BUTTON, self.on_press)
        sizer.Add(hbox1)

        panel.SetSizer(sizer)
    def on_press(self, event):
        self.Hide()
        self.prev.Show()
