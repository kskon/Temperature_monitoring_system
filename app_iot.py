import os
import sys
import time

import zmq

from flask import Flask
from flask import render_template, redirect, url_for, request, flash, make_response
from multiprocessing import Process, Queue

from forms import LoginForm

from pylib.subscriber import ZMQSubscriber



# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext import admin
# from flask.ext.admin.contrib import sqla
# from flask.ext.admin.contrib.sqla import filters
from flask_login import LoginManager
from flask_restful import Api

from pylib.pylib import get_random_uuid
from pylib.settings import SQLALCHEMY_DATABASE_URI
from pylib.settings import FLASK_SESSION_TYPE, FLASK_UPLOAD_FOLDER
from pylib.settings import FLASK_ALLOWED_EXTENSIONS, FLASK_RESOURCE_STATUSES
from pylib.db import DbProxy
from pylib.services import run_services
from pylib.log import logger


__NAME__ = "Temperature_monitoring"
ALLOWED_EXTENSIONS = set(FLASK_ALLOWED_EXTENSIONS)
STATUSES = set(FLASK_RESOURCE_STATUSES)

# Create application
app = Flask(__NAME__)
#, static_url_path = '/home/ubuntu/ocr/storage',
#                      static_folder = '/home/ubuntu/ocr/storage')

# Create dummy secrey key so we can use sessions
app.secret_key = get_random_uuid()
app.url_map.strict_slashes = False
app.config['SESSION_TYPE'] = FLASK_SESSION_TYPE
app.config['UPLOAD_FOLDER'] = FLASK_UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config.from_object('config') # ????
api = Api(app)


# Create database
# db = SQLAlchemy(app)

# Create admin
login_manager = LoginManager()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {'content-type': 'application/xml'})
    return resp

# Routes

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

# Main pages
@app.route('/')
# @login_required
def temperature_list_page():
    tempr = DbProxy()
    #tempr.get_all()
    context = {'temperature': tempr}
    return render_template('index.html', data=context) 

@app.route('/update/<rid>', methods=['POST'])
def resource_update(rid=None):
    dbproxy = DbProxy()
    res = dbproxy.get_resource(rid)
    if res:
        turn = request.form['turnon']
        turnon = False
        if turn == 'ON':
            turnon = True
        status = request.form['status']
        href = request.form['href']
        dbproxy.update_resource(rid=rid, turnon=turnon, status=status, href=href)
    flash("Item: ID=[{}] has been updated. {}".format(rid, request.form['status']))
    return redirect(url_for('resource_list_page'))

def do_subscribe():
    def save_results(queue, steps=1000):
        subscriber = ZMQSubscriber(queue=queue)
        while True:
            if not queue.empty():
                raw_msg = queue.get()
                message = raw_msg[6::]
                logger.debug('message through queue={}'.format(message))
                dbproxy.add_tempr(message)
            else:
                logger.debug('queue is empty')
                time.sleep(0.2)
    dbproxy = DbProxy()
    subscriber_queue = Queue()
    subscriber_process = Process(target=save_results, args=(subscriber_queue,))
    subscriber_process.start()

@app.route('/help')
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # run_services()


    do_subscribe()
    app.run('127.0.0.1', 8980, debug=True)
