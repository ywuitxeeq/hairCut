# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: status_code.py
# Month: 七月
# time: 2020/7/22 19:43
# noqa
""" Write an introduction to the module here """


from haircut.BaseRequestHandler import BaseRequestHandler
from abc import ABC


class StatusHandler(BaseRequestHandler, ABC):

    async def get(self, *args, **kwargs):
        self.send_error(404)

    async def post(self, *args, **kwargs):
        self.send_error(404)

    def set_default_headers(self):
        super(StatusHandler, self).set_default_headers()
        self.set_header('Content-type', 'text/html;charset=utf-8')


