import numpy as np  
import cv2
import sys, os
import argparse

def save_pic2npy(image_dir):
	if not os.path.exists(image_dir) :
		print "error, can not find directer: "+image_dir
		exit(0)
		# print "error path: "+sys.argv[1]
		# exit(0)
	image = np.zeros((1,),np.uint8)
	for file in os.listdir(image_dir):
		if file.endswith(".jpg"):
			file_path = os.path.join(image_dir, file)
			print file_path
			img = cv2.imread(file_path)
			img = img[np.newaxis,:]
			if len(image.shape) == 1:
				image = img
			else:
				image = np.vstack((image,img))
	np.save("pic", image)

def load_npy2pic(image_dir):
	if os.path.exists(image_dir) :
		if not image_dir.endswith(".npy"):
			print "Please input file path end with \".npy\""
			exit(0)
	else :
		print "error, can not find file: "+image_dir
		exit(0)
	image = np.load(image_dir)
	for i in range(image.shape[0]):
		window_name = "image["+str(i)+"]"
		cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)#cv2.WINDOW_AUTOSIZE)
		cv2.imshow(window_name,image[i])
		cv2.waitKey()
		cv2.destroyAllWindows()
	pass

def main():
	parser = argparse.ArgumentParser(description='manual to this script')
	parser.add_argument('-pic', type=str, default = None)
	parser.add_argument('-data', type=str, default = None)
	args = parser.parse_args()
	if args.pic != None:
		save_pic2npy(args.pic)
	if args.data != None:
		load_npy2pic(args.data)
	print sys.argv
	print "args.pic = "+str(args.pic)
	print "args.data = "+str(args.data)
	pass

if __name__ == "__main__":
	main()
	# for root, dirs, files in os.walk("./"):  
	# 	print(root)
	# 	print(dirs)
	# 	print(files)
	# print os.listdir("./")
