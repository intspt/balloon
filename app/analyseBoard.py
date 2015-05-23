#-*- coding:utf-8 -*-

import os, re

from bs4 import BeautifulSoup 

from app import db
from config import BOARD_ADDR, PROBLEM_NUM
from models import Team, SendBalloon



def analyseBoard():
    if not os.path.exists(BOARD_ADDR):
        print 'path error or summary.html does not exist!'
    else:
        board = BeautifulSoup(open(BOARD_ADDR, 'r').read())
        tr_list = board.find_all(style="border-bottom: 1px solid black;height: 42px;")
        for tr in tr_list:
            td_list = tr.find_all('td')
            team_name = td_list[1].get_text().split('\n')[0]
            problem_status_list = td_list[4: 4 + PROBLEM_NUM]
            team = Team.query.filter_by(name=team_name).first()
            team_location, team_problem_solved = team.location, team.problem_solved
            for (i, problem_status) in enumerate(problem_status_list):
                if '/' in problem_status.get_text():
                    if ((team_problem_solved >> i) & 1) == 0:
                        problem_solved = Team.query.filter_by(name=team_name).first().problem_solved
                        Team.query.filter_by(name=team_name).update({'problem_solved': problem_solved | (1 << i)})
                        send_balloon = SendBalloon(team_name, i, team_location)
                        db.session.add(send_balloon)
                        db.session.commit()
                        db.session.close()
