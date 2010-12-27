import Image
import PSDraw

im = Image.open('image.ppm')

title = 'Test'
box = (0,0,800,600)

file = open('/home/matthew/work/pythonwork/tmp.ps','w+')
ps = PSDraw.PSDraw(file)
ps.begin_document(title)

# draw image
#ps.image((1*72,2*72,7*72,10*72),im,75)
ps.rectangle(box)

#ps.setfont("HelveticNarrow-Bold",36)
#ps.text((100,100),title)

ps.end_document
