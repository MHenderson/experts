import Gnuplot, Numeric, Experts, MLab
g = Gnuplot.Gnuplot(persist=1)

noOfExperts = 15
totalTime = 17
A = Experts.ScalarExpertsProblem(noOfExperts,totalTime,1,1,1,1,0)

beta = 0.1

result = A.mixture(beta)

A.makeHTMLReport()

##x = range(totalTime)
##y = result[0]
##z = Numeric.repeat([result[1]],totalTime)
##
##d3 = Gnuplot.Data(x,y,with='points')
##d4 = Gnuplot.Data(x,z,with='lines')
##g.title('Mixture of Scalar Experts Experiment')
##g.xlabel('Time');
##g.ylabel('Loss');
##g.plot(d3)
##
##g.hardcopy(filename='tmp.ps',enhanced=1,mode='eps',color=0,fontname='Times-Roman',fontsize=18)
