#
#
#   WARNING PASSING ALGORITHM
#
#   FROM "SURVEY PROPAGATION: AN ALGORITHM
#          FOR SATISFIABILITY" BY BRAUNSTEIN, MEZARD & ZECCHINA
#

import random, copy

#clauseList = ['a','b','c','d','e','f']
#variableList = [1,2,3,4,5,6]
#
# In this paper the array J has a clause represented by -1 and
# a negated clause represented by 1
#
#couplingDict = {'a':{1:-1,3:1},'b':{1:1,2:-1,4:-1},'c':{3:1,5:-1},'d':{3:1,4:1,5:-1},'e':{2:1,4:-1,6:-1},'f':{5:-1}}

clauseList = ['a','b','c','d','e','f','g','h','i']
variableList = [1,2,3,4,5,6,7,8]
couplingDict = {'a':{1:-1},'b':{2:1},'c':{1:1,2:-1,3:-1},'d':{3:1,4:-1},'e':{3:-1,5:-1},'f':{4:-1},'g':{4:-1,7:1},'h':{5:-1,8:-1},'i':{5:1,6:-1}}

edgeList = []
for clause in couplingDict.keys():
    for variable in couplingDict[clause].keys():
        edgeList.append([clause,variable])

# V(a)
def variablesInvolved(clause):
    return couplingDict[clause].keys()

# V(a)\{i}
def otherVariablesInvolved(clause,variable):
    result = variablesInvolved(clause)
    if result != [] and variable in result:
        result.remove(variable)
    return result

# C(i) (V(i) in this paper)
def clausesInvolving(variable):
    result = []
    for clause in clauseList:
        if variable in couplingDict[clause].keys():
            result.append(clause)
    return result

# C(i)\{i} (V(i)\{i} in this paper)
def otherClausesInvolving(clause,variable):
    result = clausesInvolving(variable)
    if result != [] and clause in result:
        result.remove(clause)
    return result        

# C-(i) (V-(i) in this paper)
def clausesInvolvingNegatively(variable):
    result = []
    for clause in clausesInvolving(variable):
        if couplingDict[clause][variable] == 1:
            result.append(clause)
    return result

# C+(i) (V+(i) in this paper)
def clausesInvolvingPositively(variable):
    result = []
    for clause in clausesInvolving(variable):
        if couplingDict[clause][variable] == -1:
            result.append(clause)
    return result

# C+(i)\{a} (V+(i)\{a} in this paper)
def otherClausesInvolvingPositively(clause,variable):
    result = clausesInvolvingPositively(variable)
    if result != [] and clause in result:
        result.remove(clause)
    return result

# C-(i)\{a} (V+(i)\{a} in this paper)
def otherClausesInvolvingNegatively(clause,variable):
    result = clausesInvolvingNegatively(variable)
    if result != [] and clause in result:
        result.remove(clause)
    return result

# \theta(x) in this paper
def stepFunction(x):
    if x<=0:
        return 0
    else:
        return 1

### u_{a->i} in this paper
##def cavityBias(clause,variable,time):
##    if time==0:
##        return random.choice([0,1])
##    else:
##        result=1
##        for otherVariable in otherVariablesInvolved(clause,variable):
##            result+=stepFunction(cavityField(clause,variable,time-1)*couplingDict[clause][otherVariable])
##        return result
##
### h_{j->a} in this paper
##def cavityField(clause,variable,time):
##    if time==0:
##        return 0
##    else:
##        result=0
##        sumOfOtherPositiveCavityBiases=0
##        sumOfOtherNegativeCavityBiases=0
##        for otherClause in otherClausesInvolvingPositively(clause,variable):
##            sumOfOtherPositiveCavityBiases+=cavityBias(clause,variable,time-1)
##        for otherClause in otherClausesInvolvingNegatively(variable,clause):
##            sumOfOtherNegativeCavityBiases+=cavityBias(clause,variable,time-1)
##        return sumOfOtherPositiveCavityBiases-sumOfOtherNegativeCavityBiases

#
#
#   MAIN BODY OF ALGORITHM
#
#   Input : The factor graph of a Boolean formula in conjunctive normal
#           form; a maximal number of iterations TMAX
#   Output : UN-CONVERGED if WP has not converged after TMAX steps. If it
#             has converged: the set of all cavity biases.
#
#
TMAX = 10
#
# Here we initialise the cavities using the above function.
#
def initialCavities(clause):
    result = {}
    for variable in couplingDict[clause].keys():
        result[variable]=random.choice([0,1])
    return result

cavityBiasDict = {}
for clause in clauseList:
        cavityBiasDict[clause] = initialCavities(clause)
#
# Here we initialise the biases in the same way.
#
def initialCavityField(clause):
    result = {}
    for variable in couplingDict[clause].keys():
        result[variable]=0
    return result

cavityFieldDict = {}
for clause in clauseList:
    cavityFieldDict[clause] = initialCavityField(clause)

# This positiveSum2 is used to compute the cavity field
def positiveSum2(clause,variable):
    result=0
    for otherClause in otherClausesInvolvingPositively(clause,variable):
        result+=cavityBiasDict[otherClause][variable]
    return result

# This negativeSum2 is also used in computing the cavity field.
def negativeSum2(clause,variable):
    result=0
    for otherClause in otherClausesInvolvingNegatively(clause,variable):
        result+=cavityBiasDict[otherClause][variable]
    return result

# This is the product needed for computing the cavity basis. Here the
# X is an dictionary (called with X=cavityFieldDict).
def product(clause,variable,X):
    result=1
    for otherVariable in otherVariablesInvolved(clause,variable):
        result*=stepFunction(X[clause][otherVariable]*couplingDict[clause][otherVariable])
    return result        

for t in range(1,TMAX+1):
    #
    # make a copy of the edgeCavityList for comparison after
    # update 
    #    
    cavityBiasDictPrevious=copy.deepcopy(cavityBiasDict)
    #
    # Update cavity field
    #
    for clause in clauseList:
        for variable in cavityFieldDict[clause].keys():
            cavityFieldDict[clause][variable]=positiveSum2(clause,variable)-negativeSum2(clause,variable)    
    #
    # Update cavity biases
    #
    for clause in clauseList:
        for variable in cavityFieldDict[clause].keys():
            cavityBiasDict[clause][variable]=product(clause,variable,cavityFieldDict)       
    #
    #
    #  If convergence then return resultDict
    #
    convergence=1
    for clause in clauseList:
        for variable in cavityBiasDict[clause].keys():
            if cavityBiasDict[clause][variable]!=cavityBiasDictPrevious[clause][variable]:
                convergence=0
    #
    #  If convergence return time and break
    #
    if convergence==1:
        print 'CONVERGENCE AFTER TIME =',t
        break

if t==TMAX:
    print 'DIVERGENCE'

def positiveSum(variable):
    result=0
    for clause in clausesInvolvingPositively(variable):
        result+=cavityBiasDict[clause][variable]
    return result

def negativeSum(variable):
    result=0
    for clause in clausesInvolvingNegatively(variable):
        result+=cavityBiasDict[clause][variable]
    return result

def localField(variable):
    return positiveSum(variable)-negativeSum(variable)

def contradictionNumber(variable):
    if positiveSum(variable)*negativeSum(variable)>0:
        return 1
    else:
        return 0
