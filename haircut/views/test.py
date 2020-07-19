# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: test.py
# Month: 七月
# time: 2020/7/17 15:37
# noqa
""" Write an introduction to the module here """

from abc import ABC
from utils.DecimalDatetimeEncoder import DecimalDatetimeEncoder
from haircut.BaseRequestHandler import BaseRequestHandler
from utils.asyncUtil import logger
from utils.tormHelp import TorMysqlHelp
import json


class TestHandler(BaseRequestHandler, ABC):

    async def get(self, *args, **kwargs):

        name = self.get_argument('name', False)
        sql = """INSERT INTO `haircut_cart` (`uesr_id`, `product_id`, `quantity`, `checked`) VALUES (%s, %s, %s, %s)"""
        # n = await TorMysqlHelp.query_one_execute('select * from haircut_cart;', to_dict=True)
        n = await TorMysqlHelp.query_all_execute('select * from haircut_cart;', to_dict=True)
        # n = await TorMysqlHelp.commit_one_execute(sql, [2, 3, 5, 9])
        # n = await TorMysqlHelp.commit_executemany(sql, [(7, 3, 5, 9), (4, 3, 5, 9), (7, 3, 5, 9), (4, 3, 5, 9)])

        print(n)
        # await logger('日志测试 %s', name, method='WARN')
        self.write(json.dumps(n, cls=DecimalDatetimeEncoder,ensure_ascii=False))
        return

    def set_default_headers(self):
        """
        js 跨域
        :return:
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')


