import math
import numpy as np

from experts.utils import twoNorm

class ScalarExpertsProblem():

    def __init__(self, expertsPredictionMatrix, outcomeVector, lossFunction = np.fabs):

        self.noOfExperts = expertsPredictionMatrix.shape[0]
        self.totalTime = expertsPredictionMatrix.shape[1]
        self.expertsPredictionMatrix = expertsPredictionMatrix
        self.outcomeVector = outcomeVector

        self.lossFunction = lossFunction

        self.weightVector = np.ones(self.noOfExperts)
        self.predictionVector = np.zeros(self.totalTime)

        self.expertsLossMatrix = np.zeros((self.noOfExperts, self.totalTime))
        self.learnerLossVector = np.zeros(self.totalTime)

    def predictionFunction(self, value, beta):
        c = ((1 + beta) * math.log(2 / (1 + beta))) / (2 * (1 - beta))
        if value <= 0.5 - c:
            return 0
        elif value < 0.5 + c and value > 0.5 - c:
            return 0.5 - ((1 - 2 * value) / (4 * c))
        else:
            return 1

    def updateFunction(self,value,beta):
        return 1 - (1 - beta) * value

    def predict(self, experts_, weights, predictionFunction, beta):
        normalized_weights = weights/sum(weights)
        r = sum(normalized_weights * experts_)
        return(predictionFunction(r, beta))

    def mixture(self, beta):

        for t in range(self.totalTime):
            
            outcomeNow = self.outcomeVector[t]
            expertsPredictionNowVector = self.expertsPredictionMatrix[:, t]
            predictionNow = self.predict(expertsPredictionNowVector, self.weightVector, self.predictionFunction, beta)

            # update predictions
            self.predictionVector[t] = predictionNow
            
            # update learner loss
            lossNow = self.lossFunction(predictionNow - outcomeNow)
            self.learnerLossVector[t] = lossNow

            # update experts loss
            expertsLossNow = self.lossFunction(expertsPredictionNowVector - outcomeNow)
            self.expertsLossMatrix[:, t] = expertsLossNow
            
            # update weights
            updateVector = self.updateFunction(expertsLossNow, beta)
            self.weightVector = self.weightVector * updateVector

class VectorExpertsProblem():

    def __init__(self, expertsPredictionMatrix, outcomeMatrix):

        self.expertsPredictionMatrix = expertsPredictionMatrix
        self.outcomeMatrix = outcomeMatrix

        self.noOfExperts = expertsPredictionMatrix.shape[0]
        self.totalTime = expertsPredictionMatrix.shape[1]
        self.vectorLength = expertsPredictionMatrix.shape[2]

        self.learnerLossVector = np.zeros(self.totalTime)
        self.predictionMatrix = np.zeros([self.totalTime, self.vectorLength])

        self.expertsLosses = np.zeros(self.noOfExperts)
        self.expertsLossMatrix = np.zeros([self.totalTime, self.noOfExperts])

        self.weightVector = np.ones(self.noOfExperts)

    def predictionFunction(self, value, beta):
        c = ((1 + beta) * math.log(2 / (1 + beta))) / (2 * (1 - beta));
        zeroIndices = np.less(value, 0.5 - c)
        oneIndices = np.greater(value, 0.5 + c)
        r = 0.5 - ((1 - 2 * value) / (4 * c))
        r = np.where(zeroIndices, 0.0, r)
        r = np.where(oneIndices, 1.0, r)
        return r

    def updateFunction(self, value, beta):
        return 1 - (1 - beta) * value

    def predict(self, weights, experts_, beta):
        normalizedWeightVector = weights/sum(weights)
        normalizedWeightVectorMatrix = np.repeat(normalizedWeightVector, self.vectorLength)
        normalizedWeightVectorMatrix.shape = (self.noOfExperts, self.vectorLength)
        productNow = normalizedWeightVectorMatrix * experts_
        vecrNow = sum(productNow)
        return(self.predictionFunction(vecrNow, beta))

    def mixture(self, beta, lossFunction = twoNorm):

        for t in range(self.totalTime):

            # update prediction
            expertsPredictionMatrixNow = self.expertsPredictionMatrix[:, t, :]
            predictionNow = self.predict(self.weightVector, expertsPredictionMatrixNow, beta)
            self.predictionMatrix[t, :] = predictionNow

            # update learner loss
            outcomeNow = self.outcomeMatrix[t, :]
            learnerLossNow = lossFunction(np.absolute(predictionNow - outcomeNow))
            self.learnerLossVector[t] = learnerLossNow

            # update expert losses
            outcomeNowMatrix = np.repeat(outcomeNow, self.noOfExperts)
            outcomeNowMatrix.shape = (self.noOfExperts, self.vectorLength)
            expertLossMatrixNow = expertsPredictionMatrixNow - outcomeNowMatrix
            expertLossNowVector = np.zeros(self.noOfExperts)
            for i in range(self.noOfExperts):
                expertLossNowVector[i] = lossFunction(np.absolute(expertLossMatrixNow[:, i]))
                self.expertsLossMatrix[t, i] = expertLossNowVector[i]

            # update weights
            self.weightVector = self.weightVector * self.updateFunction(expertLossNowVector, beta)
