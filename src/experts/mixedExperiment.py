import Experts
import random
import numpy as np

from miscFunctions import *
import matplotlib.pyplot as gplt

#psyco.full()

vectorLength = 3
noOfExperts = 4
totalTime = 6
beta = 0.1
noOfExperiments = 3

vectorResultMatrix = np.zeros([noOfExperiments,totalTime])
scalarResultMatrix = np.zeros([noOfExperiments,totalTime])

for i in range(noOfExperiments):
    
    experiment=str(i)
    reportFile = "report.html"
    A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1)
#    result = A.scalarMixture(beta)
#    A.makeHTMLReport(reportFile)
#    scalarResult = result[0]
#    vectorResult = result[1]
#    vectorResultMatrix[i,:] = vectorResult
#    scalarResultMatrix[i,:] = scalarResult

x = range(totalTime)

#vectorAverage = sum(vectorResultMatrix)/noOfExperiments
#scalarAverage = sum(scalarResultMatrix)/noOfExperiments
#
#a = gplt.plot(x,vectorAverage,x,scalarAverage)
