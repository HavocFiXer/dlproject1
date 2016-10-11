import cPickle as pk
import numpy as np
from PIL import Image

f=file('train.data')
data=pk.load(f)
f.close()

print 'data number:',len(data)
print 'first data number:',len(data[1328])
print 'second data number:',len(data[82])

im=Image.new('L',(100,50),0)
pix=im.load()
for i in xrange(50):
	for j in xrange(100):
		if data[1328][0][i][j]>0.5:
			pix[j,i]=0
		else:
			pix[j,i]=255
im.save('verify.png','png')
