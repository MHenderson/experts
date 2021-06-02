import Image, MLab, Numeric
#
# returns grayscale image of array argument
#
def imagesc(array):
    array2 = array[:]
    dimensions = Numeric.shape(array2)
    x = dimensions[0]
    y = dimensions[1]
    array2.shape = (1,x*y)
    sequence = array2[0]
    im = Image.new('L',[x,y])
   # a = MLab.rand(100*100)
    z = Numeric.floor(255*sequence)
    im.putdata(z)
    return im
