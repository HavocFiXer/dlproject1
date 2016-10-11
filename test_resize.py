import PIL
from PIL import Image
#import Image

im=Image.open('sample.png')
newim=im.resize((57,35),Image.BILINEAR)
newim.save('nsample.png','png')

nsize=newim.size
for i in xrange(nsize[0]):
	for j in xrange(nsize[1]):
		print newim.load()[i,j]

print '-----------------'

size=im.size
for i in xrange(size[0]):
	for j in xrange(size[1]):
		print im.load()[i,j]
