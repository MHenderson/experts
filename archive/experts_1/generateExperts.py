import Experts, Numeric, MLab, Gnuplot, random, psyco
from digit import *


psyco.full()


##vectorLength = 15
##noOfExperts = 20
##totalTime = 15
##noOfExperiments = 20
##noOfItsPerDP = 35
vectorLength = 6
noOfExperts = 5
totalTime = 7
noOfExperiments = 3
noOfItsPerDP = 3
dataPoints = range(0,78100,1000)
differenceVector = Numeric.zeros(len(dataPoints),Numeric.Float)
maximumNoOfPseudoExperts = noOfExperts**totalTime
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

            # a = range(maximumNoOfPseudoExperts)

            pseudoExpertsUsed = []
            #print pseudoExpertsUsed

            for j in range(noOfExperts,totalNoOfExperts):
                #print "Expert ",j,"added."

                if len(pseudoExpertsUsed)==maximumNoOfPseudoExperts:
                    print "Pseudo experts exhausted..."                

                newExpert = MLab.zeros([totalTime,vectorLength],Numeric.Float)

                # choose new random pseudo expert
##                chosen = 0
##                while chosen==0:
##                    pseudoExpert = Numeric.floor(random.uniform(noOfExperts+1,maximumNoOfPseudoExperts))
##                    if pseudoExpert not in pseudoExpertsUsed:
##                        pseudoExpertsUsed.append(pseudoExpert)
##                        chosen = 1
##              
##                for k in range(vectorLength):
##                    newExpert[:,k] = oldPredictionMatrix[:,k,digit(pseudoExpert,noOfExperts,k)]

                chosen = 0
                while chosen==0:
                    pseudoExpert = Numeric.floor(random.uniform(noOfExperts+1,maximumNoOfPseudoExperts))
                    if pseudoExpert not in pseudoExpertsUsed:
                        pseudoExpertsUsed.append(pseudoExpert)
                        chosen = 1

                #print pseudoExpertsUsed

                for t in range(totalTime):
                    newExpert[t,:] = oldPredictionMatrix[t,:,digit(pseudoExpert,noOfExperts,t)]

                newPredictionMatrix[:,:,j] = newExpert[:,:]

            B = Experts.VectorExpertsProblem(vectorLength,totalNoOfExperts,totalTime,newPredictionMatrix,A.outcomeMatrix,0,0)

            #print B.expertsPredictionMatrix
            
            result = B.scalarMixture(0.1)
            #B.makeHTMLReport()
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

    if m>0:
        x = dataPoints[:m+1]
        y = differenceVector[:m+1]
        plotData = Gnuplot.Data(x,y,with='points')
        g = Gnuplot.Gnuplot(persist=1)
        g.xlabel('No. of pseudo experts.');
        g.ylabel('Advantage of scalar algorithm.');
        g.plot(plotData)
        g.hardcopy(filename='result.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=20)


##vectorData = Gnuplot.Data(x,vectorAverage,with='lines',title='vec')
##scalarData = Gnuplot.Data(x,scalarAverage,with='lines',title='sca')
##g = Gnuplot.Gnuplot(persist=1)
##g.title('Mixture of Vector Experts Experiment')
###g('set term png small color')
###g('set output "tmp2.png"')
##g.plot(vectorData,scalarData)
##g.hardcopy(filename='tmp3.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=20)


