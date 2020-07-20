# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: index.py
# Month: 七月
# time: 2020/7/20 14:38
# noqa
""" Write an introduction to the module here """
from abc import ABCMeta

from haircut.BaseRequestHandler import BaseRequestHandler


class IndexHandler(BaseRequestHandler, metaclass=ABCMeta):

    async def get(self, *args, **kwargs):

        return self.write('ok')
