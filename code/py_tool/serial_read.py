import serial
import os
import serial.tools.list_ports
import sys

import cv2
import cv2.cv as cv
import numpy as np

# help(cv.Resize)
# os._exit(0)

file_path_base = "aec_illumination"
file_format = '.txt'#'.xls'
port_list = list(serial.tools.list_ports.comports())
if not len(port_list) :
	print repr('No serial port')
	os._exit(0)
print repr('Please choose the port :')
count = 0
for ports in port_list :
	port_name = list(ports)
	count += 1
	print repr(str(count)+'. '+port_name[0])
port_name = raw_input()
if port_name == '' :
	port_name = '/dev/ttyACM0'

try:
	ser = serial.Serial(port_name, 115200, timeout=65)
except :
	print repr('no port named : '+port_name)
	os._exit(0)

# if not os.path.isfile(file_path_base+file_format) :
# 	fileRead = open(file_path_base+file_format, 'w')
# else :
# 	for num in range(100) :
# 		if not os.path.isfile(file_path_base+str(num+1)+file_format) :
# 			fileRead = open(file_path_base+str(num+1)+file_format, 'w')
# 			break

# while True :
# 	try :
# 		data = ser.read(1)
# 	except :
# 		print repr('can\'t open serial port :'+port_name)
# 		os._exit(0)
# 	else :
# 		fileRead.write(data)
# 		sys.stdout.write(data)

image_buf = []
pix = 1
muti_num = 10
cv2.namedWindow("image_big", flags=0)
# cv2.namedWindow("image", flags=0)
imag = cv.CreateMat(1, 1, cv.CV_8UC3)
imag_big = cv.CreateMat(1, 1, cv.CV_8UC3)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
while True :
	data = ser.readline().rstrip('\r\n')
	# if data.startswith('RECT') :
	# 	detected_rect_ls = data.split()
	# 	start_x = int(detected_rect_ls[1])
	# 	start_y = int(detected_rect_ls[2])
	# 	width = int(detected_rect_ls[3])
	# 	height = int(detected_rect_ls[4])
	# 	name_score = detected_rect_ls[5]
	# 	if not name_score.startswith('colorobject') :
	# 		cv.Rectangle(imag, (start_x, start_y), (start_x+width, start_y+height), (0,0,255), 1, 8)
	# 		cv.PutText(imag, name_score, (start_x+width-1, start_y+height-1), font, (0,0,255))
	if data == 'FRAME' :
		frame_count = int(ser.readline().rstrip('\r\n'))
		cols = int(ser.readline().rstrip('\r\n'))
		rows = int(ser.readline().rstrip('\r\n'))
		channal = int(ser.readline().rstrip('\r\n'))
		print repr('frame_count : ' + str(frame_count))
		r = []
		g = []
		b = []
		# print cols
		# print rows
		# print channal
		# print rows*cols
		# while pix != '\n' :
		for i in range(3) :
			for j in range(rows*cols) :
				pix = ord(ser.read(1))
				if i == 0 :
					r.append(pix)
				elif i == 1 :
					g.append(pix)
				elif i == 2 :
					b.append(pix)
		# print np.asarray(imag)
		count = 0
		imag = cv.CreateMat(rows, cols, cv.CV_8UC3)
		imag_big = cv.CreateMat(rows*muti_num, cols*muti_num, cv.CV_8UC3)
		for i in range(rows) :
			for j in range(cols) :
				imag[i,j] = [b[count], g[count], r[count]]
				count+=1
		cv.Resize(imag, imag_big, cv2.INTER_CUBIC)
		# cv2.destroyAllWindows()
		# cv2.imshow("image", imag)
		# cv.ShowImage("image", imag)
	elif data.startswith('RECT') :
		detected_rect_ls = data.split()
		start_x = int(detected_rect_ls[1])
		start_y = int(detected_rect_ls[2])
		width = int(detected_rect_ls[3])
		height = int(detected_rect_ls[4])
		name_score = detected_rect_ls[5]
		if not name_score.startswith('colorobject') :
			cv.Rectangle(imag_big, (start_x*muti_num, start_y*muti_num), ((start_x+width)*muti_num, (start_y+height)*muti_num), (0,0,255), 1, 1)
			cv.PutText(imag_big, name_score, ((start_x)*muti_num, (start_y+height-1)*muti_num), font, (0,0,255))

	cv.ShowImage("image_big", imag_big)
	# cv.ShowImage("image", imag)
	# del r[:]
	# del g[:]
	# del b[:]
	key = cv.WaitKey(1)
	if key == 27 :	#'ESC'
		# print key 
		cv2.destroyAllWindows()
		os._exit(0)
	elif key == ord('s') :
		cv.SaveImage("pic_"+str(frame_count)+".jpg", imag)