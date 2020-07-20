# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: admin.py
# Month: 七月
# time: 2020/7/20 19:17
# noqa
""" Write an introduction to the module here """
from abc import ABC

from utils.asyncOpenFile import async_open
from haircut.BaseRequestHandler import BaseRequestHandler
from utils.asyncUtil import logger


class AdminHandler(BaseRequestHandler, ABC):

    async def get(self, method, **kwargs):
        result = await async_open(self.get_template_path(), 'index.html', 'admin')
        self.set_header('Content-Type', 'text/html; charset=utf-8')
        return self.write(result)

