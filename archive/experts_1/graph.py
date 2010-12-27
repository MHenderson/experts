# File : graph.py

from math import *
import gui, Tkinter, dialog

class Graph:

    vertexList = []
    edgeList = []
    adjacencyDict = {}

    def __init__(self,vertices,edges,adjacencies,labelling={}):
        self.vertexList = vertices
        self.edgeList = edges
        self.adjacencyDict = adjacencies
        if labelling=={}:
            self.labellingDict = dict(zip(self.vertexList,self.vertexList))
        else:
            self.labellingDict = labelling

    def graphDraw(self,showLabels=0,drawVertices=1):
        root = Tkinter.Tk()
        app = GraphWindow(self,showLabels,drawVertices,400,400,root)
        app.master.title("pyGraph")
        app.pack(expand=True,fill='both')
        app.mainloop()

    def ends(self,edge):
        result = []
        for i in self.adjacencyDict.keys():
            if edge in self.adjacencyDict[i]:
                result.append(i)
        return result

class GraphWindow(Tkinter.Frame):
    
    def __init__(self,graph,showLabels,drawVertices,x,y,master=None):             
        
        Tkinter.Frame.__init__(self,master)        
        self.g = graph
        self.c = Tkinter.Canvas(self,height=y,width=x,bg="white")
        self.c.delete(Tkinter.ALL)
        coords = self.coords(x,y,len(self.g.vertexList))
        labelCoords = self.labelCoords(x,y,len(self.g.vertexList))
        vertexCoordsDict = dict(zip(self.g.vertexList,coords))
        vertexLabelCoordsDict = dict(zip(self.g.vertexList,labelCoords))
        
        # assign vertices to points on canvas and possibly draw labels

        for vertex in self.g.vertexList:
            # draw the vertices as solid circles
            if drawVertices==1:
                self.c.create_oval(vertexCoordsDict[vertex][0]-2,vertexCoordsDict[vertex][1]-2,vertexCoordsDict[vertex][0]+2,vertexCoordsDict[vertex][1]+2,fill="black")
            if showLabels==1:
                self.c.create_text(vertexLabelCoordsDict[vertex][0],vertexLabelCoordsDict[vertex][1],text=self.g.labellingDict[vertex])           
                           
        for edge in self.g.edgeList:
            end0 = self.g.ends(edge)[0]
            end1 = self.g.ends(edge)[1]
            self.c.create_line(vertexCoordsDict[end0][0],vertexCoordsDict[end0][1],vertexCoordsDict[end1][0],vertexCoordsDict[end1][1])

        self.c.pack(expand=True,fill='both')

        
    def coords(self,width,height,n):   # expand and translate the roots on canvas             
        return [[width/(2.4)*(a.real)+width/2,height/(2.4)*(a.imag)+height/2] for a in [e**((2*k*pi*1j)/n) for k in range(n)]]

    def labelCoords(self,width,height,n):     
        return [[width/(2.1)*(a.real)+width/2,height/(2.1)*(a.imag)+height/2] for a in [e**((2*k*pi*1j)/n) for k in range(n)]]
