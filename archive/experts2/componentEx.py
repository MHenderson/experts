import Experts2, Numeric, MLab, time
from scipy import gplt
from scipy import stats

vectorLength = 4
noOfExperts = 5
totalTime = 15
noOfPseudoExperts = 1495
beta = 0.9

noOfItsPer = 10

lossMatrix = MLab.zeros((noOfPseudoExperts+noOfExperts+1,noOfItsPer),Numeric.Float)

starttime = time.clock()

for j in range(noOfItsPer):
    a = Experts2.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1)
    b = a
    outcome = b.outcomeMatrix
    print "Iteration: ", j+1
    for i in range(noOfPseudoExperts+noOfExperts+1):
        # print "# PseudoExperts: ",i
        vectorPrediction = b.mixture(beta)
        componentwisePrediction = b.componentwiseScalarMixture(beta)
        componentwiseFinalLoss = Numeric.add.accumulate(b.lossFunction(outcome,componentwisePrediction))[b.totalTime-1]
        vectorFinalLoss = Numeric.add.accumulate(b.lossFunction(outcome,vectorPrediction))[b.totalTime-1]
        lossMatrix[i,j] = componentwiseFinalLoss-vectorFinalLoss
        newExpert = a.randomPseudoExpert()
        b = b.addExpert(newExpert)

stoptime = time.clock()

print stoptime-starttime

lossVector = stats.mean(lossMatrix)

#print lossMatrix
#print stats.mean(lossMatrix)

std = stats.std(lossMatrix)

#print std

plottingData = MLab.zeros((noOfPseudoExperts+noOfExperts+1,3),Numeric.Float)

plottingData[:,0] = lossVector
plottingData[:,1] = lossVector+std
plottingData[:,2] = lossVector-std

gplt.plot(plottingData[:,0],'title "\\parbox{3in}{Mean difference between total loss \\ of Algorithm 1 and the componentwise \\ scalar algorithm}" with points pointtype 2',plottingData[:,1],'title "Standard deviation" with dots',plottingData[:,2],'notitle with dots')
gplt.grid('off')
gplt.xtitle("No. of pseudo experts")
gplt.ytitle("Advantage")
gplt.output("C:\graph.tex",'latex')


