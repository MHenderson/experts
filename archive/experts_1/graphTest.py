import graph

vertices = range(2**3)
edges = [[x,y] for x in vertices for y in vertices if x<>y and x^y in [2**i for i in range(3)]]
adjacencies = dict(zip(vertices,[[y for y in vertices if [x,y] in edges] for x in vertices]))
x = graph.Graph(vertices, edges, adjacencies)
x.graphDraw()
