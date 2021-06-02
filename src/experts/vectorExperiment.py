import Experts

vectorLength = 15
noOfExperts = 20
totalTime = 25

A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1)

beta = 0.1

result = A.mixture(beta)

A.makeHTMLReport()

