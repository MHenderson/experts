#
#
#   ALGORITHMS
#
#   FROM "SURVEY PROPAGATION: AN ALGORITHM
#          FOR SATISFIABILITY" BY BRAUNSTEIN, MEZARD & ZECCHINA
#

import random, copy, math

# \theta(x) in this paper
def stepFunction(x):
    if x<=0:
        return 0
    else:
        return 1

#
#
#   WP ALGORITHM
#
#   Input : The factor graph of a Boolean formula in conjunctive normal
#           form; a maximal number of iterations TMAX
#   Output : UN-CONVERGED if WP has not converged after TMAX steps. If it
#             has converged: the set of all cavity biases.
#
#
def WP(satprob, TMAX):
    #TMAX = 10
    #
    # Here we initialise the cavities using the above function.
    #
    def initialCavities(clause):
        result = {}
        for variable in satprob.couplingDict[clause].keys():
            result[variable]=random.choice([0,1])
        return result

    #cavityBiasDict = {}
    for clause in satprob.clauseList:
            satprob.cavityBiasDict[clause] = initialCavities(clause)
    #
    # Here we initialise the fields in the same way.
    #
    def initialCavityField(clause):
        result = {}
        for variable in satprob.couplingDict[clause].keys():
            result[variable]=0
        return result

    #cavityFieldDict = {}
    for clause in satprob.clauseList:
        satprob.cavityFieldDict[clause] = initialCavityField(clause)

    # This positiveSum2 is used to compute the cavity field
    def positiveSum2(clause,variable):
        result=0
        for otherClause in satprob.otherClausesInvolvingPositively(clause,variable):
            result+=satprob.cavityBiasDict[otherClause][variable]
        return result

    # This negativeSum2 is also used in computing the cavity field.
    def negativeSum2(clause,variable):
        result=0
        for otherClause in satprob.otherClausesInvolvingNegatively(clause,variable):
            result+=satprob.cavityBiasDict[otherClause][variable]
        return result

    # This is the product needed for computing the cavity basis. Here the
    # X is an dictionary (called with X=cavityFieldDict).
    def product(clause,variable,X):
        result=1
        for otherVariable in satprob.otherVariablesInvolved(clause,variable):
            result*=stepFunction(X[clause][otherVariable]*satprob.couplingDict[clause][otherVariable])
        return result        

    for t in range(1,TMAX+1):
        #
        # make a copy of the edgeCavityList for comparison after
        # update 
        #    
        cavityBiasDictPrevious=copy.deepcopy(satprob.cavityBiasDict)
        #
        # Update cavity field
        #
        for clause in satprob.clauseList:
            for variable in satprob.cavityFieldDict[clause].keys():
                satprob.cavityFieldDict[clause][variable]=positiveSum2(clause,variable)-negativeSum2(clause,variable)    
        #
        # Update cavity biases
        #
        for clause in satprob.clauseList:
            for variable in satprob.cavityFieldDict[clause].keys():
                satprob.cavityBiasDict[clause][variable]=product(clause,variable,satprob.cavityFieldDict)       
        #
        #
        #  If convergence then return resultDict
        #
        convergence=1
        for clause in satprob.clauseList:
            for variable in satprob.cavityBiasDict[clause].keys():
                if satprob.cavityBiasDict[clause][variable]!=cavityBiasDictPrevious[clause][variable]:
                    convergence=0
        #
        #  If convergence return time and break
        #
        if convergence==1:
            return satprob.cavityBiasDict
            break

    if t==TMAX:
        return 'UN-CONVERGED'

#
#
#   WID ALGORITHM
#
#   Input : the factor graph of a Boolean formula in conjunctive normal form
#
#   Output : UN-CONVERGED, or status of the formula, SAT or UNSAT; If the
#            formula is SAT: one assignment which satisfies all clauses.
#


def WID(satprob,TMAX):
    while (satprob.noOfUnfixedVariables()>0):
        outcomeOfWP=WP(satprob,TMAX)
        if outcomeOfWP=='UN-CONVERGED':
            return outcomeOfWP
        else:
            # if there is at least one contradiction # = 1 return UNSAT
            for variable in satprob.variableList:
                if satprob.contradictionNumber(variable)==1:
                    return 'UNSAT'
            
            #    if there is at least one non-zero local field, fix variables
            #        and clean the graph
            for variable in satprob.variableList:
                if satprob.localField(variable)!=0:
                    # fix all variables with H_i!=0
                    for variable in satprob.variableList:
                        if satprob.localField(variable)!=0:
                            if satprob.localField(variable)>0:
                                # fix variable=1
                                satprob.fixedVariableDict[variable]=1
                            else:
                                # fix variable=0
                                satprob.fixedVariableDict[variable]=0
                satprob.cleanGraph()
                continue
           
            #    else
            #       chose and arbitrary unfixed variable, fix it and clean
            unfixedVariables=[]
            for variable in satprob.variableList:
                if variable not in satprob.fixedVariableDict.keys():
                    unfixedVariables.append(variable)
                    
            #
            # If, by the above procedure we fix all variables then return
            # assignment
            #
            if unfixedVariables==[]:
                for variable in satprob.variableList:
                    satprob.assignment[variable]=satprob.fixedVariableDict[variable]
                return satprob.assignment

            else:
                arbitraryUnfixedVariable = random.choice(unfixedVariables)
                satprob.fixedVariableDict[arbitraryUnfixedVariable]=random.choice([0,1])
                satprob.cleanGraph()

    for variable in satprob.variableList:
        satprob.assignment[variable]=satprob.fixedVariableDict[variable]
    return satprob.assignment

