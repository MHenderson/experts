from perm import *
import math
import graph
import Numeric #(this is only needed for computing factorial!)

##vertices = ['v1','v2','v3','v4','v5','v6','v7','v8']
##edges = ['e1','e2','e3','e4','e5','e6','e7']
##adjacencies = {'v1':['e1'],'v2':['e2'],'v3':['e1','e2','e3','e4'],'v4':['e3'],'v5':['e5'],'v6':['e4','e5','e6','e7'],'v7':['e6'],'v8':['e7']}
##g = graph.Graph(vertices,edges,adjacencies)

vertices = ['v1','v2','v3','v4','v5','v6','v7']
edges = ['e1','e2','e3','e4','e5','e6']
adjacencies = {'v1':['e1','e2','e3','e4','e5','e6'],'v2':['e1'],'v3':['e2'],'v4':['e3'],'v5':['e4'],'v6':['e5'],'v7':['e6']}
g = graph.Graph(vertices,edges,adjacencies)

def exhaustiveGracefulSearch(graph):
    labels = range(len(g.vertexList))
    initialLabelling = dict(zip(g.vertexList,labels))
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

solns = exhaustiveGracefulSearch(g)
print(len(solns))

##for soln in solns:
##    labelling = dict(zip(vertices,soln))
##    g.labellingDict = labelling
##    g.graphDraw()


