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
from sqlalchemy import desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DBPATH

Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'temperature'
    id = Column(Integer, primary_key=True)
    temperature = Column(String(10))
    date_time = Column(DateTime)

    def __init__(self,
                 temperature='temperature',
                 d=datetime.datetime.now()):
        self.temperature = temperature
        self.date_time = d

    def __repr__(self):
        return "{} {}".format(
            self.temperature,
            self.date_time)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(30))
    password = Column(String(256))

    def __init__(self,
                email = email,
                password = password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "Users({} {}/{}".format(
            self.id, 
            self.email, 
            self.password)

class Revers(Base):
    __tablename__ = "revers"
    id = Column(Integer, primary_key=True)
    new_temperature = Column(String(10))


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
        res = Temperature(temperature=kwargs.get('temperature'))
        self.session.add(res)
        self.session.commit()
        return res.id

    def get_resource(self, rid):
        return self.session.query(Temperature).filter(Temperature.id == rid).first()

    def get_count(self):
        return self.session.query(Temperature).filter(Temperature.id == rid).first()

    def update_resource(self, rid, message):
        #name = kwargs.get('name')
        #href = kwargs.get('href')
        #turnon = kwargs.get('turnon')
        #status = kwargs.get('status')
        #d = kwargs.get('date')
        #t = kwargs.get('time')
        #uptime = kwargs.get('uptime')
        self.session.query(Temperature).filter(Temperature.id == rid).update(message)
        self.session.commit()

    def delete_resource(self, rid):
        self.session.query(Temperature).filter(Temperature.id == rid).delete()
        self.session.commit()

    def get_all(self, order1=Temperature.date_time):
        return self.session.query(Temperature).order_by(order1).all()

    def add_tempr(self, message):
        res = Temperature(temperature=message, d=datetime.datetime.now())
        #count  = self.session.query(func.count('*')).select_from(Temperature)
        count  = self.session.execute("select count(*) from Temperature").scalar()
        print "aaaaaaa"
        print count 
        if count < 10:
            self.session.add(res)
        else:
            res_oldest = self.session.query(Temperature).order_by(Temperature.date_time).first() 
            print "Alesha"
            print res_oldest
            if res_oldest:
                res_oldest.date_time = datetime.datetime.now()
                res_oldest.temperature = message

        self.session.commit()

if __name__ == '__main__':
    unittest.main(verbosity=7)