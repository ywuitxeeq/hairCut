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

    FMT = '%Y-%m-%d %H:%M:%S'

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):

            return obj.strftime(self.FMT)


def new_format_encoder(fmt="%Y-%m-%d %H:%M:%S"):
    import copy
    new_encoder = copy.deepcopy(DecimalDatetimeEncoder)
    new_encoder.FMT = fmt
    return new_encoder
