from perm import *
import math
#import graph
import Numeric #(this is only needed for computing factorial!)

def exhaustiveGracefulSearch(graph):
    labels = range(len(graph.vertexList))
    initialLabelling = dict(zip(graph.vertexList,labels))
    graph.labellingDict = initialLabelling
    #g.graphDraw()

    A = labels[:]
    P = []
    # the following could be replaced by factorial(len(g.vertexList+1)) if I
    # write a factorial function
    q = Numeric.product(range(1,len(graph.vertexList)+1))
    for i in range(q):
        P.append(A)
        A = perm(A)

    solns = []
    for p in P:
        # D is the list of differences D=[1,2,3,..,#E]
        D = range(1,len(graph.edgeList)+1)
        for edge in graph.edgeList:
            end0 = graph.ends(edge)[0]
            end1 = graph.ends(edge)[1]
            difference = int(math.fabs(p[initialLabelling[end0]]-p[initialLabelling[end1]]))
            if difference in D:
                D.remove(difference)
        if D == []:
            solns.append(p)
    return solns





