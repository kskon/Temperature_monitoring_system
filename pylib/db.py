# -*- python -*-
# author: krozin@gmail.com
# db: created 2016/11/05
# author: kskonovalov100@gmail.com
# PC-resources: added 2016/11/21
# copyright

import datetime
import hashlib
import os
import random
import unittest

from sqlalchemy import Column, Boolean, Integer, String, Date, Time, DateTime
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DBPATH

Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'temperature'
    id = Column(Integer, primary_key=True)
    temperature = Column(String(10))
    date = Column(Date) # last_data_update
    time = Column(Time) # last_time_update

    def __init__(self,
                 temperature='temperature',
                 d=datetime.datetime.now(),
                 t=datetime.datetime.now().time()):
        self.temperature = temperature
        self.date = d
        self.time = t

    def __repr__(self):
        return "<Temperature({} {} {}|{})>".format(
            self.id, self.temperature,
            self.date, self.time)

    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    uname = Column(String(30))
    password = Column(String(256))

    def __init__(self,
                uname = uname,
                password = password):
        self.uname = uname
        self,password = password

    def __repr__(self):
        return "<Users({} {}|{})>".format(
            self.id, self.uname, self.password)

class DbProxy(object):

    def __init__(self):
        if not os.path.exists(DBPATH):
            with open(DBPATH, 'a'):
                os.utime(DBPATH, None)

        self._init_engine(uri='sqlite:///{}'.format(DBPATH), echo=True)
        self._init_db()

    def _init_engine(self, uri, **kwards):
        self.engine = create_engine(uri, **kwards)

    def _init_db(self):
        self.session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def add_temp(self, **kwargs):
        print "add_resource"
        res = Temperature(
            temperature=kwargs.get('temperature'))
        self.session.add(res)
        self.session.commit()
        return res.id

    def get_resource(self, rid):
        return self.session.query(Temperature).filter(Temperature.id == rid).first()

    def update_resource(self, rid, **kwargs):
        #name = kwargs.get('name')
        #href = kwargs.get('href')
        #turnon = kwargs.get('turnon')
        #status = kwargs.get('status')
        #d = kwargs.get('date')
        #t = kwargs.get('time')
        #uptime = kwargs.get('uptime')
        self.session.query(Temperature).filter(Temperature.id == rid).update(kwargs)
        self.session.commit()

    def delete_resource(self, rid):
        self.session.query(Temperature).filter(Temperature.id == rid).delete()
        self.session.commit()

    def get_all(self, order1=Temperature.date, order2=Temperature.time):
        return self.session.query(Temperature).order_by(desc(order1), desc(order2)).all()

    def add_tempr(self, d):
        print "add_tempr"
        res = Temperature(temperature=d.get('temperature'))
        self.session.add(res)
        self.session.commit()
        return res.id

if __name__ == '__main__':
    unittest.main(verbosity=7)