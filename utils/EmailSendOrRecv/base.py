# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: base.py
# time: 2020/3/28 14:07
""" Write an introduction to the module here """

from abc import abstractmethod, ABCMeta


class EmailBase(metaclass=ABCMeta):
    """邮箱基本类"""

    def __init__(self, user, pwd, host, port=None, *args, **kwargs):
        self._user = user
        self._pwd = pwd
        self._host = host
        self._port = port
        self._login(*args, **kwargs)

    @abstractmethod
    def _login(self, *args, **kwargs):
        pass

    @abstractmethod
    def logout(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, types, value, traceback):
        self.logout()




