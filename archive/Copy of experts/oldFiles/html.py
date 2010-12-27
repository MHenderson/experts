import Numeric

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
    return result
