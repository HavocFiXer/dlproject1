import Image
import os
import numpy as np
import cPickle as pk

#imagepath='./images/'
imagepath='./'
imagesfolder=os.listdir('./images/')

maxwidth=400
maxheight=200

logfile=open('generateDataMetrix.log','w')

writerdic={}
datalist=[]
writercounter=0

for name in imagesfolder:
	if name[-4:]=='.png' or name[-4:]=='PNG':
		im=Image.open(imagepath+name)
		width=im.size[0]
		height=im.size[1]
		pix=im.load()
		if width > maxwidth or height > maxheight:
			logfile.write('Skip image [%s] with width [%d] and height [%d]\n'%(name, width,height))
			continue

		imagearray=np.array([[0.0]*maxwidth]*maxheight)
		for i in xrange(height):
			for j in xrange(width):
				if pix[j,i] != 255 or pix[j,i]!=6:
					logfile.write('Image %s has pixel p[%d,%d]=%d'%(name,j,i,pix[j,i]))
					imagearray[(maxwidth-width)/2+j,(maxheight-height)/2+i]=pix[j,i]/255

		writer=name.strip().split('_')[0][:-1]
		if not writer.isdigit:
			print 'Not digit: %s'%(name)
		if writer not in writerdic:
			writerdic[writer]=counter
			counter+=1
			datalist.append([imagearray])
		else:
			datalist[writerdic[writer]].append(imagearray)

f=file('train.data','w')
pk.dump(datalist,f)
f.close()

logfile.close()
