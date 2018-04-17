import serial
import os
import serial.tools.list_ports
import sys
import time

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=100)	#921600

time_last = time.time()

while True :
	while ser.in_waiting:
		if ser.read() == '1':
			time_now = time.time()
			time_per_100000 = time_now-time_last
			print "time = "+str(time_per_100000)
			print "fps = "+str(1/time_per_100000)
			print "YELD time = "+str(time_per_100000*10)+"us\n"

			time_last = time_now

