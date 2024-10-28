import copy
import numpy as np

def twoNorm(vector):
    length = vector.shape[0]
    return np.sqrt(sum(vector**2)/length)

def accumulate(vector):
    result = copy.deepcopy(vector)
    for i in range(len(vector)):
        if i==0:
            result[i] = result[i]
        else:
            result[i] = result[i]+result[i-1]
    return result 
    
def digit(x,base,i):
    return int((x/(base**i))%base)
