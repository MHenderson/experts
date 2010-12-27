# File: dialog2.py

import tkSimpleDialog
#import string
from Tkinter import *

class MyDialog(tkSimpleDialog.Dialog):

    def body(self,master):

        Label(master,text="n:").grid(row=0,sticky=W)
  #      Label(master,text="Second:").grid(row=1,sticky=W)

        self.e1 = Entry(master)
  #      self.e2 = Entry(master)

        self.e1.grid(row=0,column=1)
  #      self.e2.grid(row=1,column=1)

   #     self.cb = Checkbutton(master, text="Hardcopy")
   #     self.cb.grid(row=2,columnspan=2,sticky=W)
        
        return None # initial focus

    def apply(self):
        
        first = int(self.e1.get())
   #     second = int(self.e2.get())
        self.result = first

class MyDialog2(tkSimpleDialog.Dialog):

    def body(self,master):

        Label(master,text="n:").grid(row=0,sticky=W)
        Label(master,text="m:").grid(row=1,sticky=W)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0,column=1)
        self.e2.grid(row=1,column=1)

    #    self.cb = Checkbutton(master, text="Hardcopy")
    #    self.cb.grid(row=2,columnspan=2,sticky=W)
        
        return None # initial focus

    def apply(self):
        
        self.first = int(self.e1.get())
        self.second = int(self.e2.get())
        


