import Numeric, copy

def accumulate(vector):
    result = copy.deepcopy(vector)
    for i in range(len(vector)):
        if i==0:
            result[i] = result[i]
        else:
            result[i] = result[i]+result[i-1]
    return result
