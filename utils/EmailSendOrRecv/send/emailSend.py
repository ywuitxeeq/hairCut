# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: emailSend.py
# time: 2020/3/28 14:24
""" Write an introduction to the module here """
import yagmail
from ..base import EmailBase


class EmailSend(EmailBase):
    """邮件发送 map.vip.126.com"""

    def __init__(self, *args, **kwargs):
        self._server = None
        super(EmailSend, self).__init__(*args, **kwargs)

    def _login(self, *args, **kwargs):
        if self._server is None:

            self._server = yagmail.SMTP(user=self._user,
                                        password=self._pwd, host=self._host,
                                        port=self._port,
                                        *args, **kwargs)

    def logout(self, *args, **kwargs):
        if self._server is not None:
            self._server.close()

    def send_email(self, **kwargs):
        """
        发送带有内嵌的邮件  yagmail.inline('demo.png')
        param to  收件人列表 ['xxx@126.com', 'xxx@163.com']
        param subject  邮件标题
        param contents  邮件内容 ['xxx', 'xxx.html', '<a href="#">百度</a>']
        param attachments  附件 example [xxx.jpg, C:\\xxx\\xxx\\xx.xml']
        param cc  邮件抄送人 ['xxx@126.com', 'xxx@163.com']
        param bcc 密秘邮件抄送人 ['xxx@126.com', 'xxx@163.com']
        param preview_only 只是查看信息不发送
        param headers dict {"Form": "nick name"}
        param newline_to_break bool   if newline_to_break: content_string = content_string.replace("\n", "<br>")
        :param kwargs:
        :return:
        """
        return self._server.send(**kwargs)

