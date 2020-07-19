# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: DecimalDatetimeEncoder.py
# Month: 七月
# time: 2020/7/17 18:47
# noqa
""" Write an introduction to the module here """
import datetime
import decimal
import json


class DecimalDatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):

            return obj.strftime('%Y-%m-%d %H:%M:%S')
