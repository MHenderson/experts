from experts.utils import twoNorm
from experts.utils import accumulate

import math
import numpy as np

import random

class ExpertsProblem:

    def predictionFunction(self,value,beta):
        c = ((1+beta)*math.log(2/(1+beta)))/(2*(1-beta));
        if np.size(value)==1:
            if value<=0.5-c:
                return 0
            elif value<0.5+c and value>0.5-c:
                return 0.5-((1-2*value)/(4*c))
            else:
                return 1
        else:
            zeroIndices = np.less(value,0.5-c)
            oneIndices = np.greater(value,0.5+c)
            r = 0.5-((1-2*value)/(4*c))
            r = np.where(zeroIndices,0.0,r)
            r = np.where(oneIndices,1.0,r)
            return r

    def updateFunction(self,value,beta):
        return 1-(1-beta)*value
                           
class VectorExpertsProblem(ExpertsProblem):
    
    def __init__(self,vectorLength,noOfExperts,totalTime,expertsPredictionMatrix=[],outcomeMatrix=[],outcomeAsExpert=0,addNoise=0,verbosity=0):
        self.vectorLength = vectorLength
        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        self.componentwiseCLV = ["Didn\'t run componentwise scalar mixture"]
        self.scalarPredictionMatrix = ["Didn\'t run componentwise scalar mixture"]
        if type(expertsPredictionMatrix)==int:
            if verbosity>=1: print("Randomizing Vector Experts...")
            self.expertsPredictionMatrix = np.random.rand(self.totalTime,self.vectorLength,self.noOfExperts)
        else:
            self.expertsPredictionMatrix = expertsPredictionMatrix
        if type(outcomeMatrix)==int:
            if verbosity>=1: print("Randomizing Vector Outcomes...")
            self.outcomeMatrix = np.floor(2*np.random.rand(self.vectorLength,self.totalTime))
        else:
            self.outcomeMatrix = outcomeMatrix
        if outcomeAsExpert==1:
            if verbosity>=1: print("Introducing outcome as expert...")
            for t in range(self.totalTime):
                self.expertsPredictionMatrix[t,:,self.noOfExperts-1]=self.outcomeMatrix[:,t]
        if addNoise==1:
            if verbosity>=1: print("Adding noise to outcome-expert...")
            self.addNoise(self.noOfExperts-1,self.totalTime)

    def addNoise(self,expert,totalTime):
        
        for i in range(totalTime):
            for j in range(self.vectorLength):
                a = random.gauss(0,0.1)
                if 0<=a+self.expertsPredictionMatrix[i,j,expert]<=1:
                    self.expertsPredictionMatrix[i,j,expert] = a+self.expertsPredictionMatrix[i,j,expert] 
    
    def mixture(self,beta):

        lossFunction = twoNorm
        expertsLosses = np.zeros(self.noOfExperts)
        expertsCumulativeLossMatrix = np.zeros([self.totalTime,self.noOfExperts])
        totalLearnerLoss = 0
        self.learnerCumulativeLossVector = np.zeros(self.totalTime)
        weightVector = np.ones(self.noOfExperts)
        self.predictionMatrix = np.zeros([self.totalTime,self.vectorLength])

        for t in range(self.totalTime):

            # COMPUTE PREDICTION
            expertsPredictionMatrixNow = self.expertsPredictionMatrix[t,:,:]
            outcomeNow = self.outcomeMatrix[:,t]
            normalizedWeightVector = weightVector/sum(weightVector)
            normalizedWeightVectorMatrix = np.repeat(normalizedWeightVector,self.vectorLength)
            normalizedWeightVectorMatrix.shape = (self.noOfExperts,self.vectorLength)
            normalizedWeightVectorMatrix = np.transpose(normalizedWeightVectorMatrix)
            productNow = expertsPredictionMatrixNow*normalizedWeightVectorMatrix
            productNow = np.transpose(productNow)
            vecrNow = sum(productNow)
            predictionNow = self.predictionFunction(vecrNow,beta)
            self.predictionMatrix[t,:] = predictionNow
            
            # CALCULATE LEARNER LOSS
            learnerLossNow = lossFunction(np.absolute(predictionNow-outcomeNow))
            totalLearnerLoss = totalLearnerLoss + learnerLossNow
            self.learnerCumulativeLossVector[t] = totalLearnerLoss
            
            # CALCULATE EXPERT LOSSES
            outcomeNowMatrix = np.repeat(outcomeNow,self.noOfExperts)
            outcomeNowMatrix.shape = (self.vectorLength,self.noOfExperts)
            expertLossMatrixNow = expertsPredictionMatrixNow - outcomeNowMatrix
            expertLossNowVector = np.zeros(self.noOfExperts)
            for i in range(self.noOfExperts):
                expertLossNowVector[i] = lossFunction(np.absolute(expertLossMatrixNow[:,i]))
                expertsCumulativeLossMatrix[t,i] = expertsCumulativeLossMatrix[t-1,i]+expertLossNowVector[i]
            
            # UPDATE WEIGHTS
            weightVector = weightVector*self.updateFunction(expertLossNowVector,beta)
        
        # CALCULATE THEORETICAL UPPER BOUND
        expertsLosses = expertsCumulativeLossMatrix[self.totalTime-1,:]
        bestExpertLoss = np.min(expertsLosses);
        self.upperbound = (np.log(self.noOfExperts)-bestExpertLoss*np.log(beta))/(2*np.log(2/(1+beta)));   

        return [self.learnerCumulativeLossVector,self.upperbound]

    def scalarMixture(self,beta,verbosity=0):
        
        result = self.mixture(beta)

        self.scalarPredictionMatrix = np.zeros([self.totalTime,self.vectorLength])

        mixedLossMatrix = np.zeros([self.vectorLength,self.totalTime])

        for component in range(self.vectorLength):
            if verbosity>=1:print("Running scalar algorithm on component",component,"...")
            
            setOfExperts = []
            for expert in range(self.noOfExperts):
                a = self.expertsPredictionMatrix[:,component,expert]
                #if a not in setOfExperts:
                #    setOfExperts.append(a)
                #    noOfComponentExperts = len(setOfExperts)
                #    componentExperts = np.zeros([self.totalTime,noOfComponentExperts])
                #for i in range(noOfComponentExperts):
                #    componentExperts[:,i] = setOfExperts[i]
        
            componentOutcomes = self.outcomeMatrix[component,:]
            #B = ScalarExpertsProblem(noOfComponentExperts,self.totalTime,componentExperts,componentOutcomes,0,0,verbosity)
            #componentResult = B.mixture(beta)
            #self.scalarPredictionMatrix[:,component] = B.predictionVector[:]
            #mixedLossMatrix[component,:] = componentResult[0]       
         
        self.componentwiseCLV = np.sqrt((sum(mixedLossMatrix**2))/self.vectorLength)    
        self.componentwiseCLV = accumulate(self.componentwiseCLV)
        self.learnerCumulativeLossVector = result[0]

        return [self.componentwiseCLV,self.learnerCumulativeLossVector]

