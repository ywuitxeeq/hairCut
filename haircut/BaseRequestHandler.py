# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: BaseRequestHandler.py
# Month: 七月
# time: 2020/7/17 15:26
# noqa
""" Write an introduction to the module here """
from abc import ABC

from tornado.web import RequestHandler


class BaseRequestHandler(RequestHandler, ABC):

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE, HEAD')

    def prepare(self): pass

    def get(self, *args, **kwargs): pass

    def post(self, *args, **kwargs): pass

    def put(self, *args, **kwargs): pass

    def patch(self, *args, **kwargs): pass

    def delete(self, *args, **kwargs): pass

    def head(self, *args, **kwargs): pass

    def on_finish(self) -> None:
        pass

    def set_default_headers(self) -> None:
        """Override this to set HTTP headers at the beginning of the request.

        For example, this is the place to set a custom ``Server`` header.
        Note that setting such headers in the normal flow of request
        processing may not do what you want, since headers may be reset
        during error handling.
        """
        referer = self.request.headers.get("Origin", '')
        allow_headers = 'Origin, X-Requested-With, content-Type, Accept, Authorization, Referer, User-Agent, Host'
        self.set_header('Access-Control-Allow-Origin', referer)
        self.set_header('Content-type', 'application/json;charset=utf8')
        self.set_header('Access-Control-Allow-Credentials', "true")
        self.set_header(
            'Access-Control-Allow-Headers', allow_headers)
        self.set_header('Access-Control-Max-Age', 1000)

