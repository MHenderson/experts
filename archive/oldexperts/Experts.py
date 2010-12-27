import Numeric, MLab, random, Gnuplot
from miscFunctions import *

class ExpertsProblem:

    def predictionFunction(self,value,beta):
        c = ((1+beta)*Numeric.log(2/(1+beta)))/(2*(1-beta));
        if Numeric.size(value)==1:
            if value<=0.5-c:
                return 0
            elif value<0.5+c and value>0.5-c:
                return 0.5-((1-2*value)/(4*c))
            else:
                return 1
        else:
            zeroIndices = Numeric.less(value,0.5-c)
            oneIndices = Numeric.greater(value,0.5+c)
            r = 0.5-((1-2*value)/(4*c))
            r = Numeric.where(zeroIndices,0.0,r)
            r = Numeric.where(oneIndices,1.0,r)
            return r
        
    def twoNorm(self,vector):
        length = vector.shape[0]
        return Numeric.sqrt(sum(vector**2)/length)

    def update(self,value,beta):
        return 1-(1-beta)*value
                           
class VectorExpertsProblem(ExpertsProblem):
    
    def __init__(self,vectorLength,noOfExperts,totalTime,expertsPredictionMatrix=[],outcomeMatrix=[],outcomeAsExpert=0,addNoise=0,verbosity=0):
        self.vectorLength = vectorLength
        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        self.componentwiseCLV = ["Didn\'t run componentwise scalar mixture"]
        self.scalarPredictionMatrix = ["Didn\'t run componentwise scalar mixture"]
        if type(expertsPredictionMatrix)==int:
            if verbosity>=1: print "Randomizing Vector Experts..."
            self.expertsPredictionMatrix = MLab.rand(self.totalTime,self.vectorLength,self.noOfExperts)
        else:
            self.expertsPredictionMatrix = expertsPredictionMatrix
        if type(outcomeMatrix)==int:
            if verbosity>=1: print "Randomizing Vector Outcomes..."
            self.outcomeMatrix = Numeric.floor(2*MLab.rand(self.vectorLength,self.totalTime))
        else:
            self.outcomeMatrix = outcomeMatrix
        if outcomeAsExpert==1:
            if verbosity>=1: print "Introducing outcome as expert..."
            for t in range(self.totalTime):
                self.expertsPredictionMatrix[t,:,self.noOfExperts-1]=self.outcomeMatrix[:,t]
        if addNoise==1:
            if verbosity>=1: print "Adding noise to outcome-expert..."
            self.addNoise(self.noOfExperts-1,self.totalTime)

    def makeHTMLReport(self,filename='reportFiles/report.html'):
        #
        # OPEN FILE & WRITE TITLE
        #
        reportFile = open(filename,mode='w+')
        reportFile.writelines(['<h1>Vector Experts Experiment HTML Report</h1>'])
        #
        # OUTCOME IMAGE
        #
        #outcomesImg = imagesc(self.outcomeMatrix)
        #outcomesImg.save("reportFiles/outcomes.png")
        #reportFile.writelines(['<hr><h2>Outcomes</h2><img src="reportFiles/outcomes.png"></img><br>'])
        #
        # OUTCOME TABLE
        #
        reportFile.writelines(['<hr><h2>Outcomes</h2>'])
        reportFile.writelines(array2HTML(Numeric.transpose(self.outcomeMatrix),3,'rowtitle','coltitle','Outcome Matrix'))
        #
        # PREDICTION TABLE
        #
        reportFile.writelines(['<hr><h2>Predictions</h2>'])
        reportFile.writelines(array2HTML(self.predictionMatrix,3,'rowtitle','coltitle','Vector Prediction Matrix'))
        if type(self.scalarPredictionMatrix[0])==str:
            reportFile.writelines(self.scalarPredictionMatrix[0])
        else:
            reportFile.writelines(array2HTML(self.scalarPredictionMatrix,3,'rowtitle','coltitle','Scalar Prediction Matrix'))
        #
        # CUMULATIVE LOSS TABLE
        #
        reportFile.writelines(['<hr><h2>Cumulative Loss (Vector Mixture)</h2>'])
        reportFile.writelines(str(self.learnerCumulativeLossVector))
        #
        # CUMULATIVE LOSS TABLE
        #
        reportFile.writelines(['<hr><h2>Cumulative Loss (Componentwise Scalar Mixture)</h2>'])
        reportFile.writelines(str(self.componentwiseCLV))
        #
        # EXPERTS IMAGE
        #
        #reportFile.writelines(['<hr><h2>Experts</h2><img src="reportFiles/experts.png"></img>'])
        #
        # EXPERTS TABLE
        #
        reportFile.writelines(['<hr><h2>Experts</h2>'])
        for i in range(self.noOfExperts):
            caption = 'Expert '+str(i)
            reportFile.writelines(array2HTML(self.expertsPredictionMatrix[:,:,i],3,'rowtitle','coltitle',caption))
            reportFile.writelines('<br>')
        #
        # PLOTS
        #
        g = Gnuplot.Gnuplot(persist=1)
        w = self.componentwiseCLV
        x = range(self.totalTime)
        y = self.learnerCumulativeLossVector
        z = Numeric.repeat([self.upperbound],self.totalTime)
        
        lossData = Gnuplot.Data(x,y,with='lines')
        upperboundData = Gnuplot.Data(x,z,with='lines')

        g.title('Vector Experts Experiment')
        g.xlabel('Time')
        g.ylabel('Loss')
        g('set term png small color')
        g('set output "reportFiles/plot.png"')

        if type(w[0])==str:
            g.plot(lossData,upperboundData)

        else:
            componentwiseLossData = Gnuplot.Data(x,w,with='lines')
            g.plot(lossData,upperboundData,componentwiseLossData)

        reportFile.writelines(['<hr><h2>Plot of Loss</h2><img src="reportFiles/plot.png">Plot</img>'])


    def addNoise(self,expert,totalTime):
        
        for i in range(totalTime):
            for j in range(self.vectorLength):
                a = random.gauss(0,0.1)
                if 0<=a+self.expertsPredictionMatrix[i,j,expert]<=1:
                    self.expertsPredictionMatrix[i,j,expert] = a+self.expertsPredictionMatrix[i,j,expert] 
    
    def mixture(self,beta):

        lossFunction = self.twoNorm
        expertsLosses = Numeric.zeros(self.noOfExperts,Numeric.Float)
        expertsCumulativeLossMatrix = Numeric.zeros([self.totalTime,self.noOfExperts],Numeric.Float)
        totalLearnerLoss = 0
        self.learnerCumulativeLossVector = Numeric.zeros(self.totalTime,Numeric.Float)
        weightVector = Numeric.ones(self.noOfExperts,Numeric.Float)
        self.predictionMatrix = Numeric.zeros([self.totalTime,self.vectorLength],Numeric.Float)

        for t in range(self.totalTime):
            #
            # COMPUTE PREDICTION
            #
            expertsPredictionMatrixNow = self.expertsPredictionMatrix[t,:,:]
            outcomeNow = self.outcomeMatrix[:,t]
            normalizedWeightVector = weightVector/sum(weightVector)
            normalizedWeightVectorMatrix = MLab.repeat(normalizedWeightVector,self.vectorLength)
            normalizedWeightVectorMatrix.shape = (self.noOfExperts,self.vectorLength)
            normalizedWeightVectorMatrix = Numeric.transpose(normalizedWeightVectorMatrix)
            productNow = expertsPredictionMatrixNow*normalizedWeightVectorMatrix
            productNow = Numeric.transpose(productNow)
            vecrNow = sum(productNow)
            predictionNow = self.predictionFunction(vecrNow,beta)
            self.predictionMatrix[t,:] = predictionNow
            #
            # CALCULATE LEARNER LOSS
            #
            learnerLossNow = lossFunction(predictionNow-outcomeNow)
            totalLearnerLoss = totalLearnerLoss + learnerLossNow
            self.learnerCumulativeLossVector[t] = totalLearnerLoss
            #
            # CALCULATE EXPERT LOSSES
            #
            outcomeNowMatrix = Numeric.repeat(outcomeNow,self.noOfExperts)
            outcomeNowMatrix.shape = (self.vectorLength,self.noOfExperts)
            expertLossMatrixNow = expertsPredictionMatrixNow - outcomeNowMatrix
            expertLossNowVector = Numeric.zeros(self.noOfExperts,Numeric.Float)
            for i in range(self.noOfExperts):
                expertLossNowVector[i] = lossFunction(expertLossMatrixNow[:,i])
                expertsCumulativeLossMatrix[t,i] = expertsCumulativeLossMatrix[t-1,i]+expertLossNowVector[i]
            #
            # UPDATE STEP
            #
            weightVector = weightVector*self.update(expertLossNowVector,beta)
        #
        # CALCULATE THEORETICAL UPPER BOUND
        #
        expertsLosses = expertsCumulativeLossMatrix[self.totalTime-1,:]
        bestExpertLoss = MLab.min(expertsLosses);
        self.upperbound = (Numeric.log(self.noOfExperts)-bestExpertLoss*Numeric.log(beta))/(2*Numeric.log(2/(1+beta)));   

        return [self.learnerCumulativeLossVector,self.upperbound]

    def scalarMixture(self,beta,verbosity=0):
        
        result = self.mixture(beta)

        self.scalarPredictionMatrix = Numeric.zeros([self.totalTime,self.vectorLength],Numeric.Float)

        mixedLossMatrix = Numeric.zeros([self.vectorLength,self.totalTime],Numeric.Float)

        for component in range(self.vectorLength):
            if verbosity>=1:print "Running scalar algorithm on component",component,"..."
            componentExperts = self.expertsPredictionMatrix[:,component,:]
            componentOutcomes = self.outcomeMatrix[component,:]
            B = ScalarExpertsProblem(self.noOfExperts,self.totalTime,componentExperts,componentOutcomes,0,0,verbosity)
            componentResult = B.mixture(beta)
            self.scalarPredictionMatrix[:,component] = B.predictionVector[:]
            mixedLossMatrix[component,:] = componentResult[0]       
         
        self.componentwiseCLV = Numeric.sqrt((sum(mixedLossMatrix**2))/self.vectorLength)    
        self.componentwiseCLV = accumulate(self.componentwiseCLV)
        self.learnerCumulativeLossVector = result[0]

        return [self.componentwiseCLV,self.learnerCumulativeLossVector]

