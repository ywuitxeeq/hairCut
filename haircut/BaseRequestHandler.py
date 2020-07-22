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

from utils.jwtToken import token_class


class BaseRequestHandler(RequestHandler, ABC):

    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        self.user = None
        self.auth = None

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE, HEAD')

    async def prepare(self):
        head_auth = self.request.headers.get("Authorization")
        cookie_auth = self.get_cookie("authorization")
        if head_auth:
            auth = head_auth
        elif cookie_auth:
            from urllib.parse import unquote
            auth = unquote(cookie_auth)
        else:
            auth = ''
        res = token_class.decode_token(auth, interval=6)
        if res['ret'] == 0:
            self.user = res['data']
            self.auth = True

    async def get(self, *args, **kwargs): pass

    async def post(self, *args, **kwargs): pass

    async def put(self, *args, **kwargs): pass

    async def patch(self, *args, **kwargs): pass

    async def delete(self, *args, **kwargs): pass

    async def head(self, *args, **kwargs): pass

    def on_finish(self) -> None:
        super(BaseRequestHandler, self).on_finish()

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

    def write_error(self, status_code, **kwargs):
        
        if status_code == 404:
            return self.render('admin/error.html')
        return super(BaseRequestHandler, self).write_error(status_code, **kwargs)
