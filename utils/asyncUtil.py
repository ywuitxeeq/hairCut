# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: asyncUtil.py
# Month: 七月
# time: 2020/7/17 15:28
# noqa
""" Write an introduction to the module here """
from utils.EmailSendOrRecv.send import emailSend
from settings.config import SEND_EMAIL_CONFIG


async def logger(msg, *args, method='info'):
    from haircut.Aplication import app
    level = dict(
        CRITICAL=50, FATAL=50, ERROR=40,
        WARNING=30, WARN=30, INFO=20,
        DEBUG=10, NOTSET=0,
    )
    if level.get(method.upper()):
        await app.logger(msg, *args, method=method)
    else:
        raise ValueError('no this method')


def send_email(to, subject, contents, **kwargs):
    """

    :param to: [xxx@qq.com]
    :param subject: 主题
    :param contents: 内容
    :param kwargs:
    :return:
    """
    import threading
    kwarg = dict(
        to=to,
        subject=subject,
        contents=contents,
        **kwargs)

    def send_to():
        with emailSend.EmailSend(**SEND_EMAIL_CONFIG) as send:
            send.send_email(**kwarg)

    threading.Thread(target=send_to).start()
