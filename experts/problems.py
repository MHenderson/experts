from experts.utils import twoNorm
from experts.utils import accumulate

import math
import numpy as np

import random

class ScalarExpertsProblem():

    def __init__(self, expertsPredictionMatrix, outcomeVector, lossFunction = np.fabs):

        self.noOfExperts = expertsPredictionMatrix.shape[1]
        self.totalTime = expertsPredictionMatrix.shape[0]
        self.expertsPredictionMatrix = expertsPredictionMatrix
        self.outcomeVector = outcomeVector

        self.lossFunction = lossFunction

        self.weightVector = np.ones(self.noOfExperts)
        self.predictionVector = np.zeros(self.totalTime)

        self.expertsLossMatrix = np.zeros((self.totalTime, self.noOfExperts))
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
            expertsPredictionNowVector = self.expertsPredictionMatrix[t,:]
            predictionNow = self.predict(expertsPredictionNowVector, self.weightVector, self.predictionFunction, beta)

            # update predictions
            self.predictionVector[t] = predictionNow
            
            # update learner loss
            lossNow = self.lossFunction(predictionNow - outcomeNow)
            self.learnerLossVector[t] = lossNow

            # update experts loss
            expertsLossNow = self.lossFunction(expertsPredictionNowVector - outcomeNow)
            self.expertsLossMatrix[t, :] = expertsLossNow
            
            # update weights
            updateVector = self.updateFunction(expertsLossNow, beta)
            self.weightVector = self.weightVector * updateVector
