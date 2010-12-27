def digit(x,base,i):
    return int((x/(base**i))%base)

def allTuples(base,length):
    a = range(base**length)
    b = range(length)
    b.reverse()
    return [[digit(j,base,i) for i in b] for j in a]
