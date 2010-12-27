import Numeric, Experts, MLab, random
from miscFunctions import *
from scipy import gplt

#psyco.full()

vectorLength = 3
noOfExperts = 4
totalTime = 6
beta = 0.1
noOfExperiments = 3

vectorResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)
scalarResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)

for i in range(noOfExperiments):
    
    experiment=str(i)
    reportFile = "C:\Documents and Settings\Matthew Henderson\My Documents\work\pythonwork\experts\\reports\\report"+experiment+".html"
    A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1)
    result = A.scalarMixture(beta)
    A.makeHTMLReport(reportFile)
    scalarResult = result[0]
    vectorResult = result[1]
    vectorResultMatrix[i,:] = vectorResult
    scalarResultMatrix[i,:] = scalarResult

x = range(totalTime)

vectorAverage = sum(vectorResultMatrix)/noOfExperiments
scalarAverage = sum(scalarResultMatrix)/noOfExperiments

a = gplt.plot(x,vectorAverage,x,scalarAverage)
