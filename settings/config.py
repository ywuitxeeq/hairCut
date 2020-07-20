# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: config.py
# Month: 七月
# time: 2020/7/17 14:59
# noqa
""" Write an introduction to the module here """

from os import path

BASE_PATH = path.dirname(path.dirname(__file__))

OPTIONS = {
    'PORT': 80,
    'NUM_PROCESSES': 1,
}

SETTINGS = {
    # "debug": True, #可以用以下四个方法分别设置
    # 'debug': False,
    'autoreload': False,  # 自动重启
    'complited_template_cache': False,  # 取消缓存编译的模板
    'static_hash_cache': False,  # 取消hash 缓存
    # 'server_traceback':False, # 取消提供跟踪信息 用得少

    'static_path': path.join(BASE_PATH, 'static'),
    'template_path': path.join(BASE_PATH, 'templates'),
    'xsrf_cookies': False,  # 开启后在模板里面加{% module xsrf_form_html() %}
    'cookie_secret': 'lF3G8L7fQdehKh3XroTsO1K5aAXqGEHPkCVUofJQ/vA=',
    # 'login_url':'/login.html',
}

MYSQL_CONFIG = dict(
    max_connections=50,  # max open connections
    idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
    wait_connection_timeout=3,  # wait connection timeout
    host="127.0.0.1",
    user="root",
    passwd="SoJySoNySoRySoVySoZySoD=",
    db="haircut",
    charset="utf8",
    autocommit=False
)

SEND_EMAIL_CONFIG = {
    "user": 'ywuitxeeq1@126.com',
    "pwd": 'TLMKIZONEAZTONST',
    "host": "smtp.126.com"
}

RECV_EMAIL_CONFIG = {
    "user": 'ywuitxeeq1@126.com',
    "pwd": 'TLMKIZONEAZTONST',
    "host": "imap.126.com"
}


TOKEN_EXPIRE_TIME = 30
