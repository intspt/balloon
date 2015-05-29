#!/usr/bin/env python
#-*- coding:utf-8 -*-

from functools import wraps

from flask import render_template, g, request, redirect, flash
from flask.ext.login import current_user, login_user, logout_user, login_required

from app import app, db, lm
from models import Team, User, SendBalloon
from analyseBoard import analyseBoard
from config import BALLOON_COLOR



def throw_exception(f):
    @wraps(f)
    def call(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            print e
            return unicode(e)
    return call



@lm.user_loader
def load_user(userid):
    return User.query.get(userid)



@app.before_request
def before_request():
    g.user = current_user



@app.route('/')
@throw_exception
def home():
    if current_user.is_authenticated():
        return render_template('admin.html')
    else:
        return render_template('summary.html')



@app.route('/login', methods = ['GET', 'POST'])
@throw_exception
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name, password = request.form['name'], request.form['password']
        if name:
            user = User.query.filter_by(name=name).first()
            if user is not None and password == user.password:
                login_user(user, remember=True)
                return redirect('/')
            else:
                return LOGIN_INFO_ERROR
        else:
            return LOGIN_INFO_ERROR



@app.route('/logout')
@login_required
@throw_exception
def logout():
    logout_user()
    return redirect('/')



@app.route('/board')
@throw_exception
def board():
    return render_template('summary.html')



@app.route('/addTeam', methods = ['GET', 'POST'])
@login_required
@throw_exception
def add_team():
    if request.method == 'GET':
        return render_template('addTeam.html')
    else:
        team_list = request.form['content'].split('\n')
        for team in team_list:
            name, location = team.split('\t')
            db.session.add(Team(name, location))
            db.session.commit()
            db.session.close()

        return redirect('/')



@app.route('/teamList')
@login_required
@throw_exception
def teamList():
    team_list = Team.query.all()
    return render_template('teamList.html', team_list=team_list)



@app.route('/deleteTeam')
@login_required
@throw_exception  
def delete_team():
    team = Team.query.filter_by(id_=request.args['tid']).first()
    db.session.delete(team)
    db.session.commit()
    db.session.close()
    return redirect('/teamList')



@app.route('/balloon')
@login_required
@throw_exception
def balloon():
    send_balloon_list = SendBalloon.query.order_by(SendBalloon.id_.desc()).all()
    return render_template('balloon.html', send_balloon_list=send_balloon_list, BALLOON_COLOR=BALLOON_COLOR)


@app.route('/changeStatus')
@login_required
@throw_exception
def change_status():
    SendBalloon.query.filter_by(id_=request.args['sid']).update({'is_sent': True})
    db.session.commit()
    db.session.close()
    return redirect('/balloon')


@app.route('/printBalloon')
@login_required
@throw_exception
def printBalloon():
    send_balloon_list = SendBalloon.query.order_by(SendBalloon.id_.desc()).all()
    return render_template('printBalloon.html', send_balloon_list=send_balloon_list, BALLOON_COLOR=BALLOON_COLOR)
