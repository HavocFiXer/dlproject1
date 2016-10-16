from PIL import Image
import os
import numpy as np
import cPickle as pk
import random as rd

imagepath='./../images/'
#imagepath='./'
imagesfolder=os.listdir(imagepath)

rzwidth=64
rzheight=32

writerdic={}
datalist=[]
writercounter=0
filecounter=0

for name in imagesfolder:
	if name[-4:]=='.png' or name[-4:]=='PNG':
		im=Image.open(imagepath+name)
		width=im.size[0]
		height=im.size[1]
		im=im.resize((rzwidth,rzheight), Image.BILINEAR);
		pix=im.load()

		imagearray=np.array([[0.0]*rzwidth]*rzheight)
		for i in xrange(rzheight):
			for j in xrange(rzwidth):
				if pix[j,i]<180:
					imagearray[i][j]=1.0

		writer=name.strip().split('_')[0]
		tmppo=0
		for tmppo in xrange(len(writer)):
			if not writer[tmppo].isdigit():
				break
		writer=writer[:tmppo]
		if writer not in writerdic:
			writerdic[writer]=writercounter
			writercounter+=1
			datalist.append([imagearray])
		else:
			datalist[writerdic[writer]].append(imagearray)
		filecounter+=1
		if filecounter%1000==0:
			print filecounter

#generate all data in format of numpy matrix
f=file('data32x64.data','w')
pk.dump(datalist,f)
f.close()


totalnumber=0
people=0
acc=0
bucketdic={}
bucketcontaindic={}
for i in xrange(len(datalist)):
	number=len(datalist[i])
	acc+=number
	bucketcontaindic[i]=len(datalist[i])
	while people<acc:
		bucketdic[people]=i
		people+=1
#save bucketfile
f=file('bucketdic.data','w')
pk.dump(bucketdic,f)
f.close();
f=file('bucketcontaindic.data','w')
pk.dump(bucketcontaindic,f)
f.close()


#generate test data
TestPairs={}
totalnumber=filecounter
#positive
counter=0
while counter<5000:
	pick=rd.randint(0,totalnumber-1)
	if bucketcontaindic[bucketdic[pick]]==1:
		continue
	#print[i for i in range(bucketcontaindic[bucketdic[pick]])]
	tmp=rd.sample(xrange(bucketcontaindic[bucketdic[pick]]),2)
	if tmp[0]>tmp[1]:
		tmp[0],tmp[1]=tmp[1],tmp[0]
	element=((bucketdic[pick],tmp[0]),(bucketdic[pick],tmp[1]))
	if element not in TestPairs:
		TestPairs[element]=[1.0, 0.0]
		counter+=1

#negative
counter=0
while counter<5000:
	pick1=rd.randint(0,totalnumber-1)
	pick2=rd.randint(0,totalnumber-1)
	if bucketdic[pick1]==bucketdic[pick2]:
		continue
	if pick1>pick2:
		pick1, pick2 = pick2, pick1
	tmp1=rd.randint(0,bucketcontaindic[bucketdic[pick1]]-1)
	tmp2=rd.randint(0,bucketcontaindic[bucketdic[pick2]]-1)
	element=((bucketdic[pick1],tmp1),(bucketdic[pick2],tmp2))
	if element not in TestPairs:
		TestPairs[element]=[0.0, 1.0]
		counter+=1


f=file('testdic.data','w')
pk.dump(TestPairs,f)
f.close()

f=file('testlist.data','w')
testpairlist=[[],[]]
for a,b in TestPairs.items():
	testpairlist[0].append(a)
	testpairlist[1].append(b)
pk.dump(testpairlist,f)
f.close()
