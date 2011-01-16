import Experts, Numeric, MLab, random
from miscFunctions import *
#from scipy import gplt

vectorLength = 7
noOfExperts = 4      
totalTime = 10
noOfExperiments = 4
noOfItsPerDP = 4
#
# For the time being, the upper limit of the following range 
# should be <= noOfExperts**vectorLength(+1?)
#
dataPoints = range(0,51,1)
differenceVector = Numeric.zeros(len(dataPoints),Numeric.Float)
maximumNoOfPseudoExperts =  noOfExperts**vectorLength


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

            A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,0)

            oldPredictionMatrix = A.expertsPredictionMatrix
            newPredictionMatrix = Numeric.zeros([totalTime,vectorLength,totalNoOfExperts],Numeric.Float)

            newPredictionMatrix[:,:,0:noOfExperts] = oldPredictionMatrix

            pseudoExpertsUsed = []

            for j in range(noOfExperts,totalNoOfExperts):              

                newExpert = MLab.zeros([totalTime,vectorLength],Numeric.Float)
                X = [noOfExperts**k for k in range(vectorLength)]
                X = sum(X)
                X *= noOfExperts-1

                chosen = 0
                while chosen==0:
                    pseudoExpert = random.choice(range(X+1))
                    if pseudoExpert not in pseudoExpertsUsed:
                        pseudoExpertsUsed.append(pseudoExpert)
                        chosen = 1

                for t in range(totalTime):
                    newExpert[t,:] = oldPredictionMatrix[t,:,digit(pseudoExpert,noOfExperts,t)]

                for component in range(vectorLength):
                    newExpert[:,component] = oldPredictionMatrix[:,component,digit(pseudoExpert,noOfExperts,component)]

                newPredictionMatrix[:,:,j] = newExpert[:,:]

            B = Experts.VectorExpertsProblem(vectorLength,totalNoOfExperts,totalTime,newPredictionMatrix,A.outcomeMatrix,0,0)
           
            result = B.scalarMixture(0.1)
            B.makeHTMLReport("report.html")
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

gplt.plot(differenceVector)


