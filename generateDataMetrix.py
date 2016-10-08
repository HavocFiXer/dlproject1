import Image
import os

imagepath='./images/'
#imagepath='./'
imagesfolder=os.listdir('./images/')

maxwidth=400
maxheight=200

logfile=open('generateDataMetrix.log','w')

writerdic={}

for name in imagesfolder:
	if name[-4:]=='.png' or name[-4:]=='PNG':
		im=Image.open(imagepath+name)
		width=im.size[0]
		height=im.size[1]
		if width > maxwidth or height > maxheight:
			logfile.write('Skip image [%s] with width [%d] and height [%d]\n'%(name, width,height))
			continue
		writer=name.strip().split('_')[0][:-1]
		if not writer.isdigit:
			print 'Not digit: %s'%(name)
		#if writer in writerdic:
			#data[writerdic[writer]].append()


logfile.close()
