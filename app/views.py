#!/usr/bin/env python
#-*- coding:utf-8 -*-

from functools import wraps

from flask import render_template, g, request, redirect, flash
from flask.ext.login import current_user, login_user, logout_user, login_required

from app import app, db, lm
from models import Team, User
from config import color, problem_num, balloon_list, sent_list, teams
from getBoard import getBoard



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
            name, password, location = team.split()
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



@app.route('/balloon', methods = ['GET', 'POST'])
@login_required
@throw_exception
def balloon():
    global color, problem_num, balloon_list, sent_list 
    if request.method == 'POST':
        problem_num = int(request.form['problem_num'])
        color = []
        for i in range(problem_num):
            color.append([str(i + 1), request.form[str(i + 1)]])
        return redirect('/balloon')
    elif problem_num == 0:
        sent_list = []
        return render_template('balloon.html', balloonList = [], teams = [], solve_list = [], problem_num = problem_num, color = [])
    else:
        solve_list = getBoard(problem_num)
        balloon_list = []
        cnt = 0
        for record in solve_list:
            # print record
            if record[1] != '0':
                # print record[0].encode('utf-8'), record
                team = User.query.filter_by(name = record[0]).first()
                flag = -1
                for idx in range(len(teams)):
                    if team.name == teams[idx][0]:
                        flag = idx
                        break
                if flag == -1:
                    teams.append([team.name] + [None for i in range(problem_num)])
                    flag = len(teams) - 1
                print flag
                for i in range(problem_num):
                    if record[2 + i][2] != '-':
                        message = u'给座位:' + team.location + u' 队伍:' + team.name + u' 送第' + str(i + 1) + u'题 ' + color[i][1] +u'色气球'
                        # print message.encode('utf-8')
                        balloon_list.append([message, cnt])
                        cnt += 1
                        if cnt > len(sent_list):
                            sent_list.append([False, flag, i + 1])
                        teams[flag][i + 1] = sent_list[cnt - 1][0]
        return render_template('balloon.html', balloon_list = balloon_list, teams = teams, sent_list = sent_list, problem_num = problem_num, color = color)



@app.route('/resetBalloon')
@login_required
@throw_exception
def resetBalloon():
    global color, problem_num, sent_list
    problem_num = 0
    color = []
    sent_list = []
    teams = []
    return redirect('/balloon')



@app.route('/sendBalloon/<int:idx>')
@login_required
@throw_exception
def sendBalloon(idx):
    global sent_list
    sent_list[idx][0] = True
    teams[sent_list[idx][1]][sent_list[idx][2]] = True
    return redirect('/balloon')