class ScalarExpertsProblem(ExpertsProblem):

    def __init__(self,noOfExperts,totalTime,expertsPredictionMatrix=[],outcomeVector=[],outcomeAsExpert=0,addNoise=0,verbosity=0):
        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        if type(expertsPredictionMatrix)==int:
            if verbosity>=3: print "Randomizing scalar experts..."
            self.expertsPredictionMatrix = MLab.rand(totalTime,self.noOfExperts)
        else:
            if verbosity>=3: print "Using given scalar experts..." 
            self.expertsPredictionMatrix = expertsPredictionMatrix
        if type(outcomeVector)==int:
            if verbosity>=3: print "Randomizing scalar outcomes..."
            self.outcomeVector = Numeric.floor(2*MLab.rand(totalTime))
        else:
            if verbosity>=3: print "Using given scalar outcomes..."
            self.outcomeVector = outcomeVector
        if outcomeAsExpert==1:
            if verbosity>=3: print "Introducing scalar outcomes as scalar expert..."
            self.expertsPredictionMatrix[:,self.noOfExperts-1]=self.outcomeVector
        if addNoise==1:
            if verbosity>=3: print "Adding noise to outcome-expert..."
            for t in range(totalTime):
                a = random.gauss(0,0.01)
                if 0<=a+self.expertsPredictionMatrix[t,self.noOfExperts-1]<=1:
                    self.expertsPredictionMatrix[t,self.noOfExperts-1]=a+self.expertsPredictionMatrix[t,self.noOfExperts-1] 

    def mixture(self,beta):

        lossFunction = Numeric.fabs
        expertsTotalLossVector = Numeric.zeros(self.noOfExperts,Numeric.Float)
        totalLearnerLoss = 0
        self.learnerLossVector = Numeric.zeros(self.totalTime,Numeric.Float)
        self.learnerCumulativeLossVector = Numeric.zeros(self.totalTime,Numeric.Float)
        weightVector = Numeric.ones(self.noOfExperts,Numeric.Float)
        self.predictionVector = Numeric.zeros(self.totalTime,Numeric.Float)
        
        for t in range(self.totalTime):
            #
            # COMPUTE PREDICTION
            #
            expertsPredictionNowVector = self.expertsPredictionMatrix[t,:]
            outcomeNow = self.outcomeVector[t]
            normalizedWeightVector = weightVector/sum(weightVector)
            r = sum(normalizedWeightVector*expertsPredictionNowVector)
            predictionNow = self.predictionFunction(r,beta)
            self.predictionVector[t] = predictionNow
            #
            # CALCULATE LOSSES
            #
            lossNow = lossFunction(predictionNow-outcomeNow)
            self.learnerLossVector[t] = lossNow
            totalLearnerLoss = totalLearnerLoss+lossFunction(predictionNow-outcomeNow)
            self.learnerCumulativeLossVector[t]=totalLearnerLoss
            expertsLossNowVector = lossFunction(expertsPredictionNowVector-outcomeNow)
            expertsTotalLossVector = expertsTotalLossVector + expertsLossNowVector
            #
            # UPDATE STEP
            #
            updateVector = self.update(expertsLossNowVector,beta)
            weightVector = weightVector*updateVector
            
        bestExpertLoss = MLab.min(expertsTotalLossVector)
        self.upperbound = (Numeric.log(self.noOfExperts)-bestExpertLoss*Numeric.log(beta))/(2*Numeric.log(2/(1+beta)));
        return [self.learnerLossVector,self.learnerCumulativeLossVector,self.upperbound]

    def makeHTMLReport(self,filename='report.html'):
        #
        # OPEN FILE & WRITE TITLE
        #
        reportFile = open(filename,mode='w+')
        reportFile.writelines(['<h1>Scalar Experts Experiment HTML Report</h1>'])
        #
        # OUTCOME IMAGE
        #
        #outcomesImg = imagesc(self.outcomeMatrix)
        #outcomesImg.save("reportFiles/outcomes.png")
        #reportFile.writelines(['<hr><h2>Outcomes</h2><img src="reportFiles/outcomes.png"></img><br>'])
        #
        # OUTCOME TABLE
        #
        reportFile.writelines(['<hr><h2>Outcomes</h2>'])
        reportFile.writelines(str(self.outcomeVector))
        #
        # PREDICTION TABLE
        #
        reportFile.writelines(['<hr><h2>Predictions</h2>'])
        reportFile.writelines(str(self.predictionVector))
        #
        # CUMULATIVE LOSS TABLE
        #
        reportFile.writelines(['<hr><h2>Cumulative Loss</h2>'])
        reportFile.writelines(str(self.learnerCumulativeLossVector))
        #
        # EXPERTS IMAGE
        #
        #reportFile.writelines(['<hr><h2>Experts</h2><img src="reportFiles/experts.png"></img>'])
        #
        # EXPERTS TABLE
        #
        reportFile.writelines(['<hr><h2>Experts</h2>'])
        for i in range(self.noOfExperts):
            reportFile.writelines('Expert ')
            reportFile.write(str(i))
            reportFile.writelines(': ')
            reportFile.writelines(str(self.expertsPredictionMatrix[:,i]))
            reportFile.writelines('<br>')
        #
        # PLOT
        #
        g = Gnuplot.Gnuplot(persist=1)
        x = range(self.totalTime)
        y = self.learnerCumulativeLossVector
        z = Numeric.repeat([self.upperbound],self.totalTime)

        lossData = Gnuplot.Data(x,y,with='lines')
        upperboundData = Gnuplot.Data(x,z,with='lines')

        g.title('Scalar Experts Experiment')
        g.xlabel('Time')
        g.ylabel('Loss')
        g('set term png small color')
        g('set output "reportFiles/plot.png"')
        g.plot(lossData,upperboundData)

        reportFile.writelines(['<hr><h2>Plot of Loss</h2><img src="reportFiles/plot.png">Plot</img>'])
       





        