class ScalarExpertsProblem(ExpertsProblem):

    def __init__(self, noOfExperts, totalTime, expertsPredictionMatrix, outcomeVector):

        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        self.expertsPredictionMatrix = expertsPredictionMatrix
        self.outcomeVector = outcomeVector

    def predict(self, experts_, outcomes, weights, beta):
        normalized_weights = weights/sum(weights)
        r = sum(normalized_weights * experts_)
        return(self.predictionFunction(r, beta))

    def mixture(self, beta):

        lossFunction = np.fabs
        expertsTotalLossVector = np.zeros(self.noOfExperts)
        totalLearnerLoss = 0
        self.learnerLossVector = np.zeros(self.totalTime)
        self.learnerCumulativeLossVector = np.zeros(self.totalTime)
        weightVector = np.ones(self.noOfExperts)
        self.predictionVector = np.zeros(self.totalTime)
        
        for t in range(self.totalTime):
            
            outcomeNow = self.outcomeVector[t]
            expertsPredictionNowVector = self.expertsPredictionMatrix[t,:]
            predictionNow = self.predict(expertsPredictionNowVector, outcomeNow, weightVector, beta)

            # COMPUTE PREDICTION
            self.predictionVector[t] = predictionNow
            
            # CALCULATE LEARNER LOSS
            lossNow = lossFunction(predictionNow - outcomeNow)
            self.learnerLossVector[t] = lossNow

            # CALCULATE EXPERT LOSS
            expertsLossNowVector = lossFunction(expertsPredictionNowVector - outcomeNow)
            
            # UPDATE STEP
            # self.update
            updateVector = self.updateFunction(expertsLossNowVector, beta)
            weightVector = weightVector * updateVector

        bestExpertLoss = np.min(expertsTotalLossVector)
        self.upperbound = (math.log(self.noOfExperts) - bestExpertLoss * math.log(beta)) / (2 * math.log(2 / (1 + beta)))

        return {"loss": self.learnerLossVector, "bound": self.upperbound}
