import wx
from homepage import home_page

class login_frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title = title, size = (350, 200))
        self.username = ""
        self.password = ""
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel, -1)
        hbox1.Add(l1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1 = wx.TextCtrl(panel)
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1.Bind(wx.EVT_TEXT,self.on_user_typed)
        sizer.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        l2 = wx.StaticText(panel, -1)
        hbox2.Add(l2, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t2 = wx.TextCtrl(panel)
        hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t2.Bind(wx.EVT_TEXT,self.on_password_typed)
        sizer.Add(hbox2)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn = wx.Button(panel, -1, "login")
        hbox3.Add(self.btn,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.btn.Bind(wx.EVT_BUTTON, self.on_press)
        sizer.Add(hbox3)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn2 = wx.Button(panel, -1, "create account")
        hbox4.Add(self.btn2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.btn.Bind(wx.EVT_BUTTON, self.on_press)
        sizer.Add(hbox4)
        panel.SetSizer(sizer)
        self.home = home_page("home page")

    def on_user_typed(self, event):
        self.username = event.GetString()
        print("user")
        print(self.username)
    def on_password_typed(self, event):
        self.password = event.GetString()
        print("pass")
        print(self.password)
    def on_press(self, event):
        #replace with login stuff
        print("pressed")
        print(self.username)
        print(self.password)
        self.Hide()
        self.home.Show()
        # self.home.Center()
    def create_account(self, event):
        print("create account")
app = wx.App()
frame = login_frame("login")
frame.Show()
app.MainLoop()