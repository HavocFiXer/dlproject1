import cPickle as pk
import numpy as np

f=file('train.data')
data=pk.load(f)
f.close()

outfile=open('dataInfo.txt')
outfile.write('writer number: %d\n'%(len(data)))
totalnumber=0
for i in xrange(len(data)):
	outfile.write('\t%d:%d\n'%(i,len(data[i])))
	totalnumber+=len(data[i])
outfile.write('total number: %d\n'%(totalnumber))

outfile.close()
