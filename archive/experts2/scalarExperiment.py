import Experts2, Numeric
from scipy import gplt

a = Experts2.ScalarExpertsProblem(4,5,1,1,1,0)
b = a.mixture(0.5)
c = a.outcomeMatrix
d = a.lossFunction(b,c)
e = Numeric.add.accumulate(d)
gplt.plot(e)
