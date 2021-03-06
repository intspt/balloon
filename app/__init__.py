#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

FLASKS_ETTINGS = '../config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = False)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = '/login'