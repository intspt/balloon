#!/usr/bin/env python
#-*- coding:utf-8 -*-

from app import db
from config import TEAM_NAME_LEN, TEAM_LOCATION_LEN



class User(db.Model):
    __tablename__ = 'user'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(9))
    password = db.Column(db.String(9))

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



class Team(db.Model):
    __tablename__ = 'team'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(TEAM_NAME_LEN))
    location = db.Column(db.String(TEAM_LOCATION_LEN))
    problem_solved = db.Column(db.Integer)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.problem_solved = 0



class SendBalloon(db.Model):
    __tablename__ = 'sendballoon'
    id_ = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(TEAM_NAME_LEN))
    problem_id = db.Column(db.Integer)
    team_location = db.Column(db.String(TEAM_LOCATION_LEN))
    is_sent = db.Column(db.Boolean)

    def __init__(self, team_name, problem_id, team_location):
        self.team_name = team_name
        self.problem_id = problem_id
        self.team_location = team_location
        self.is_sent = False