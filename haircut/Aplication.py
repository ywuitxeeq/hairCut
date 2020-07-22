# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: Aplication.py
# Month: 七月
# time: 2020/7/17 14:52
# noqa
""" Write an introduction to the module here """
import tornado.web
from tornado.ioloop import IOLoop
from settings.log import logging_config
from settings.config import BASE_PATH, SETTINGS
from os import path
from haircut.url import urls
import functools


__all__ = ["create_app", "app"]


class Application(tornado.web.Application):

    def __init__(self):
        super(Application, self).__init__(handlers=urls, **SETTINGS)

        self._logger = logging_config(
            file_path=path.join(BASE_PATH, 'log', 'haircut'),
            logger_name='haircut.log',
            stream_handler=True, set_logging_level='error')

    async def logger(self, msg, *args, method='info'):
        method = method.lower()
        if hasattr(self._logger, method):
            log = functools.partial(getattr(self._logger, method), msg, *args)
            await IOLoop.instance().run_in_executor(None, log)


app = Application()


def create_app():
    return app
