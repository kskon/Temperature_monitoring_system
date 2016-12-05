#! /usr/local/Cellar/python/2.7.12
# -*- coding: utf-8 -*-

import serial 
import zmq
import time


ser = serial.Serial('/dev/cu.usbmodem1411', 9600, dsrdtr = 1, timeout=1)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:8968")
i = 0
while True:
	temp = ser.readline()
	if i >= 5:
		socket.send("TEMP " + str(temp))
	i+=1




#ser.write("N")
#ser.close()
	



    


