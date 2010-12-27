# File 

#! /usr/local/bin/python
from Tkinter import *
#from graph import *
from math import *
import dialog

class GraphDisplay(Frame):
    
    def __init__(self,graph,master=None):
        Frame.__init__(self,master)
        
        self.grid()
        self.createWidgets()
        self.g = graph
        self.drawGraph(self.g.adjacencyDict)
       
    def createWidgets(self):

        # Canvas
        self.mycanvas = Canvas(self,bg="white")
        self.mycanvas.grid()   #(row=1,column=0,columnspan=4)        

    def drawGraph(self,g):
        self.mycanvas.delete(ALL)
        P = self.coords(len(g.keys()))    # assign vertices to points on canvas

        for p in P:
            # draw the vertices as solid circles
            self.mycanvas.create_oval(p[0]-2,p[1]-2,p[0]+2,p[1]+2,fill="black")
                
        for i in g.keys():           # draw the edges (each drawn twice!)
            for j in g[i]:
                self.mycanvas.create_line(P[i][0],P[i][1],P[j][0],P[j][1],width=0.1,smooth=1)

    def coords(self,n):   # expand and translate the roots on canvas
        x = 250 #self.mycanvas.winfo_width()
        y = 200 #self.mycanvas.winfo_height()       
        return [[x/(2.4)*(a.real)+x/2,y/(2.4)*(a.imag)+y/2] for a in [e**((2*k*pi*1j)/n) for k in range(n)]]  