#
#
#   SP ALGORITHM
#
#   Input : the factor graph of a Boolean formula in conjunctive normal
#           form; a maximal number of iterations TMAX, a requested precision
#           eps.
#
#   Output : UN-CONVERGED if SP has not converged after TMAX sweeps. If it
#            has converged: the set of all cavity-bias-surveys.
#
#

def SP(satprob, TMAX, eps):
    #
    # randomly initialize the cavity bias surveys on all edges of the graph
    # (this ought to be part of SAT.py)
    #
    def initialCavities(clause):
        result = {}
        for variable in satprob.couplingDict[clause].keys():
            result[variable]=random.random()
        return result

    for clause in satprob.clauseList:
        satprob.cavityBiasDict[clause] = initialCavities(clause)

    #
    # Initialise the survey dictionaries randomly
    #
    def initialToOne(clause):
        result = {}
        for variable in satprob.couplingDict[clause].keys():
            result[variable]=1
        return result

    for clause in satprob.clauseList:
        satprob.uSurveyDict[clause] = initialToOne(clause)

    for clause in satprob.clauseList:
        satprob.sSurveyDict[clause] = initialToOne(clause)

    for clause in satprob.clauseList:
        satprob.zeroSurveyDict[clause] = initialToOne(clause)
   
    for t in range(1,TMAX+1):
        
        if t==TMAX:
            return 'UNCONVERGED'
        #
        # make a copy of the edgeCavityList for comparison after
        # update 
        #    
        cavityBiasDictPrevious=copy.deepcopy(satprob.cavityBiasDict)
        #
        # Update cavity bias surveys (from eqn 18)
        #
        for clause in satprob.clauseList:
            for variable in satprob.cavityBiasDict[clause].keys():
                satprob.uSurveyDict[clause][variable] = (1-satprob.uProd(clause,variable))*satprob.sProd(clause,variable)
                satprob.sSurveyDict[clause][variable] = (1-satprob.sProd(clause,variable))*satprob.uProd(clause,variable)
                satprob.zeroSurveyDict[clause][variable] = satprob.Prod(clause,variable)
                cavityBias = 1
        #
        # Now update the cavity biases (this is wasteful, should be
        # incorporated into the above loop)
        #
        for clause in satprob.clauseList:
            for variable in satprob.cavityBiasDict[clause].keys():
                tmpCavityBias=1
                for otherVariable in satprob.otherVariablesInvolved(clause,variable):
                    A = satprob.uSurveyDict[clause][otherVariable]
                    B = satprob.sSurveyDict[clause][otherVariable]
                    C = satprob.zeroSurveyDict[clause][otherVariable]
                    tmpCavityBias*=A/(A+B+C) # Here we should divide by A+B+C
                satprob.cavityBiasDict[clause][variable]=tmpCavityBias          
        #
        # If iteration has `converged' then return cavity bias dictionary
        #
        converge = 1
        for clause in satprob.clauseList:
            for variable in satprob.cavityBiasDict[clause]:
                if math.fabs(satprob.cavityBiasDict[clause][variable]-cavityBiasDictPrevious[clause][variable])>=eps:
                    converge = 0

        if converge == 1:
            return satprob.cavityBiasDict


def SID(satprob, TMAX, eps):
    print satprob.couplingDict
    SP(satprob,TMAX,eps)
    largestVar = satprob.variableList[0]
    largestVal = math.fabs(satprob.positiveBias(largestVar)-satprob.negativeBias(largestVar))
    for variable in satprob.variableList:
        newVal=math.fabs(satprob.positiveBias(variable)-satprob.negativeBias(variable))
        if newVal>largestVal:
            largestVar=variable
            largestVal=newVal
    if satprob.positiveBias(largestVar)>satprob.negativeBias(largestVar):
        satprob.fixedVariableDict[largestVar]=1
    else:
        satprob.fixedVariableDict[largestVar]=0
    satprob.cleanGraph()
    print satprob.couplingDict
        
                    
                    
                

