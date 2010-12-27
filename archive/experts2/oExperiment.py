import Experts2, Numeric, MLab
from scipy import gplt

a = Experts2.VectorExpertsProblem(10,4,16,1,1,1,1)
outcomes = a.outcomeMatrix
aResult = a.mixture(0.1)
aResult2 = a.componentwiseScalarMixture(0.1)

b = a.addExpert(a.randomPseudoExpert())
bResult = b.mixture(0.1)
bResult2 = b.componentwiseScalarMixture(0.5)

noOfPseudoExperts = 15
noOfItsPer = 3

vlossVector = MLab.zeros(noOfPseudoExperts,Numeric.Float)
clossVector = MLab.zeros(noOfPseudoExperts,Numeric.Float)

for i in range(noOfPseudoExperts):
    for j in range(noOfItsPer):
        print i,j
        newExpert = a.randomPseudoExpert()
        b = b.addExpert(newExpert)
        bResult = b.mixture(0.1)
        bResult2 = b.componentwiseScalarMixture(0.1)
        vlossVector[i]+=Numeric.add.accumulate(b.lossFunction(outcomes,bResult))[b.totalTime-1]
        clossVector[i]+=Numeric.add.accumulate(b.lossFunction(outcomes,bResult2))[b.totalTime-1]

differenceVector=(vlossVector-clossVector)
gplt.plot(differenceVector)
    
