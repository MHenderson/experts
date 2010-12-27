#
# perm
#
# input : list
#
# output : next permutation in lexicographic order

def perm(L):
    
    M=L[:]
    largest=len(M)-1

    for j in range(len(M)-1):
        if M[j]<M[j+1]:
            largest=j

    if largest==len(M)-1:
        return M
    else:
        firstGreater=largest+1
        for i in range(largest+2,len(M)):
            if M[i]<M[firstGreater] and M[i]>M[largest]:
                firstGreater=i

        a = M[largest]
        b = M[firstGreater]
        M[largest]=b
        M[firstGreater]=a
        A = M[largest+1:len(M)]
        A.reverse()
        M = M[0:largest+1]+A
        return M
    
    

        
