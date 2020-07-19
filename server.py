# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: server.py
# Month: 七月
# time: 2020/7/17 14:51
# noqa
""" Write an introduction to the module here """
from os import path as os_path
from sys import path as sys_path;sys_path.append(os_path.dirname(os_path.abspath(__file__)))  # noqa
from tornado.ioloop import IOLoop
import platform
from haircut.Aplication import create_app
from tornado.httpserver import HTTPServer
from settings.config import OPTIONS


def app_init():
    """

    :return:
    """
    import asyncio
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        try:
            import uvloop
        except ImportError:
            pass
        else:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    return create_app()


if __name__ == '__main__':

    app = app_init()

    http_server = HTTPServer(app)
    http_server.bind(OPTIONS.get('PORT'))
    http_server.start(OPTIONS.get('NUM_PROCESSES'))

    IOLoop.current().start()


