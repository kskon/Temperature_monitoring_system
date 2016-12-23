import serial
import hashlib
import os
import sys
import random
import time
import unittest

import zmq
from multiprocessing import Process, Queue

from settings import LOGGER as logger
from settings import ZEROMQ_SERVER_HOST, ZEROMQ_SERVER_PORT
serial = serial.Serial('/dev/cu.usbmodem1411', 9600, dsrdtr = 1, timeout=1)

class ZMQPublisher(object):
    def __init__(self,
                 ip_port='tcp://{}:{}'.format(ZEROMQ_SERVER_HOST, ZEROMQ_SERVER_PORT),
                 receivers=['gui', 'all']):
        # logger.debug("ZMQPublisher: ip_port={}".format(ip_port))
        self.receivers = receivers
        self.ip_port = ip_port
        self.last_message = None
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.ip_port)

    def send(self, msg, receiver='all'):
        if receiver in self.receivers:
            message = '{}: {}'.format(receiver, msg)
            self.last_message = message
            logger.debug("ZMQPublisher: message={}".format(message))
            self.socket.send_string(message)
        else:
            raise ValueError, 'receiver is not correct'


def init_publisher():
    publisher = ZMQPublisher()
    i=0
    while True:
        try:
            # Let's do something here.... read from com port or ...etc...
            temp = serial.readline()
            if i >=5:
                publisher.send("TEMP " + str(temp))
            else:
                i+=1
            barcode = hashlib.sha256(os.urandom(30).encode('base64')[:-1]).hexdigest()[:10]
            #publisher.send(barcode, random.choice(['gui', 'all']))3
            time.sleep(0.1)
        except KeyboardInterrupt:
            logger.debug('init_publisher while loop is stopping')
            break


class TestZMQPublisher(unittest.TestCase):

    def test_stupid(self):
        publisher = ZMQPublisher()
        receivers = ['gui', 'all']
        for i in xrange(10):
            barcode = hashlib.sha256(os.urandom(30).encode('base64')[:-1]).hexdigest()[:10]
            try:
                publisher.send(barcode, random.choice(receivers))
                time.sleep(1)
            except Exception as e:
                logger.debug(e)
                self.assertTrue(False, 'something wrong')

if __name__ == '__main__':
    #unittest.main(verbosity=7)
    try:
        publisher_process = Process(target=init_publisher)
        publisher_process.start()
        logger.debug('publisher_process start')
        publisher_process.join()
    except KeyboardInterrupt:
        logger.debug('publisher_process terminating')
        publisher_process.terminate()
        sys.exit()
