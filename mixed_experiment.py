import experts
from experts import problems

import numpy as np

vectorLength = 3
noOfExperts = 4
totalTime = 6
beta = 0.1
noOfExperiments = 3

vectorResultMatrix = np.zeros([noOfExperiments, totalTime])
scalarResultMatrix = np.zeros([noOfExperiments, totalTime])

for i in range(noOfExperiments):
    
    experiment = str(i)
    reportFile = "report.html"
    A = experts.problems.VectorExpertsProblem(vectorLength, noOfExperts, totalTime, 1, 1, 1, 1)
