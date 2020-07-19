# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# SITE 
# fileName: main.py
# Month: 四月
# time: 2020/4/2 10:33
""" Write an introduction to the module here """
import os
import sys
sys.path.append(os.getcwd())

from EmailSendOrRecv.recv import *
from EmailSendOrRecv.send import *

USER = 'ywuitxeeq1@126.com'
PWD = 'TLMKIZONEAZTONST'
RECEIVE_HOST = 'imap.126.com'
SEND_HOST = 'smtp.126.com'


if __name__ == '__main__':

    # 收
    obj = emailRecv.EmailRecv(USER, PWD, RECEIVE_HOST)
    msg = obj.read()
    for uid, info in msg:
        # print(uid, info.body['html'])
        print(uid, info.subject)
    obj.logout()

    # 发

    obj = emailSend.EmailSend(USER, PWD, SEND_HOST)

    obj.send_email(to=['649865787@qq.com'], subject='给你说的秘密',
                   contents=['给你说的秘密 你能看出来它是谁吗?',
                             "请看附件内容 超经典",
                             """<a herf="#">百度</a>""",
                             ],)

    obj.logout()
