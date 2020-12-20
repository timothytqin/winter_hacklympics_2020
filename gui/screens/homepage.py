import wx
from history import history_frame
from profile import profile_frame
from lane_detection_frame import recording_frame

class home_page(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title = title, size= (350,200))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn = wx.Button(panel, -1, "start recording")
        hbox1.Add(self.btn,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.btn.Bind(wx.EVT_BUTTON, self.on_press_record)
        sizer.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbtn = wx.Button(panel, -1, "history")
        self.hbtn.Bind(wx.EVT_BUTTON, self.on_press_history)
        self.pbtn = wx.Button(panel, -1, "profile")
        self.pbtn.Bind(wx.EVT_BUTTON, self.on_press_profile)
        hbox2.Add(self.hbtn)
        hbox2.Add(self.pbtn)
        sizer.Add(hbox2)
        panel.SetSizer(sizer)
        self.record = recording_frame("record", self)
        self.history = history_frame("history",self)
        self.profile = profile_frame("profile",self)
    def on_press_record(self, event):
        print("start recording")
        self.Hide()
        self.record.Show()
    def on_press_history(self, event):
        self.Hide()
        self.history.Show()
    def on_press_profile(self,event):
        self.Hide()
        self.profile.Show()
    # self.record.show()
    # self.record.center()
