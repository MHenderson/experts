import Experts2, Numeric, MLab
from scipy import gplt

a = Experts2.VectorExpertsProblem(4,5,15,1,1,1,1)
b = a.mixture(0.3)
c = a.outcomeMatrix
d = a.lossFunction(b,c)
e = Numeric.add.accumulate(d)

f = a.componentwiseScalarMixture(0.3)
g = a.lossFunction(f,c)
h = Numeric.add.accumulate(g)

plotData = MLab.zeros((15,2),Numeric.Float)

plotData[:,0] = e
plotData[:,1] = h

gplt.plot(plotData[:,0],'title "Algorithm 1" with points',plotData[:,1],'title "Componentwise scalar algorithm" with points')
gplt.legend('12.5,0.5')
gplt.grid('off')
gplt.xtitle("Time")
gplt.ytitle("Loss")
gplt.output("C:\graph2.tex",'latex')
