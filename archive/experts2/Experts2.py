import MLab, miscellany, Image, sets, Numeric, random

class ExpertsProblem:

    def __init__(self,noOfExperts,totalTime):
        # The following two constants are the essential parameters
        # for a given instance of an ExpertsProblem
        self.noOfExperts = noOfExperts
        self.totalTime = totalTime
        # The info and images dictionary contain, respectively, info and
        # images about the current problem instance. They are used to generate
        # reports.
        self.info = {}
        self.images = {}
        # The weightMatrix is updated by the mixture algorithm and the
        # column t is the weight vector at time t
        self.weightMatrix = MLab.ones((self.noOfExperts,self.totalTime),Numeric.Float)
        # The normalizedWeightMatrix is the same as the weightMatrix,
        # but normalized.
        self.normalizedWeightMatrix = MLab.ones((self.noOfExperts,self.totalTime),Numeric.Float)

class VectorExpertsProblem(ExpertsProblem):

    def __init__(self,vectorLength,noOfExperts,totalTime,expertsPredictionMatrix=0,outcomeMatrix=0,outcomeAsExpert=0,addNoise=0):
        # Call the init method of the parent class.
        ExpertsProblem.__init__(self,noOfExperts,totalTime)
        # The constant self.vectorLength is the dimension of the vector space.
        # In the subsequent line this parameter is entered in the info
        # dictionary.
        self.vectorLength = vectorLength
        # The predictionMatrix stores the predictions made by the mixture
        # algorithm
        self.predictionMatrix = MLab.zeros((self.vectorLength,self.totalTime),Numeric.Float)
        # The lossMatrix stores the loss of the algorithm at time t
        self.lossVector = MLab.zeros(self.totalTime,Numeric.Float)
        # If no experts prediction matrix is handed to the constructor then
        # create a random one of shape [vectorLength,noOfExperts,totalTime]
        # otherwise use the matrix handed in.
        if type(expertsPredictionMatrix)==int:
            self.expertsPredictionMatrix = MLab.rand(self.vectorLength,self.noOfExperts,self.totalTime)
        else:
            self.expertsPredictionMatrix = expertsPredictionMatrix
        # If no outcome matrix is handed to the constructor then create a
        # random one of shape [vectorLength,totalTime], otherwise use the vector
        # handed in.
        if type(outcomeMatrix)==int:
            self.outcomeMatrix = MLab.rand(self.vectorLength,self.totalTime)
            self.outcomeMatrix = Numeric.floor(2*self.outcomeMatrix)
        else:
            self.outcomeMatrix = outcomeMatrix
        # If outcomeAsExpert=1 then change the first experts prediction to
        # the outcomeVector
        if outcomeAsExpert==1:
            self.expertsPredictionMatrix[:,0,:]=self.outcomeMatrix[:,:]
        # If addNoise=1 then noisfy the outcomeVector
        if addNoise==1:
            self.expertsPredictionMatrix[:,0,:] = miscellany.noisfy(self.expertsPredictionMatrix[:,0,:])              
        # Produce an HTML report of the problem.
        # self.produceHTMLReport("report.html")

    def randomPseudoExpert(self):
        # Compute the max # of pseudoexperts    
        maxNoOfPseudoEx = 0
        for i in range(self.vectorLength):
            maxNoOfPseudoEx+=self.noOfExperts**i
        maxNoOfPseudoEx*=self.noOfExperts-1
        # Now pick the new pseudoExpert at random
        newPseudoExpert = random.randrange(maxNoOfPseudoEx)
        return newPseudoExpert        

    def addExpert(self,pseudoExpert):
        # Construct the prediction matrix for the new pseudoExpert
        pseudoExpertMatrix = MLab.zeros((self.vectorLength,self.totalTime),Numeric.Float)
        for i in range(self.vectorLength):
            componentExpert = miscellany.digit(pseudoExpert,self.noOfExperts,i)
            pseudoExpertMatrix[i,:]=self.expertsPredictionMatrix[i,componentExpert,:]    
        #  Construct the prediction matrix for the new problem instance
        newPredictionMatrix = MLab.zeros((self.vectorLength,self.noOfExperts+1,self.totalTime),Numeric.Float)
        newPredictionMatrix[:,0:self.noOfExperts,:] = self.expertsPredictionMatrix[:,:,:]
        newPredictionMatrix[:,self.noOfExperts,:] = pseudoExpertMatrix[:,:]
        return VectorExpertsProblem(self.vectorLength,self.noOfExperts+1,self.totalTime,newPredictionMatrix,self.outcomeMatrix,0,0)       

    def produceHTMLReport(self,filename):
        ''' Produces an HTML Report of the VectorExpertsProblem
            instance. '''
        self.info = {'Total Time':self.totalTime,'Number of Experts':self.noOfExperts,'Dimension':self.vectorLength}
        self.images['Outcome Vector Image'] = miscellany.imagesc(self.outcomeMatrix)
        self.info['Outcome Matrix'] = miscellany.array2HTML(self.outcomeMatrix)
        self.info['Weight Matrix'] = miscellany.array2HTML(self.weightMatrix)
        self.info['Normalized Weight Matrix'] = miscellany.array2HTML(self.normalizedWeightMatrix)
        self.info['Prediction Matrix'] = miscellany.array2HTML(self.predictionMatrix) 
        for i in range(self.noOfExperts):
            self.info['Expert ' +str(i) + ' Prediction Matrix'] = miscellany.array2HTML(self.expertsPredictionMatrix[:,i,:])
            self.images['Expert ' +str(i) + ' Prediction Matrix Image'] = miscellany.imagesc(self.expertsPredictionMatrix[:,i,:])
        # The constants reportDir, imagesDir and relativeimagesDir are all
        # strings for the directories where the reports and images are put.
        reportDir = "reports/"
        imagesDir = "reports/images/"
        relativeimagesDir = "images/" ## Here, relative means relative to
                                      ## reportDir
        # We add the reportDir path to the filename
        filename = reportDir+filename
        # Then open a file with the name: filename
        reportFile = open(filename,mode='w+')
        reportFile.writelines('<h1>Report</h1><hr>')
        # Each key/value pair in the info dictionary is then dumped into the
        # reportFile (we used a sorted list of the dictionary keys)
        sortedInfo = self.info.keys()
        sortedInfo.sort()
        for key in sortedInfo:
            reportFile.writelines('<br>'+str(key)+':<center> '+str(self.info[key])+' </center>')
        imagenumber = 0
        reportFile.writelines('<h1>Images</h1>')
        # Each image in the image dictionary is saved in a file in the imagesDir
        # and a line is added the the HTML report to load the image.
        sortedImages = self.images.keys()
        sortedImages.sort()
        for key in sortedImages:
            im = self.images[key]
            imagefile = imagesDir + "image" + str(imagenumber) +".jpeg"
            im.save(imagefile,"JPEG")
            imagefile = relativeimagesDir + "image" + str(imagenumber) + ".jpeg"
            reportFile.writelines('<hr>'+str(key)+':'+'<center><img src=' + imagefile + ' width="200" height="200"></img></center>')
            imagenumber+=1      

    def mixture(self,beta):
        weightVector = MLab.ones(self.noOfExperts,Numeric.Float)
