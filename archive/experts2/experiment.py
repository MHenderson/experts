import Experts2, MLab, random, Numeric, miscellany, sets
from scipy import gplt

def pseudoExpertsExperiment():
    # loop
    #
    #     1) generate next random pseudoExpert (create new problem instance?)
    #
    #     2) run the mixture algorithm
    #
    #     3) run the componentwiseScalarMixture algorithm
    #
    #     4) compute losses
    #
    #     5) plot the loss comparison
    #
    beta = 0.9
    vectorProblem = Experts2.VectorExpertsProblem(2,5,10,1,1,1,0)
    noOfPseudoExperts = 5
    noOfExperimentsPer = 3
    averageFinalVectorLoss = MLab.zeros(noOfPseudoExperts,Numeric.Float)
    averageFinalComponentwiseLoss = MLab.zeros(noOfPseudoExperts,Numeric.Float)
    for j in range(noOfPseudoExperts):
        vectorLossMatrix = MLab.zeros((noOfExperimentsPer,vectorProblem.totalTime),Numeric.Float)
        componentwiseLossMatrix = MLab.zeros((noOfExperimentsPer,vectorProblem.totalTime),Numeric.Float)
        for k in range(noOfExperimentsPer):            
            # Compute the max # of pseudoexperts    
            maxNoOfPseudoEx = 0
            for i in range(vectorProblem.vectorLength):
                maxNoOfPseudoEx+=vectorProblem.noOfExperts**i
            maxNoOfPseudoEx*=vectorProblem.noOfExperts-1
            # Now pick the new pseudoExpert at random
            newPseudoExpert = random.randrange(maxNoOfPseudoEx)
            # Construct the prediction matrix for the new pseudoExpert
            newPseudoExpertMatrix = MLab.zeros((vectorProblem.vectorLength,vectorProblem.totalTime),Numeric.Float)
            for i in range(vectorProblem.vectorLength):
                componentExpert = miscellany.digit(newPseudoExpert,vectorProblem.noOfExperts,i)
                newPseudoExpertMatrix[i,:]=vectorProblem.expertsPredictionMatrix[i,componentExpert,:]
            # Construct the prediction matrix for the new problem instance
            newPredictionMatrix = MLab.zeros((vectorProblem.vectorLength,vectorProblem.noOfExperts+1,vectorProblem.totalTime),Numeric.Float)
            newPredictionMatrix[:,0:vectorProblem.noOfExperts,:] = vectorProblem.expertsPredictionMatrix[:,:,:]
            newPredictionMatrix[:,vectorProblem.noOfExperts,:] = newPseudoExpertMatrix[:,:]
            # Now create new problem instance with the new expert?
            vectorProblem = Experts2.VectorExpertsProblem(vectorProblem.vectorLength,vectorProblem.noOfExperts+1,vectorProblem.totalTime,newPredictionMatrix,vectorProblem.outcomeMatrix,0,0)
            # Run mixture of vector experts algorithm
            vectorPredictionMatrix = vectorProblem.mixture(beta)
            # Run componentwise scalar mixture algorithm
            componentWisePredictionMatrix = vectorProblem.componentwiseScalarMixture(beta)
            # Compute losses
            vectorLoss = vectorProblem.lossFunction(vectorPredictionMatrix,vectorProblem.outcomeMatrix)
            componentwiseLoss = vectorProblem.lossFunction(componentWisePredictionMatrix,vectorProblem.outcomeMatrix)
            # Compute cumulative losses
            cumVectorLoss = Numeric.add.accumulate(vectorLoss)
            cumComponentwiseLoss = Numeric.add.accumulate(componentwiseLoss)
            print "Vector",cumVectorLoss[vectorProblem.totalTime-1]
            print "other",cumComponentwiseLoss[vectorProblem.totalTime-1]
            # Put cumulative losses in matrix
            vectorLossMatrix[k,:] = cumVectorLoss
            componentwiseLossMatrix[k,:] = cumComponentwiseLoss
        # Compute average losses
        averageVectorLoss = sum(vectorLossMatrix)/noOfExperimentsPer
        averageComponentwiseLoss = sum(componentwiseLossMatrix)/noOfExperimentsPer
        # Put average FINAL loss in vector
        averageFinalVectorLoss[j] = averageVectorLoss[vectorProblem.totalTime-1]
        averageFinalComponentwiseLoss[j] = averageComponentwiseLoss[vectorProblem.totalTime-1]
    # Plot difference of averages
    x = range(noOfPseudoExperts)
    gplt.plot(x,averageFinalComponentwiseLoss-averageFinalVectorLoss)
##        gplt.output("C:/test.png",'png color')

##def lossFunction(matrix1,matrix2):
##    if matrix1.shape!=matrix2.shape:
##        return None
##    else:
##        x = matrix1.shape[0]
##        y = matrix2.shape[1]
##    return Numeric.sqrt(sum((matrix1-matrix2)**2)/x)

##    # Here we use the setOfExperts to store the current set of
##    # vector experts (as base noOfExperts integers)
##    setOfExperts = sets.Set()
##    for i in range(vectorProblem.noOfExperts):
##        genuineExpert = 0
##        for j in range(vectorProblem.vectorLength):
##            genuineExpert+=i*vectorProblem.noOfExperts**j
##        setOfExperts.add(genuineExpert)
##
##    # Add the pseudoExpert to the set of pseudoExperts
##    setOfExperts.add(newPseudoExpert)
