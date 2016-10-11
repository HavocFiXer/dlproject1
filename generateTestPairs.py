import cPickle as pk
import numpy as np
import random as rd

#5000 positive & 5000 negative
totalnumber=15500#in file: dataInfo.txt

TestPairs={}
f=file('bucket.data')
bucketdic=pk.load(f)
bucketcontaindic=pk.load(f)
f.close()

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
		TestPairs[element]=1.0
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
		TestPairs[element]=0.0
		counter+=1
print TestPairs

f=file('test.data','w')
pk.dump(TestPairs,f)
f.close()
