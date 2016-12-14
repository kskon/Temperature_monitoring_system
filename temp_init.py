import serial 
import sys
import zmq
from pylib.subscriber import ZMQSubscriber
from pylib.publisher import ZMQPublisher
from multiprocessing import Process

serial = serial.Serial('/dev/cu.usbmodem1411', 9600, dsrdtr = 1, timeout=1)

def init_temp():
	publisher = ZMQPublisher()
	subscriber = ZMQSubscriber()
	i=0
	while True:
    	   temp = serial.readline()
    	   if i >=5:
    	   	publisher.send("TEMP " + str(temp))
    	   else:
    	   	i+=1













if __name__ == '__main__':
	try:
		publisher_process = Process(target=init_temp)
		publisher_process.start()
	except (KeyboardInterrupt, SystemExit):
		publisher_process.terminate()
		sys.exit()