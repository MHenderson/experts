import SAT, algorithms, graph

#
# This is a prototype for the definition of the factor
# graph of a SAT instance
#

x = SAT.random3SAT(12,5)
y = x.variableList[:]
z = x.clauseList[:]
vertices = y+z
edges = [[clause,variable] for clause in x.clauseList for variable in x.variablesInvolved(clause) if x.couplingDict[clause][variable] in [-1,1]]
adjacencies = dict(zip(vertices,[[y for y in vertices if [x,y] in edges] for x in vertices]))
x = graph.Graph(vertices, edges, adjacencies)
x.graphDraw()

