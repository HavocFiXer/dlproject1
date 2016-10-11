from PIL import Image
import os
import numpy as np
import cPickle as pk

imagepath='./images/'
#imagepath='./'
imagesfolder=os.listdir(imagepath)

maxwidth=100
maxheight=50

logfile=open('generateDataMetrix.log','w')

writerdic={}
datalist=[]
writercounter=0

pixdic={}
filecounter=0

for name in imagesfolder:
	if name[-4:]=='.png' or name[-4:]=='PNG':
		im=Image.open(imagepath+name)
		width=im.size[0]
		height=im.size[1]
		while width > maxwidth or height >maxheight:
			im=im.resize((width/2,height/2),Image.BILINEAR)
			width=im.size[0]
			height=im.size[1]
		pix=im.load()
		#if width > maxwidth or height > maxheight:
			#logfile.write('Skip image [%s] with width [%d] and height [%d]\n'%(name, width,height))
			#continue

		#print 'name',name
		#print 'heigh',height
		#print 'width',width
		imagearray=np.array([[0.0]*maxwidth]*maxheight)
		#print imagearray
		for i in xrange(height):
			for j in xrange(width):
				if pix[j,i] not in pixdic:
					pixdic[pix[j,i]]=1
				else:
					pixdic[pix[j,i]]+=1
				#if pix[j,i] != 255 and pix[j,i]!=6:
					#logfile.write('Image %s has pixel p[%d,%d]=%d\n'%(name,j,i,pix[j,i]))
				if pix[j,i]<180:
					#print j,i,(maxwidth-width)/2+j,(maxheight-height)/2+i
					imagearray[(maxheight-height)/2+i][(maxwidth-width)/2+j]=1.0

		writer=name.strip().split('_')[0]#[:-1]
		tmppo=0
		for tmppo in xrange(len(writer)):
			if not writer[tmppo].isdigit():
				break
		writer=writer[:tmppo]
		#if writer=='071':
			#print name
		#if not writer.isdigit():
			#print 'Not digit: %s'%(name)
		if writer not in writerdic:
			writerdic[writer]=writercounter
			writercounter+=1
			datalist.append([imagearray])
		else:
			datalist[writerdic[writer]].append(imagearray)
		filecounter+=1
		if filecounter%1000==0:
			print filecounter

logfile.write('writerdic:\n')
writerlist=sorted(writerdic,key=lambda key:key)
print writerlist
for item in writerlist:
	logfile.write('%s:%d\n'%(item,writerdic[item]))



f=file('train.data','w')
pk.dump(datalist,f)
f.close()

logfile.write('pixdic:\n')
pixlist=sorted(pixdic,key=lambda key:key)
for item in pixlist:
	logfile.write('%d:%d\n'%(item,pixdic[item]))

logfile.close()

