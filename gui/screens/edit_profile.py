import wx
import os
from tkinter import *
from tkinter import filedialog
class edit_frame(wx.Frame):
    def __init__(self, title, prev_frame):
        wx.Frame.__init__(self, None, title = title, size= (350,200))
        self.prev = prev_frame
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.img_btn = wx.Button(panel, -1, "edit image")
        hbox.Add(self.img_btn, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        self.img_btn.Bind(wx.EVT_BUTTON, self.load_image)
        sizer.Add(hbox)
        panel.SetSizer(sizer)
    def load_image(self, event):
        window = Tk()
        window.title('File Explorer')
        window.geometry("500x500")
        label_file_explorer = Label(window)
        button_explore = Button(window, text = "Browse Files", command = self.browseFiles)
        button_exit = Button(window, text = "Exit", command = exit)
        label_file_explorer.grid(column = 1, row = 1)
        button_explore.grid(column = 1, row = 2)
        button_exit.grid(column = 1,row = 3)
        window.mainloop()
        print(self.filename)
    def back_button(self, event):
        self.Hide()
        self.prev.Show()
    def browseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select an image", filetypes = (("Image files", ["*.jpg*", "*.png*"]), ("all files", "*.*")))
