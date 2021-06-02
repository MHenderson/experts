from experts.utils import twoNorm
from experts.utils import accumulate

import math
import numpy as np

import random

class ScalarExpertsProblem():

    def __init__(self, noOfExperts, totalTime, expertsPredictionMatrix, outcomeVector):

        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        self.expertsPredictionMatrix = expertsPredictionMatrix
        self.outcomeVector = outcomeVector

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

    def predict(self, experts_, weights, beta):
        normalized_weights = weights/sum(weights)
        r = sum(normalized_weights * experts_)
        return(self.predictionFunction(r, beta))

    def mixture(self, beta):

        lossFunction = np.fabs
        expertsLossMatrix = np.zeros((self.totalTime, self.noOfExperts))
        learnerLossVector = np.zeros(self.totalTime)
        weightVector = np.ones(self.noOfExperts)
        predictionVector = np.zeros(self.totalTime)
        
        for t in range(self.totalTime):
            
            outcomeNow = self.outcomeVector[t]
            expertsPredictionNowVector = self.expertsPredictionMatrix[t,:]
            predictionNow = self.predict(expertsPredictionNowVector, weightVector, beta)

            # COMPUTE PREDICTION
            predictionVector[t] = predictionNow
            
            # CALCULATE LEARNER LOSS
            lossNow = lossFunction(predictionNow - outcomeNow)
            learnerLossVector[t] = lossNow

            # CALCULATE EXPERT LOSS
            expertsLossNow = lossFunction(expertsPredictionNowVector - outcomeNow)
            expertsLossMatrix[t, :] = expertsLossNow
            
            # UPDATE STEP
            updateVector = self.updateFunction(expertsLossNow, beta)
            weightVector = weightVector * updateVector

        return {"learner-loss": learnerLossVector,
                "expert-loss": expertsLossMatrix}
