import Image
import os

imagepath='./images/'
testpath=imagepath+'test/'
imagesfolder=os.listdir('./images/')
testfolder=os.listdir('./images/test/')

widthdic={}
heightdic={}
maxwidth=0
maxheight=0

outfile=open('info.txt','w')

for name in imagesfolder:
	if name[-4:]=='.png' or name[-4:]=='.PNG':
		im=Image.open(imagepath+name)
		size=im.size
		if size[0] == 34:
			os.system('cp %s ./'%(imagepath+name))
			for i in xrange(size[0]):
				for j in xrange(size[1]):
					print im.load()[i,j]
		if size[1] not in heightdic:
			heightdic[size[1]]=1
			if size[1]>maxheight:
				maxheight=size[1]
		else:
			heightdic[size[1]]+=1
		if size[0] not in widthdic:
			widthdic[size[0]]=1
			if size[0]>maxwidth:
				maxwidth=size[0]
		else:
			widthdic[size[0]]+=1

for name in testfolder:
	if name[-4:]=='.png' or name[-4:]=='.PNG':
		im=Image.open(testpath+name)
		size=im.size
		if size[1] not in heightdic:
			heightdic[size[1]]=1
			if size[1]>maxheight:
				maxheight=size[1]
		else:
			heightdic[size[1]]+=1
		if size[0] not in widthdic:
			widthdic[size[0]]=1
			if size[0]>maxwidth:
				maxwidth=size[0]
		else:
			widthdic[size[0]]+=1

outfile.write('maxwidth: %d\n'%maxwidth)
outfile.write('maxheight: %d\n'%maxheight)
outfile.write('\nwidth dic:\n')
widthlist=sorted(widthdic,key=lambda key:key)
widthstr=''
for item in widthlist:
	widthstr+='%d:%d,'%(item,widthdic[item])
outfile.write('%s\n'%widthstr[:-1])
outfile.write('\nheight dic:\n')
heightlist=sorted(heightdic,key=lambda key:key)
heightstr=''
for item in heightlist:
	heightstr+='%d:%d,'%(item,heightdic[item])
outfile.write('%s\n'%heightstr[:-1])
