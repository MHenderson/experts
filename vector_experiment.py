import experts
from experts import problems

vectorLength = 15
noOfExperts = 20
totalTime = 25

A = experts.problems.VectorExpertsProblem(vectorLength, noOfExperts, totalTime, 1, 1, 1, 1)

beta = 0.1

result = A.mixture(beta)

A.makeHTMLReport()