##        predictionMatrix = MLab.zeros((self.vectorLength,self.totalTime),Numeric.Float)
        for t in range(self.totalTime):
            self.weightMatrix[:,t]=weightVector
            ###print "t",t
            ###print "weights",weightVector
            # Compute experts predictions at time t
            expertsPredictionNowMatrix = self.expertsPredictionMatrix[:,:,t]
            ###print "expertsPredictionNowMatrix",expertsPredictionNowMatrix
            # Compute normalized weightVector
            ###print sum(weightVector)
            normalizedWeightVector = weightVector/sum(weightVector)
            self.normalizedWeightMatrix[:,t]=normalizedWeightVector
            # Compute a matrix each row of which is the normalizedWeightVector
            normalizedWeightMatrix = Numeric.resize(normalizedWeightVector,(self.vectorLength,self.noOfExperts))
            # Compute vecrt
            vecrt = sum(Numeric.transpose(normalizedWeightMatrix*expertsPredictionNowMatrix))
            ###print "vecrt",vecrt
            # Compute prediction
            predictionNow = self.predictionFunction(vecrt,beta)
            ###print "prediction",predictionNow
            self.predictionMatrix[:,t] = predictionNow 
            # Get outcomes at this time
            outcomeNow = self.outcomeMatrix[:,t]
            outcomeNowMatrix = Numeric.transpose(Numeric.resize(outcomeNow,(self.noOfExperts,self.vectorLength)))
            # Update weightVector
            weightVector*=weightVector*self.updateFunction(self.lossFunction(expertsPredictionNowMatrix,outcomeNowMatrix),beta)
        # At the moment just return random prediction
        # self.produceHTMLReport("report.html")
        return self.predictionMatrix

    def updateFunction(self,value,beta):
        return 1-(1-beta)*value

    #
    # The new lossFunction really needs to be tested
    #

    def lossFunction(self,matrix1,matrix2):
        x = matrix1.shape[0]
        return Numeric.sqrt(sum((matrix1-matrix2)**2)/x)

