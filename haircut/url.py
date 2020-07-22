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
from haircut.views import status_code
from haircut.views.admin import admin
import tornado.web

urls = [
    ('/test', test.TestHandler),
    # 帐号相关
    tornado.web.url(r'/account/(?P<method>\w+?)$', account.AccountHandler, name="account"),
    (r'/account', account.AccountHandler),
    # 首页
    (r'/haircut/index', index.IndexHandler),
    (r'/', index.IndexHandler),

    # 后台管理
    tornado.web.url(r'/haircut/admin/user/disable$', admin.DisableUserHandler, name="disable"),  # 禁用
    tornado.web.url(r'/haircut/admin/login.html', admin.AdminLoginHandler),  # 后台登陆
    tornado.web.url(
        r'/haircut/admin/data/(?P<method>\w+)/(?P<table>.*)$',
        admin.AdminAsyncDataHandler,
        name='data_handler'),  # 数据处理
    tornado.web.url(r'/haircut/admin/(?P<method>.*?)$', admin.AdminHandler, name="admin"),  # 页面处理

    (r'.*$', status_code.StatusHandler),
]
