#! /usr/local/Cellar/python/2.7.12
# -*- coding: utf-8 -*-

import json
import zmq
import sys
import time

from flask import Flask
from flask import render_template, redirect, url_for, request, flash, make_response

from pylib.settings import FLASK_ALLOWED_EXTENSIONS, FLASK_RESOURCE_STATUSES

from flask_login import LoginManager
from flask_restful import Api

__NAME__ = "Temperature_monitoring"
ALLOWED_EXTENSIONS = set(FLASK_ALLOWED_EXTENSIONS)
STATUSES = set(FLASK_RESOURCE_STATUSES)

# Create application
app = Flask(__NAME__)

# Create admin
login_manager = LoginManager()

data = [] # create empty list
context = zmq.Context()
socket = context.socket(zmq.SUB)
print "Connecting events from server"
socket.connect("tcp://127.0.0.1:8968")

socket.setsockopt(zmq.SUBSCRIBE, "TEMP")

 
def get_temp(): # filling list
	while True:
		string = socket.recv()
		event_name, messagedata = string.split()
		#print event_name, messagedata
		if len(data) < 10:
			data.append(messagedata)
		else:
			break
	return data


@app.route('/')
def temperature_list_page():
	tempr = get_temp()
   	context = {'temperature': tempr}
   	return render_template('index_pith.html', data=context) 

@app.route('/help')
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # run_services()
    app.run('127.0.0.1', 8992, debug=False)


