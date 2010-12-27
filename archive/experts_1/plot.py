import Gnuplot, Numeric, Experts, MLab
g = Gnuplot.Gnuplot(persist=1)


noOfExperts = 100
totalTime = 30
beta = 0.2
A = Experts.ScalarExpertsProblem(noOfExperts)
A.expertsPredictionMatrix = Numeric.floor(2*MLab.rand(totalTime+1,A.noOfExperts))
A.outcomeVector = Numeric.floor(2*MLab.rand(totalTime+1))
x = range(totalTime+1)
result = A.mixture(totalTime+1,beta,1,1,1,1)
y = result[0]
z = Numeric.repeat([result[1]],totalTime+1)

d3 = Gnuplot.Data(x,y,with='points')
d4 = Gnuplot.Data(x,z,with='lines')
g.title('Scalar Experts Experiment')
g.xlabel('Time');
g.ylabel('Loss');
g.plot(d3,d4)

g.hardcopy(filename='tmp.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=18)
