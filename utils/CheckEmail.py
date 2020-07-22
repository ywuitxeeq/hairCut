# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: CheckEmail.py
# Month: 七月
# time: 2020/7/18 1:00
# noqa
""" Write an introduction to the module here """
import re

reg = re.compile(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')


def check_email(email):
    """

    :param email:
    :return: true 验证成功
    """
    if not re.match(reg, email):
        return False
    return True


