#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import numpy as np
import cPickle as pk
import sys
import random as rd

#Load data
f=file('data32x64.data')
data=pk.load(f)
f.close()
totalnumber=0
for i in xrange(len(data)):
	totalnumber+=len(data[i])

#Load test dictionary
f=file('testdic.data')
testdic=pk.load(f)
f.close()

#Load test list
f=file('testlist.data')
testlist=pk.load(f)
f.close()

#Load bucketdic
f=file('bucketdic.data')
bucketdic=pk.load(f)
f.close()

#Load bucketcontaindic
f=file('bucketcontaindic.data')
bucketcontaindic=pk.load(f)
f.close()

#batch size
batch_size=100

def weight_variable(shape):
	initial=tf.truncated_normal(shape,stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial=tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x,w):
	return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')

def max_pool_4x4(x):
	return tf.nn.max_pool(x,ksize=[1,4,4,1],strides=[1,4,4,1], padding='SAME')

def get_testset():
	global data
	global testlist
	imagea=[]
	imageb=[]
	label=[]
	for i in xrange(len(testlist[0])):
		person1=testlist[0][i][0][0]
		no1=testlist[0][i][0][1]
		person2=testlist[0][i][1][0]
		no2=testlist[0][i][1][1]
		testlabel=testlist[1][i]
		imagea.append(data[person1][no1])
		imageb.append(data[person2][no2])
		label.append(testlabel)
	return [imagea,imageb,label]

def next_batch(n):
	global data
	global testdic
	global bucketcontaindic
	global bucketdic
	global totalnumber
	half=n/2
	sample=[]
	totalnumber=len(data)

	#positive
	counter=0
	while counter<half:
		pick=rd.randint(0, totalnumber-1)
		if bucketcontaindic[bucketdic[pick]]==1:
			continue
		tmp=rd.sample(xrange(bucketcontaindic[bucketdic[pick]]),2)
		if tmp[0]>tmp[1]:
			tmp[0],tmp[1]=tmp[1],tmp[0]
		element=((bucketdic[pick],tmp[0]),(bucketdic[pick],tmp[1]))
		if element in testdic:
			continue
		sample.append([data[bucketdic[pick]][tmp[0]],data[bucketdic[pick]][tmp[1]],[1.0,0.0]])
		counter+=1
	
	#negative
	counter=0
	while counter<half:
		pick1=rd.randint(0,totalnumber-1)
		pick2=rd.randint(0,totalnumber-1)
		if bucketdic[pick1]==bucketdic[pick2]:
			continue
		if pick1>pick2:
			pick1, pick2 = pick2, pick1
		tmp1=rd.randint(0,bucketcontaindic[bucketdic[pick1]]-1)
		tmp2=rd.randint(0,bucketcontaindic[bucketdic[pick2]]-1)
		element=((bucketdic[pick1],tmp1),(bucketdic[pick2],tmp2))
		if element in testdic:
			continue
		sample.append([data[bucketdic[pick1]][tmp1],data[bucketdic[pick2]][tmp2],[0.0,1.0]])
		counter+=1
		
	rd.shuffle(sample)
	imagea=[]
	imageb=[]
	label=[]
	for i in xrange(len(sample)):
		imagea.append(sample[i][0])
		imageb.append(sample[i][1])
		label.append(sample[i][2])
	return [imagea,imageb,label]

#Initialization
x_a=tf.placeholder(tf.float32,[None,32,64])
x_b=tf.placeholder(tf.float32,[None,32,64])
y_=tf.placeholder(tf.float32,[None,2])
x_image_a=tf.reshape(x_a,[-1,32,64,1])
x_image_b=tf.reshape(x_b,[-1,32,64,1])
w_conv1=weight_variable([5,5,1,32])
b_conv1=bias_variable([32])
#w_conv2=weight_variable([5,5,32,64])
#b_conv2=bias_variable([64])
#w_fc1=weight_variable([8*8*64, 512])
w_fc1=weight_variable([2*8*16*32, 1024])
b_fc1=bias_variable([1024])
w_fc2=weight_variable([1024,2])
b_fc2=bias_variable([2])

keep_prob=tf.placeholder(tf.float32)
#Initialization done

#model logic
h_conv1_a=tf.nn.relu(conv2d(x_image_a, w_conv1)+b_conv1)
h_pool1_a=max_pool_4x4(h_conv1_a)
#h_conv2_a=tf.nn.relu(conv2d(h_pool1_a,w_conv2)+b_conv2)
#h_pool2_a=max_pool_2x2(h_conv2_a)
#h_pool2_flat_a=tf.reshape(h_pool2_a,[-1,8*8*64])
h_pool1_flat_a=tf.reshape(h_pool1_a,[-1,8*16*32])


h_conv1_b=tf.nn.relu(conv2d(x_image_b, w_conv1)+b_conv1)
h_pool1_b=max_pool_4x4(h_conv1_b)
#h_conv2_b=tf.nn.relu(conv2d(h_pool1_b,w_conv2)+b_conv2)
#h_pool2_b=max_pool_2x2(h_conv2_b)
#h_pool2_flat_b=tf.reshape(h_pool2_b,[-1,8*8*64])
h_pool1_flat_b=tf.reshape(h_pool1_b,[-1,8*16*32])

h_fc1_concat=tf.concat(1, [h_pool1_flat_a, h_pool1_flat_b])
h_fc1=tf.nn.relu(tf.matmul(h_fc1_concat,w_fc1)+b_fc1)
h_fc1_drop=tf.nn.dropout(h_fc1,keep_prob)

y_conv=tf.matmul(h_fc1_drop, w_fc2) +b_fc2
#model logic done

#train logic
cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
train_step=tf.train.AdamOptimizer(0.0001).minimize(cross_entropy)
#train logic done

#test logic
correct_prediction=tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#test logic done

#start session
sess=tf.Session()

#init variables
init=tf.initialize_all_variables()
sess.run(init)

testset=get_testset()

#print 'len:',len(next_batch(100))
#print 'testest len:', len(testset)
outfile=open('record.txt','w')

for i in xrange(1,100001):
	print 'start',i
	batch=next_batch(batch_size)
	sess.run(train_step,feed_dict={x_a: np.array(batch[0]), x_b:np.array(batch[1]), y_: np.array(batch[2]), keep_prob: 0.5})
	if i%200==0:
		#sess.run(train_step,feed_dict={x_a: np.array(testset[0]), x_b:np.array(testset[1]), y_:np.array(testset[2]), keep_prob: 1.0})
		result=sess.run(accuracy,feed_dict={x_a: np.array(testset[0]), x_b:np.array(testset[1]), y_:np.array(testset[2]), keep_prob: 1.0})
		print i, result
		outfile.write('%d:%f\n'%(i,result))
outfile.close()
