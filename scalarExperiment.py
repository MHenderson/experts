import experts

from experts import problems

import matplotlib.pyplot as plt

noOfExperts = 15
totalTime = 17
beta = 0.1

A = experts.problems.ScalarExpertsProblem(noOfExperts,totalTime,1,1,1,1,1)
result = A.mixture(beta)[0]

# Create plot and display it.
plt.plot(result)
plt.show()

# Create HTML report
A.makeHTMLReport()
