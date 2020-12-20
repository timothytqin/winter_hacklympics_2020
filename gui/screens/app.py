from login import login_panel
import wx

# class TabPanel(wx.Panel):
#     #----------------------------------------------------------------------
#     def __init__(self, parent):
#         """"""
#         wx.Panel.__init__(self, parent=parent)

#         colors = ["red", "blue", "gray", "yellow", "green"]
#         self.SetBackgroundColour(random.choice(colors))

#         btn = wx.Button(self, label="Press Me")
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(btn, 0, wx.ALL, 10)
#         self.SetSizer(sizer)
class frame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "home page", size=(600,400))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        login_page = login_panel(panel)
        sizer.Add(login_page,1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        # notebook = wx.Notebook(panel)
        # tabOne = TabPanel(notebook)
        # notebook.AddPage(tabOne, "Tab 1")

        # tabTwo = TabPanel(notebook)
        # notebook.AddPage(tabTwo, "Tab 2")

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        # panel.SetSizer(sizer)
        # self.Layout()
        self.Centre()
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    frame = frame()
    app.MainLoop()
