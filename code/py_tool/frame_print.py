import serial
import os
import serial.tools.list_ports
import sys
import time

import cv2
import cv2.cv as cv
import numpy as np

# help(cv.Rectangle)
# os._exit(0)

def Serial_Port_Init():
	serial_baud_rate = 921600 #115200 230400 460800 921600
	port_list = list(serial.tools.list_ports.comports())
	ser = serial.Serial()
	if not len(port_list) :
		print repr('No serial port')
		os._exit(0)

	print 'Serial Port Information:'
	for ports in port_list:
		print list(ports)

	print '\n'+'Please choose the port :'
	count = 0
	for ports in port_list :
		port_name = list(ports)
		count+=1
		print str(count)+'. '+port_name[0]
	port_name = raw_input()
	if port_name == '' :
		for i in range(len(port_list)):
			try :
				port = list(port_list[i])
				print "try to open "+port[0]
				ser = serial.Serial(port[0], serial_baud_rate, timeout=100)
			except :
				continue
		if not ser.isOpen():
			print "Cann't open any port!"
			exit()
		else :
			print "Open port: "+ser.port+" success!"
	else :
		port = list(port_list[int(port_name)-1])
		try:
			ser = serial.Serial(port[0], serial_baud_rate, timeout=100)
			print "Open port: "+ser.port+" success!"
		except:
		# except serial.portNotOpenError, e:
		# 	print e
			print "Cant't open "+port_name[0]+"!"
			exit()
	return ser, port

def Save_Image(img):
	key = cv.WaitKey(1)
	if key :
		# u8_key = chr(key)
		if key == 27 or key == 131099:	#27 = lower'ESC', 131099 = upper'ESC'
			cv2.destroyAllWindows()
			os._exit(0)
		elif key == ord('s') or key == 131155 : #131155 == 'S'
			cv.SaveImage("pic_"+str(frame_count)+".jpg", img)
		# else :
		# 	print repr('key num = '+str(key))

file_path_base = "aec_illumination"
file_format = '.txt'#'.xls'
ser, port = Serial_Port_Init()	#port[0]: serial address
								#prot[1]: device name

# if not os.path.isfile(file_path_base+file_format) :
# 	fileRead = open(file_path_base+file_format, 'w')
# else :
# 	for num in range(100) :
# 		if not os.path.isfile(file_path_base+str(num+1)+file_format) :
# 			fileRead = open(file_path_base+str(num+1)+file_format, 'w')
# 			break

pix = 1
muti_num = int(10)
cv2.namedWindow("image_big", flags=0)
# cv2.namedWindow("image", flags=0)
imag = cv.CreateMat(1, 1, cv.CV_8UC3)
imag_big = cv.CreateMat(1, 1, cv.CV_8UC3)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
time_last = time.time()
while True :
	data = ser.readline().rstrip('\r\n')
	if data.endswith('FRAME ') :
		frame_count = int(ser.readline().rstrip('\r\n'))
		cols = int(ser.readline().rstrip('\r\n'))
		rows = int(ser.readline().rstrip('\r\n'))
		channal = int(ser.readline().rstrip('\r\n'))
		frame_date_count = cols*rows*channal
		frame_date = ser.read(frame_date_count)
		time_now = time.time()
		print 'Device name:'+ port[1] + '  frame_count:' + str(frame_count) + '  fps:' + '%.2f' %(1/(time_now-time_last))
		time_last = time_now
		r = []
		g = []
		b = []
		# print cols
		# print rows
		# print channal
		# print rows*cols
		# while pix != '\n' :
		########Frame uncompress###############
		if channal == 2 :
			pt_input = 0
			if data.endswith('YUV') :
				for i in range(rows*cols//2) :		#(uint32_t i = 0; i < height_; i += 1)
					r.append(ord(frame_date[pt_input]))			#*(gray_ + k + j) = *pt_input									#  Y0
					g.append(ord(frame_date[pt_input+1]))		#*(u_ + k + j) = *(pt_input + 1)								#  U0
					b.append(ord(frame_date[pt_input+3]))    	#*(v_ + k + j) = *(pt_input + 3)								#  V0
					r.append(ord(frame_date[pt_input+2]))    	# *(gray_ + k + j + 1) = *(pt_input + 2)						#  Y1
					if pt_input+5 < frame_date_count :
						g.append((ord(frame_date[pt_input+1])+ord(frame_date[pt_input+5]))//2)    # *(u_ + k + j + 1) = (*(pt_input + 1) + *(pt_input + 5)) >> 1	#  U0
					else :
						g.append(ord(frame_date[pt_input+1]))
					if pt_input+7 < frame_date_count :
						b.append((ord(frame_date[pt_input+3])+ord(frame_date[pt_input+7]))//2)    # *(v_ + k + j + 1) = (*(pt_input + 3) + *(pt_input + 7)) >> 1	#  V0
					else :
						b.append(ord(frame_date[pt_input+3]))
					pt_input += 4
			elif 1:#data.endswith('RGB') :
				for i in range(rows*cols) :
					pix = (ord(frame_date[i*2])) | (ord(frame_date[i*2+1])<<8)
					r.append((pix & 0xF800)>>8)
					g.append((pix & 0x07E0)>>3)
					b.append((pix & 0x001F)<<3)
		########Frame compress#################
		elif channal == 3 :
			 for i in range(3) :
				for j in range(rows*cols) :
					pix = ord(frame_date[i*rows*cols+j])
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
		cv.Resize(imag, imag_big, cv2.INTER_NEAREST)# , cv2.INTER_CUBIC)
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
		if not name_score.startswith('colorobject') and not name_score.startswith('meansift') and not name_score.startswith('detobject'):
			try :
				cv.Rectangle(imag_big, (start_x*muti_num, start_y*muti_num), ((start_x+width)*muti_num, (start_y+height)*muti_num), (0,0,255), 1, 1)
				cv.PutText(imag_big, name_score, ((start_x)*muti_num, (start_y+height-1)*muti_num), font, (0,0,255))
			except :
				print repr(data)
			# 	print repr(start_x)
			# 	print repr(start_y)
			# 	print repr(width)
			# 	print repr(height)
	elif data.startswith('DEBUG_PRINT') :
		detected_rect_ls = data.split()
		detected = detected_rect_ls[1]
		if detected == "1" :
			cv.SaveImage("pic_"+str(frame_count)+".jpg", imag)
		os.system('clear')
		for detected_rect in detected_rect_ls :
			print detected_rect
		# print repr(data.rstrip('DEBUG_PRINT '))

	cv.ShowImage("image_big", imag_big)
	# cv.ShowImage("image", imag)
	Save_Image(imag)