##    def predictionFunction(self,vector,beta):
##        numerator = Numeric.log(1-vector+vector*beta)
##        denomTerm = Numeric.log(beta-beta*vector+vector)
##        denominatorInverse = 1.0/(numerator+denomTerm)
##        return numerator*denominatorInverse

    def predictionFunction(self,value,beta):
        c = ((1.0+beta)*Numeric.log(2.0/(1.0+beta)))/(2.0*(1.0-beta))
        zeroIndices = Numeric.less(value,0.5-c)
        oneIndices = Numeric.greater(value,0.5+c)
        r = 0.5-((1-2*value)/(4*c))
        r = Numeric.where(zeroIndices,0.0,r)
        r = Numeric.where(oneIndices,1.0,r)
        return r      

    def componentwiseScalarMixture(self,beta):
        predictionMatrix = MLab.zeros((self.vectorLength,self.totalTime),Numeric.Float)
        for i in range(self.vectorLength):
            # Get scalar experts
            scalarExperts = self.expertsPredictionMatrix[i,:,:]
            # Get scalar outcomes
            scalarOutcomes = MLab.zeros((self.totalTime),Numeric.Float)
            scalarOutcomes[:] = self.outcomeMatrix[i,:]
            # Create scalar problem with these experts and outcomes
            scalarProblem = ScalarExpertsProblem(self.noOfExperts,self.totalTime,scalarExperts,scalarOutcomes,0,0)
            # Compute result of scalar mixture
            result = scalarProblem.mixture(beta)
            # Put result into predictionMatrix
            predictionMatrix[i,:] = result
        return predictionMatrix

class ScalarExpertsProblem(ExpertsProblem):

    def __init__(self,noOfExperts,totalTime,expertsPredictionMatrix=0,outcomeMatrix=0,outcomeAsExpert=0,addNoise=0):
        # Call the init method of the parent class.
        ExpertsProblem.__init__(self,noOfExperts,totalTime)
        # The prediction vector
        self.predictionVector = MLab.zeros(self.totalTime,Numeric.Float)
        # If no experts prediction matrix is handed to the constructor then
        # create a random one of shape [noOfExperts,totalTime] otherwise use
        # the matrix handed in.
        if type(expertsPredictionMatrix)==int:
            self.expertsPredictionMatrix = MLab.rand(self.noOfExperts,self.totalTime)
        else:
            self.expertsPredictionMatrix = expertsPredictionMatrix
        # If no outcome matrix is handed to the constructor then create a
        # random one, otherwise use the matrix handed in.
        if type(outcomeMatrix)==int:
            self.outcomeMatrix = MLab.rand(self.totalTime)
            self.outcomeMatrix = MLab.floor(2*self.outcomeMatrix)
        else:
            self.outcomeMatrix = outcomeMatrix
        # If outcomeAsExpert=1 then change the first experts prediction to
        # the outcomeVector
        if outcomeAsExpert==1:
            self.expertsPredictionMatrix[0,:]=self.outcomeMatrix[:]
        # If addNoise=1 then noisfy the outcomeVector
        if addNoise==1:
            self.expertsPredictionMatrix[0,:] = miscellany.noisfy(self.expertsPredictionMatrix[0,:])
        # Produce an HTML report of the problem.        
        # self.produceHTMLReport("report.html")

    def updateFunction(self,value,beta):
        return 1-(1-beta)*value

    #
    # The new lossFunction really needs to be tested
    #

    def lossFunction(self,a,b):
        return Numeric.fabs(a-b)

