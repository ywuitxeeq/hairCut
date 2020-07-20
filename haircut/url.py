# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: url.py
# Month: 七月
# time: 2020/7/17 15:35
# noqa
""" Write an introduction to the module here """
from haircut.views import test
from haircut.views import account
from haircut.views import index
import tornado.web

urls = [
    ('/test', test.TestHandler),
    # 帐号相关
    tornado.web.url(r'/account/(?P<method>\w+?)',  account.AccountHandler, name="account"),
    (r'/account', account.AccountHandler),
    # 首页
    (r'/haircut/index', index.IndexHandler),
]


