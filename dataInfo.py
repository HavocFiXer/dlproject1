import cPickle as pk
import numpy as np

f=file('train.data')
data=pk.load(f)
f.close()

outfile=open('dataInfo.txt','w')
outfile.write('writer number: %d\n'%(len(data)))
totalnumber=0
totalppairnumber=0
acc=0
bucketdic={}
bucketcontaindic={}
people=0
for i in xrange(len(data)):
	number=len(data[i])
	acc+=number
	ppairnumber=number*(number-1)/2
	outfile.write('\t%d:%d->%d\n'%(i,len(data[i]),ppairnumber))
	bucketcontaindic[i]=len(data[i])
	totalnumber+=number
	totalppairnumber+=ppairnumber
	while people<acc:
		bucketdic[people]=i
		people+=1
outfile.write('total number: %d\n'%(totalnumber))
outfile.write('total positive pair number: %d\n'%(totalppairnumber))
totalnpairnumber=0
for i in xrange(len(data)):
	totalnpairnumber+=len(data[i])*(totalnumber-1)/2
outfile.write('total negative pair number: %d\n'%(totalnpairnumber))
outfile.close()

#print bucketdic
f=file('bucket.data','w')
pk.dump(bucketdic,f)
pk.dump(bucketcontaindic,f)
f.close()
