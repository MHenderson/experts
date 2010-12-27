import SAT, algorithms, graph

variables = range(1,13)
clauses = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','aa','bb','cc','dd','ee']
couplingDict = {
    'a':{1:-1,2:-1,3:-1}, 'b':{4:-1,5:-1,6:-1}, 'c':{7:-1,8:-1,9:-1}, 'd':{10:-1,11:-1,12:-1},
    'e':{1:1,4:1}, 'f':{2:1,5:1}, 'g':{3:1,6:1},
    'h':{1:1,10:1}, 'i':{2:1,11:1}, 'j':{3:1,12:1},
    'k':{4:1,10:1}, 'l':{5:1,11:1}, 'm':{6:1,12:1},
    'n':{4:1,7:1}, 'o':{5:1,8:1}, 'p':{6:1,9:1},
    'q':{7:1,10:1}, 'r':{8:1,11:1}, 's':{9:1,12:1},
    't':{1:1,1:2}, 'u':{1:1,1:3}, 'v':{2:1,3:1},
    'w':{4:1,5:1}, 'x':{4:1,6:1}, 'y':{5:1,6:1},
    'z':{7:1,8:1}, 'aa':{7:1,9:1}, 'bb':{8:1,9:1},
    'cc':{10:1,11:1}, 'dd':{10:1,12:1}, 'ee':{11:1,12:1}
    }

x = SAT.SATPROB(clauses,variables,couplingDict)
y = x.factorGraph()
y.graphDraw()

#for i in range(1000):
#    print i
#    x = SAT.SATPROB(clauses,variables,couplingDict)
#    algorithms.WID(x,100)
#    print x.assignment
