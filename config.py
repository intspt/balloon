#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

SECRET_KEY = 'dark flame master'

BASE_DIR = os.getcwd()
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + os.sep + 'app' + os.sep + 'data' + os.sep + 'data.db'
BOARD_ADDR = BASE_DIR + os.sep + 'app' + os.sep + 'templates' + os.sep + 'summary.html'

ADMIN_NAME = 'rikka'
ADMIN_PASSWORD = 'yuta'

#队伍名称最大长度
TEAM_NAME_LEN = 99
#座位信息最大长度
TEAM_LOCATION_LEN = 99

#气球颜色列表，例如
#BALLOON_COLOR = [u'红', u'蓝']
BALLOON_COLOR = [u'红']
#题目总数
PROBLEM_NUM = 1