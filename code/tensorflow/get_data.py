# -*- coding:utf-8 -*-  

import sys, os
import numpy as np
import cv2

def isPathExist(filePath):
	if os.path.exists(filePath) :
		if not filePath.endswith(".npy"):
			raise ValueError('Please input file path end with ".npy"')
	else :
		raise ValueError('error, can not find file: '+filePath)
	return True

class GetMaleFemaleData(object):
	"""docstring for GetMaleFemaleData"""
	def __init__(self, male_dir, female_dir):
		super(GetMaleFemaleData, self).__init__()
		isPathExist(male_dir)
		isPathExist(female_dir)
		male_data = np.load(male_dir)
		female_data = np.load(female_dir)
		test_data_len = 50

		male_test_data = male_data[-test_data_len-1:-1]
		male_test_lable = np.zeros(male_test_data.shape[0])
		male_train_data = male_data[0:-test_data_len-1]
		male_train_lable = np.zeros(male_train_data.shape[0])
		print 'male_test_data.shape = '+str(male_test_data.shape)
		print 'male_test_lable.shape = '+str(male_test_lable.shape)
		print 'male_test_lable = '+str(male_test_lable)
		print 'male_train_data.shape = '+str(male_train_data.shape)
		print 'male_train_lable.shape = '+str(male_train_lable.shape)
		print 'male_train_lable = '+str(male_train_lable)

		female_test_data = female_data[-test_data_len-1:-1]
		female_test_lable = np.ones(female_test_data.shape[0])
		female_train_data = female_data[0:-test_data_len-1]
		female_train_lable = np.ones(female_train_data.shape[0])
		print '\nfemale_test_data.shape = '+str(female_test_data.shape)
		print 'female_test_lable.shape = '+str(female_test_lable.shape)
		print 'female_test_lable = '+str(female_test_lable)
		print 'female_train_data.shape = '+str(female_train_data.shape)
		print 'female_train_lable.shape = '+str(female_train_lable.shape)
		print 'female_train_lable = '+str(female_train_lable)


		self.train_data = np.vstack((male_train_data,female_train_data))
		self.train_lable = np.hstack((male_train_lable,female_train_lable))
		self.test_data = np.vstack((male_test_data,female_test_data))
		self.test_lable = np.hstack((male_test_lable,female_test_lable))
		print 'self.train_data.shape = '+str(self.train_data.shape)
		print 'self.train_lable.shape = '+str(self.train_lable.shape)
		print 'self.test_data.shape = '+str(self.test_data.shape)
		print 'self.test_lable.shape = '+str(self.test_lable.shape)
		self.train_data_index = 0

	def next_train_batch(self, batch_size):
		if self.train_data_index+batch_size >= self.train_data.shape[0]:
			self.train_data_index = 0
		if self.train_data_index == 0:
			perm = np.arange(self.train_data.shape[0])
			np.random.shuffle(perm)
			self.train_data = self.train_data[perm]
			self.train_lable = self.train_lable[perm]
		self.train_data_index = self.train_data_index+batch_size
		return self.train_data[self.train_data_index-batch_size:self.train_data_index], self.train_lable[self.train_data_index-batch_size:self.train_data_index]

	def get_test_data(self):
		return self.test_data, self.test_lable
		pass
		
def main():
	male_dir = sys.argv[1]#'/home/ysq/YSQWork/DeepLearning/data/FemaleMaleFace_30x30/1_Male.npy'
	female_dir = sys.argv[2]#'/home/ysq/YSQWork/DeepLearning/data/FemaleMaleFace_30x30/0_Female.npy'
	data_get = GetMaleFemaleData(male_dir, female_dir)
	# train_data, train_lable = data_get.next_train_batch(50)
	train_data, train_lable = data_get.get_test_data()
	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	for i in range(train_data.shape[0]):
		cv2.imshow('image', train_data[i])
		print train_lable[i]
		cv2.waitKey(0)
	pass

if __name__ == '__main__':
	main()
