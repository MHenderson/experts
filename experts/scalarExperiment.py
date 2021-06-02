import Experts

import matplotlib.pyplot as plt

noOfExperts = 15
totalTime = 17
beta = 0.1

A = Experts.ScalarExpertsProblem(noOfExperts,totalTime,1,1,1,1,1)
result = A.mixture(beta)[0]

# Create plot and display it.
plt.plot(result)
plt.show()

# Create HTML report
A.makeHTMLReport()

# Create Gnuplot output
import Gnuplot
import Numeric
x = range(totalTime)
y = result[0]
z = Numeric.repeat([result[1]],totalTime)
#d3 = Gnuplot.Data(x,y)
d4 = Gnuplot.Data(x,z)
g = Gnuplot.Gnuplot(persist=1)
g.title('Mixture of Scalar Experts Experiment')
g.xlabel('Time');
g.ylabel('Loss');
g.plot(d4)
g.hardcopy(filename='tmp.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=18)
