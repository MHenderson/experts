import Gnuplot, Numeric, Experts, MLab
g = Gnuplot.Gnuplot(persist=1)

vectorLength = 70
totalTime = 20
noOfExperts = 50
beta = 0.2
A = Experts.VectorExpertsProblem(vectorLength,noOfExperts)
x = range(totalTime+1)
experts = Numeric.floor(2*MLab.rand(totalTime+1,A.vectorLength,A.noOfExperts))
outcomes = Numeric.floor(2*MLab.rand(A.vectorLength,totalTime+1))
A.expertsPredictionMatrix = experts
A.outcomeMatrix = outcomes
result = A.mixture(totalTime+1,beta,1,0,0)
y = result[0]
z = Numeric.repeat([result[1]],totalTime+1)

d3 = Gnuplot.Data(x,y,with='lines')
d4 = Gnuplot.Data(x,z,with='lines')
g.title('Vector Experts Experiment')
g.xlabel('Time');
g.ylabel('Loss');
g.plot(d3,d4)

#g.hardcopy(filename='tmp.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=18)
