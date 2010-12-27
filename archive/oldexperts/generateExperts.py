import Experts, Numeric, MLab, Gnuplot, random
from miscFunctions import *

##vectorLength = 15
##noOfExperts = 20
##totalTime = 15
##noOfExperiments = 20
##noOfItsPerDP = 35
vectorLength = 20
noOfExperts = 20
totalTime = 15
noOfExperiments = 3
noOfItsPerDP = 3
dataPoints = range(0,201,10)
differenceVector = Numeric.zeros(len(dataPoints),Numeric.Float)
##maximumNoOfPseudoExperts = noOfExperts**totalTime
maximumNoOfPseudoExperts =  noOfExperts**vectorLength
##percentageOfPseudoExperts = 0.015
##noOfPseudoExperts = int(percentageOfPseudoExperts*maximumNoOfPseudoExperts)
##print noOfPseudoExperts

for m in range(len(dataPoints)):
    print "dataPoint:",dataPoints[m]
    for n in range(noOfItsPerDP):
        print "Iteration:",n
       
        noOfPseudoExperts = dataPoints[m]
        totalNoOfExperts = noOfExperts+noOfPseudoExperts

        vectorResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)
        scalarResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)

        #
        # Add pseudoexperts
        #

        for i in range(noOfExperiments):

            A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1)
            #print A.expertsPredictionMatrix

            oldPredictionMatrix = A.expertsPredictionMatrix
            newPredictionMatrix = Numeric.zeros([totalTime,vectorLength,totalNoOfExperts],Numeric.Float)

            newPredictionMatrix[:,:,0:noOfExperts] = oldPredictionMatrix

            pseudoExpertsUsed = []

            for j in range(noOfExperts,totalNoOfExperts):

                #print "Expert ",j,"added."

                if len(pseudoExpertsUsed)==maximumNoOfPseudoExperts:
                    print "Pseudo experts exhausted..."                

                newExpert = MLab.zeros([totalTime,vectorLength],Numeric.Float)

                chosen = 0
                while chosen==0:
                    pseudoExpert = Numeric.floor(random.uniform(noOfExperts+1,maximumNoOfPseudoExperts))
                    if pseudoExpert not in pseudoExpertsUsed:
                        pseudoExpertsUsed.append(pseudoExpert)
                        chosen = 1

##                pseudoExpert = Numeric.floor(random.uniform(noOfExperts+1,maximumNoOfPseudoExperts))

##                for t in range(totalTime):
##                    newExpert[t,:] = oldPredictionMatrix[t,:,digit(pseudoExpert,noOfExperts,t)]

                for component in range(vectorLength):
                    newExpert[:,component] = oldPredictionMatrix[:,component,digit(pseudoExpert,noOfExperts,component)]

                newPredictionMatrix[:,:,j] = newExpert[:,:]

            B = Experts.VectorExpertsProblem(vectorLength,totalNoOfExperts,totalTime,newPredictionMatrix,A.outcomeMatrix,0,0)

            #print B.expertsPredictionMatrix
            
            result = B.scalarMixture(0.1)
            B.makeHTMLReport()
            scalarResult = result[0]
            vectorResult = result[1]
            vectorResultMatrix[i,:] = vectorResult
            scalarResultMatrix[i,:] = scalarResult

        x = range(totalTime)

        vectorAverage = sum(vectorResultMatrix)/noOfExperiments
        scalarAverage = sum(scalarResultMatrix)/noOfExperiments

        vectorFinalLoss = vectorAverage[totalTime-1]
        scalarFinalLoss = scalarAverage[totalTime-1]
        difference = vectorFinalLoss - scalarFinalLoss
        differenceVector[m] = differenceVector[m]+difference


differenceVector = differenceVector/noOfItsPerDP

#
# indent/dedent for plot at each stage/at end only.#
#
##if m>0:
##    x = dataPoints[:m+1]
##    y = differenceVector[:m+1]
##    plotData = Gnuplot.Data(x,y,with='points')
##    g = Gnuplot.Gnuplot(persist=1)
##    g.xlabel('No. of pseudo experts.');
##    g.ylabel('Advantage of scalar algorithm.');
##    g.plot(plotData)
##    g.hardcopy(filename='reportFiles/result.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=20)


plotData = Gnuplot.Data(dataPoints,differenceVector,with='points')
g = Gnuplot.Gnuplot(persist=1)
g.xlabel('No. of pseudo experts.');
g.ylabel('Advantage of scalar algorithm.');
g.plot(plotData)
g.hardcopy(filename='reportFiles/result.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=20)

##vectorData = Gnuplot.Data(x,vectorAverage,with='lines',title='vec')
##scalarData = Gnuplot.Data(x,scalarAverage,with='lines',title='sca')
##g = Gnuplot.Gnuplot(persist=1)
##g.title('Mixture of Vector Experts Experiment')
###g('set term png small color')
###g('set output "tmp2.png"')
##g.plot(vectorData,scalarData)
##g.hardcopy(filename='tmp3.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=20)


