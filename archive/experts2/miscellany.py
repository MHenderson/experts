# This file has important differences with the
# file miscFunctions.py
import Numeric, copy, Image, MLab, RandomArray

def twoNorm(vector):
    length = vector.shape[0]
    return Numeric.sqrt(sum(vector**2)/length)

def oneNorm(vector):
    length = vector.shape[0]
    return Numeric.sqrt(sum(vector**1)/length)

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
    
def array2HTML(array,precision=3,rowTitle='',colTitle='',caption=''):
    shape = Numeric.shape(array)
    x = shape[0]
    y = shape[1]
    result = []
    result = result + ['<table border cellspacing=0 cellpadding=5><caption>']
    result = result + [caption]
    result = result + ['</caption>']
    for i in range(x):
        result = result + ['<tr>']
        for j in range(y):
            result = result + ['<td>']
            number = str(array[i,j])
            number = number[:precision+2]
            result = result + [number]
            result = result + ['</td>']
        result = result + ['</tr>']
    result = result + ['</table>']
    string = ''
    for line in result:
	    string+=line
    return string
    
#
# returns grayscale image of array argument
#
def imagesc(array):
    array2 = array[:]
    dimensions = Numeric.shape(array2)
    x = dimensions[1]
    y = dimensions[0]
    #array2.shape = (1,x*y)
    array2 = Numeric.reshape(array2,(1,x*y))
    sequence = array2[0]
    im = Image.new('L',[x,y])
   # a = MLab.rand(100*100)
    z = Numeric.floor(255*sequence)
    im.putdata(z)
    return im

def noisfy(array):
    a = RandomArray.normal(0.95,0.05,array.shape)
    Numeric.clip(a,0.0,1.0)
    return a*array
