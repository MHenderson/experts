import Gnuplot, Numeric, Experts, MLab, random
from miscFunctions import *

#psyco.full()

g = Gnuplot.Gnuplot(persist=1)

verbosity=0

vectorLength = 20
noOfExperts = 20
totalTime = 15
beta = 0.1
noOfExperiments = 3

vectorResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)
scalarResultMatrix = Numeric.zeros([noOfExperiments,totalTime],Numeric.Float)

for i in range(noOfExperiments):
    
    reportFile = 'reportFiles/report' + str(i+1) + '.html'
    if verbosity>=1: print "--------------------------------------------------------------\n","Experiment: ",i+1
    A = Experts.VectorExpertsProblem(vectorLength,noOfExperts,totalTime,1,1,1,1,verbosity)
    if verbosity>=2: imagesc(A.outcomeMatrix).show()
    if verbosity>=4: print "Outcomes:\n",A.outcomeMatrix
    result = A.scalarMixture(beta,verbosity)
    #A.makeHTMLReport(reportFile)
    scalarResult = result[0]
    vectorResult = result[1]
    vectorResultMatrix[i,:] = vectorResult
    scalarResultMatrix[i,:] = scalarResult

    if verbosity>=1: print "--------------------------------------------------------------"

x = range(totalTime)

vectorAverage = sum(vectorResultMatrix)/noOfExperiments
scalarAverage = sum(scalarResultMatrix)/noOfExperiments

vectorData = Gnuplot.Data(x,vectorAverage,with='lines',title='Mixture of vector experts')
scalarData = Gnuplot.Data(x,scalarAverage,with='lines',title='Componentwise scalar mixture')

#g.title('Mixture of Vector Experts Experiment')
g.xlabel('Time');
g.ylabel('Cumulative Loss');
#g('set term png small color')
#g('set output "tmp.png"')
g.plot(vectorData,scalarData)

g.hardcopy(filename='reportFiles/tmp.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=18)
