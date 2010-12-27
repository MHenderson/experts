import graph, graceful

##vertices = ['v1','v2','v3','v4','v5','v6','v7','v8']
##edges = ['e1','e2','e3','e4','e5','e6','e7']
##adjacencies = {'v1':['e1'],'v2':['e2'],'v3':['e1','e2','e3','e4'],'v4':['e3'],'v5':['e5'],'v6':['e4','e5','e6','e7'],'v7':['e6'],'v8':['e7']}
##g = graph.Graph(vertices,edges,adjacencies)

##vertices = ['v1','v2','v3','v4','v5','v6','v7']
##edges = ['e1','e2','e3','e4','e5','e6']
##adjacencies = {'v1':['e1','e2','e3','e4','e5','e6'],'v2':['e1'],'v3':['e2'],'v4':['e3'],'v5':['e4'],'v6':['e5'],'v7':['e6']}
##g = graph.Graph(vertices,edges,adjacencies)

vertices = ['v1','v2','v3','v4','v5','v6','v7','v8']
edges = ['e1','e2','e3','e4','e5','e6','e7']
adjacencies = {'v1':['e1'],'v2':['e2'],'v3':['e2','e3'],'v4':['e1','e3','e4','e5'],'v5':['e4'],'v6':['e6'],'v7':['e5','e6','e7'],'v8':['e7']}
g = graph.Graph(vertices,edges,adjacencies)


solns = graceful.exhaustiveGracefulSearch(g)

verticesNeverLabelledZero = range(len(g.vertexList))
for soln in solns:
    d = soln.index(0)
    if d in verticesNeverLabelledZero:
        verticesNeverLabelledZero.remove(d)

def difference(A,B):
    result=0
    for i in range(len(A)):
        if A[i]!=B[i]:
            result+=1
    return result

vertices = range(len(solns))
connections = []
for i in vertices:
    for j in range(i+1,len(solns)):
        if difference(solns[i],solns[j])==2:
            connections.append([i,j])
edges = range(len(connections))
adjacencies={}
for i in vertices:
    adjacencies[i]=[]
for edge in edges:
    end0 = connections[edge][0]
    end1 = connections[edge][1]
    adjacencies[end0].append(edge)
    adjacencies[end1].append(edge)

g = graph.Graph(vertices,edges,adjacencies)
g.graphDraw()  

##for soln in solns:
##    labelling = dict(zip(vertices,soln))
##    g.labellingDict = labelling
##    g.graphDraw()