##    def predictionFunction(self,vector,beta):
##        numerator = Numeric.log(1-vector+vector*beta)
##        denomTerm = Numeric.log(beta-beta*vector+vector)
##        denominatorInverse = 1.0/(numerator+denomTerm)
##        return numerator*denominatorInverse

    def predictionFunction(self,value,beta):
        c = (1.0+beta)*Numeric.log(2.0/(1.0+beta))/(2.0*(1.0-beta))
        if value<0.5-c:
            return 0.0
        elif value>0.5+c:
            return 1.0
        else:
            return 0.5-(1-2*value)/(4.0*c)

    def produceHTMLReport(self,filename):
        ''' Produces an HTML Report of the ScalarExpertsProblem
            instance. '''
        self.info = {'Total Time':self.totalTime,'Number of Experts':self.noOfExperts}
        self.info['Experts Prediction Matrix'] = miscellany.array2HTML(self.expertsPredictionMatrix)
        self.info['Outcome Matrix'] = str(self.outcomeMatrix)
        self.info['Prediction Vector'] = str(self.predictionVector)
        self.info['Normalized Weight Matrix'] = miscellany.array2HTML(self.normalizedWeightMatrix)
        self.info['Weight Matrix'] = miscellany.array2HTML(self.weightMatrix)
        self.images['Experts Prediction Matrix Image'] = miscellany.imagesc(self.expertsPredictionMatrix)
##        self.images['Outcome Vector Image'] = miscellany.imagesc(self.outcomeMatrix)
        # The constants reportDir, imagesDir and relativeimagesDir are all
        # strings for the directories where the reports and images are put.
        reportDir = "reports/"
        imagesDir = "reports/images/"
        relativeimagesDir = "images/" ## Here, relative means relative to reportDir
        # We add the reportDir path to the filename
        filename = reportDir+filename
        # Then open a file with the name: filename
        reportFile = open(filename,mode='w+')
        reportFile.writelines('<h1>Report</h1><hr>')
        # Each key/value pair in the info dictionary is then dumped into the
        # reportFile
        for key in self.info:
            reportFile.writelines('<br>'+str(key)+':<center> '+str(self.info[key])+' </center>')
        imagenumber = 0
        reportFile.writelines('<h1>Images</h1>')
        # Each image in the image dictionary is saved in a file in the imagesDir
        # and a line is added the the HTML report to load the image.
        for key in self.images:
            im = self.images[key]
            imagefile = imagesDir + "image" + str(imagenumber) +".jpeg"
            im.save(imagefile,"JPEG")
            imagefile = relativeimagesDir + "image" + str(imagenumber) + ".jpeg"
            reportFile.writelines('<hr>'+str(key)+':'+'<center><img src=' + imagefile + ' width="200" height="200"></img></center>')
            imagenumber+=1

##    def mixture(self,beta):
##        # Create expertsPredictionMatrix
##        vectorExpertsMatrix = MLab.zeros((1,self.noOfExperts,self.totalTime),Numeric.Float)
##        vectorExpertsMatrix[0,:,:] = self.expertsPredictionMatrix
##        # Create outcomeMatrix
##        outcomeMatrix =  self.outcomeMatrix
##        # Create vector problem of dimension 1 with
##        # this prediction and outcome matrix.
##        problem = VectorExpertsProblem(1,self.noOfExperts,self.totalTime,vectorExpertsMatrix,outcomeMatrix,0,0)
##        return problem.mixture(beta)

    def mixture(self,beta):

        weightVector = MLab.ones(self.noOfExperts,Numeric.Float)

        for t in range(self.totalTime):
            self.weightMatrix[:,t]=weightVector
            #
            # COMPUTE PREDICTION
            #
            expertsPredictionNowVector = self.expertsPredictionMatrix[:,t]
            outcomeNow = self.outcomeMatrix[t]
            normalizedWeightVector = weightVector/sum(weightVector)
            self.normalizedWeightMatrix[:,t]=normalizedWeightVector
            r = sum(normalizedWeightVector*expertsPredictionNowVector)
            predictionNow = self.predictionFunction(r,beta)
            self.predictionVector[t] = predictionNow
            #
            # UPDATE STEP
            #
            #print "outcome",outcomeNow
            #print "experts",expertsPredictionNowVector
            expertsLossNowVector = self.lossFunction(outcomeNow,expertsPredictionNowVector)
            #print "loss",expertsLossNowVector
            updateVector = self.updateFunction(expertsLossNowVector,beta)
            ##print "update",updateVector
            ##print "before",weightVector
            weightVector *= updateVector
            ##print "after",weightVector
            
        return self.predictionVector


