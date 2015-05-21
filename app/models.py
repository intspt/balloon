#!/usr/bin/env python
#-*- coding:utf-8 -*-

from app import db



class Team(db.Model):
    __tablename__ = 'team'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(22))
    location = db.Column(db.String(99))

    def __init__(self, name, location):
        self.name = name
        self.location = location



class User(db.Model):
    __tablename__ = 'user'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(22))
    password = db.Column(db.String(22))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id_)