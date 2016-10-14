#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import numpy as np
import cPickle as pk
import sys

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

def max_pool_5x5(x):
	return tf.nn.max_pool(x,ksize=[1,5,5,1],strides=[1,5,5,1],padding='SAME')

#Load data
f=file('train.data')
data=pk.load(f)
f.close()

#Load test dictionary
f=file('test.data')
testdic=pk.load(f)
f.close()

#Read system parameters
batch_size=int(sys.argv[1])

#Initialization and logic
x_image=tf.reshape(x,[-1,50,100,1])

w_conv1=weight_variable([5,5,1,32])
b_conv1=bias_variable([32])
h_conv1=tf.nn.relu(conv2d(x_image, w_conv1)+b_conv1)
h_pool1=max_pool_5x5(h_conv1)

w_conv2=weight_variable([5,5,32,64])
b_conv2=bias_variable([64])
h_conv2=tf.nn.relu(conv2d(h_pool1,w_conv2)+b_conv2)
h_pool2=max_pool_2x2(h_conv2)

w_fc1=weight_variable([10*5*64, 1024])
b_fc1=bias_variable([1024])
h_pool2_flat=tf.reshape(h_pool2,[-1,10*5*64])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1)+b_fc1)

keep_prob=tf.placeholder(tf.float32)
h_fc1_drop=tf.nn.dropout(h_fc1, keep_prob)

w_fc2=weight_variable([1024,2])
b_fc=bias_variable([10])

y_conv=tf.matmul(h_fc1_drop, w_fc2) +b_fc2


