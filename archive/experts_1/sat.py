import random, math, graph

def random3clause(variables):
    tempvariables = variables[:]
    result={}
    for i in range(3):
        random.shuffle(tempvariables)
        variable = tempvariables.pop()
        result[variable]=random.choice([-1,1])
    return result

def random3SAT(noOfClauses,noOfVariables):
    possibleClauses = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    clauseList = possibleClauses[:noOfClauses]
    variableList = range(1,noOfVariables+1)
    couplingDict = {}
    for clause in clauseList:
        couplingDict[clause] = random3clause(variableList)
    return SATPROB(clauseList,variableList,couplingDict)      

class SATPROB:
    
    clauseList = []
    variableList = []
    couplingDict = {}
    edgeList = []
    cavityBiasDict = {}
    cavityFieldDict = {}
    fixedVariableDict = {}
    uSurveyDict = {}
    sSurveyDict = {}
    zeroSurveyDict = {}
    assignment = {}

    def __init__(self,clauses,variables,couplings):
        self.clauseList=clauses
        self.variableList=variables
        self.couplingDict=couplings
                
        for clause in self.couplingDict.keys():
            for variable in self.couplingDict[clause].keys():
                self.edgeList.append([clause,variable])

    # V(a)
    def variablesInvolved(self,clause):
        return self.couplingDict[clause].keys()

    # V(a)\{i}
    def otherVariablesInvolved(self,clause,variable):
        result = self.variablesInvolved(clause)
        if result != [] and variable in result:
            result.remove(variable)
        return result

    # C(i) (V(i) in this paper)
    def clausesInvolving(self,variable):
        result = []
        for clause in self.clauseList:
            if variable in self.couplingDict[clause].keys():
                result.append(clause)
        return result

    # C(i)\{i} (V(i)\{i} in this paper)
    def otherClausesInvolving(self,clause,variable):
        result = self.clausesInvolving(variable)
        if result != [] and clause in result:
            result.remove(clause)
        return result

    # C-(i) (V-(i) in this paper)
    def clausesInvolvingNegatively(self,variable):
        result = []
        for clause in self.clausesInvolving(variable):
            if self.couplingDict[clause][variable] == 1:
                result.append(clause)
        return result

    # C+(i) (V+(i) in this paper)
    def clausesInvolvingPositively(self,variable):
        result = []
        for clause in self.clausesInvolving(variable):
            if self.couplingDict[clause][variable] == -1:
                result.append(clause)
        return result

    # C+(i)\{a} (V+(i)\{a} in this paper)
    def otherClausesInvolvingPositively(self,clause,variable):
        result = self.clausesInvolvingPositively(variable)
        if result != [] and clause in result:
            result.remove(clause)
        return result

    # C-(i)\{a} (V+(i)\{a} in this paper)
    def otherClausesInvolvingNegatively(self,clause,variable):
        result = self.clausesInvolvingNegatively(variable)
        if result != [] and clause in result:
            result.remove(clause)
        return result

    # V_a^s(j) (or C_a^s(j))
    def otherLocalSatisfyingClauses(self,clause,variable):
        if self.couplingDict[clause][variable]==1:
            return self.otherClausesInvolvingNegatively(clause,variable)
        else:
            return self.otherClausesInvolvingPositively(clause,variable)

    # V_a^u(j) (or C_a^u(j))
    def otherLocalUnsatisfyingClauses(self,clause,variable):
        if self.couplingDict[clause][variable]==1:
            return self.clausesInvolvingPositively(variable)
        else:
            return self.clausesInvolvingNegatively(variable)

    def generalProd(self,variable,clauseSubset):
        result=1
        for clause in clauseSubset:
            result*=1-self.cavityBiasDict[clause][variable]
        return result

    def sProd(self,clause,variable):
        return self.generalProd(variable,self.otherLocalSatisfyingClauses(clause,variable))
       
    def uProd(self,clause,variable):
        return self.generalProd(variable,self.otherLocalUnsatisfyingClauses(clause,variable))

    def Prod(self,clause,variable):
        return self.generalProd(variable,self.otherClausesInvolving(clause,variable))

    def positiveProd(self,variable):
        return self.generalProd(variable,self.clausesInvolvingPositively(variable))

    def negativeProd(self,variable):
        return self.generalProd(variable,self.clausesInvolvingNegatively(variable))
        

    # \hat{PI}_I^+ (eq 21 pg 11)
    def positiveSurvey(self,variable):
        return (1-self.positiveProd(variable))*self.negativeProd(variable)
        
    # \hat{\Pi}_i^-
    def negativeSurvey(self,variable):
        return (1-self.positiveProd(variable))*self.positiveProd(variable)

    # \hat{\Pi}_i^0
    def zeroSurvey(self,variable):
        return self.generalProd(variable,self.clausesInvolving(variable))

    # Positive Bias W_i^+ (eq 22 on pg 11)
    def positiveBias(self,variable):
        return self.positiveSurvey(variable)/(self.positiveSurvey(variable)+self.negativeSurvey(variable)+self.zeroSurvey(variable))

    # Negative Bias W_i^-
    def negativeBias(self,variable):
        return self.negativeSurvey(variable)/(self.positiveSurvey(variable)+self.negativeSurvey(variable)+self.zeroSurvey(variable))

    # Zero Bias W_i^0
    def zeroBias(self,variable):
        return 1-self.positiveBias(variable)-self.negativeBias(variable)

    # Sigma_a (eqn 26 pg 11)
    # check that I am using log to the correct base here
    def clauseComplexity(self,clause):
        firstTerm=1
        for variable in self.variablesInvolved(clause):
            firstTerm*=(self.uSurveyDict[clause][variable]+self.sSurveyDict[clause][variable]+self.zeroSurveyDict[clause][variable])
        secondTerm=1
        for variable in self.variablesInvolved(clause):
            secondTerm*=self.uSurveyDict[clause][variable]
        return math.log(firstTerm-secondTerm)

    def variableComplexity(self,variable):
        return math.log(self.positiveSurvey(variable)+self.positiveSurvey(variable)+self.zeroSurvey(variable))

    def degree(self,variable):
        result=0
        for clause in self.clausesInvolving(variable):
            result+=1
        return result
    
    def complexity(self):
        result=0
        for clause in self.clauseList:
            result+=self.clauseComplexity(clause)
        for variable in self.variableList:
            result-=(self.degree(variable)-1)*self.variableComplexity(variable)
        return result

    def positiveSum(self,variable):
        result=0
        for clause in self.clausesInvolvingPositively(variable):
            result+=self.cavityBiasDict[clause][variable]
        return result

    def negativeSum(self,variable):
        result=0
        for clause in self.clausesInvolvingNegatively(variable):
            result+=self.cavityBiasDict[clause][variable]
        return result

    def localField(self,variable):
        return self.positiveSum(variable)-self.negativeSum(variable)

    def contradictionNumber(self,variable):
        if self.positiveSum(variable)*self.negativeSum(variable)>0:
            return 1
        else:
            return 0

    def fixVariables(self,fixDict):
        self.fixedVariableDict = fixDict
        for variable in self.fixedVariableDict.keys():
            self.assignment[variable]=self.fixedVariableDict[variable]

    def allVariablesAssigned(self,clause):
        result=1
        for variable in self.variablesInvolved(clause):
            if variable not in self.fixedVariableDict:
                result=0
        return result

    def noOfUnfixedVariables(self):
        return len(self.variableList)-len(self.fixedVariableDict.keys())

    def clauseSatisfied(self,clause):
        result=0
        if self.assignment == {}:
            return result        
        if self.allVariablesAssigned(clause)==0:
            return result
        else:
            for variable in self.variablesInvolved(clause):
                if self.couplingDict[clause][variable]==-1:
                    result=result or self.assignment[variable]
                else:
                    result=result or int(not self.assignment[variable])
        return result

    def prune(self,clause):
        result = {}
        for variable in self.variablesInvolved(clause):
            if variable not in self.fixedVariableDict.keys():
                result[variable]=self.couplingDict[clause][variable]
        return result                

    def cleanGraph(self):
        # remove satisfied clauses
        for clause in self.clauseList:
            if self.clauseSatisfied(clause):
                self.clauseList.remove(clause)
        newCouplingDict={}
        for clause in self.clauseList:
            newCouplingDict[clause]=self.couplingDict[clause]
        self.couplingDict=newCouplingDict
        # reduce clauses involving fixed variables
        newCouplingDict2={}
        for clause in self.clauseList:
            newCouplingDict2[clause]=self.prune(clause)
        self.couplingDict=newCouplingDict2

    def factorGraph(self):
        y = self.variableList[:]
        z = self.clauseList[:]
        vertices = y+z
        edges = [[clause,variable] for clause in self.clauseList for variable in self.variablesInvolved(clause) if self.couplingDict[clause][variable] in [-1,1]]
        adjacencies = dict(zip(vertices,[[y for y in vertices if [x,y] in edges] for x in vertices]))
        return graph.Graph(vertices, edges, adjacencies)
