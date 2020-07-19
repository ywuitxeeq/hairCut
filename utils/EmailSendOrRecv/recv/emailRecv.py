# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: emailRecv.py
# time: 2020/3/28 14:23
""" Write an introduction to the module here """
import logging

from ..base import EmailBase
from ..imap_utf7 import decode as mail_decode, encode as mail_encode
from imbox import Imbox


class EmailRecv(EmailBase):
    """
        messages.sent_from	发件人
        messages.sent_to	收件人
        messages.subject	邮件主题
        messages.date	发送日期
        messages.body['plain']	文本格式的正文
        messages.body['html']	HTML格式的正文
        messages.attachments	附件
        messages.parsed_date datetime 类型
    """

    def __init__(self, *args, **kwargs):
        self._server = None
        super(EmailRecv, self).__init__(*args, **kwargs)

    def _login(self, *args, **kwargs):
        if not isinstance(self._server, Imbox):

            self._server = Imbox(self._host, username=self._user,
                                 password=self._pwd, port=self._port, *args, **kwargs)

        return self._server

    def logout(self, *args, **kwargs):
        """
        退出
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(self._server, Imbox):
            try:
                self._server.logout()
            except Exception as e:
                logging.error('logout error %s', e)

    def folders(self):

        temp_list = list()

        folder_tuple = self._server.folders()
        if folder_tuple[0] != 'OK':
            return
        for folder in folder_tuple[1]:
            readable_folder = mail_decode(folder)
            temp_list.append(readable_folder.split()[-1].strip('"'))
        return temp_list

    def mark_seen(self, uuid):
        """
        标记本邮件已读
        :param uuid: 邮箱唯一编号
        :return:
        """
        self._server.mark_seen(uuid)

    def mark_flag(self, uuid):
        """
        标记红旗邮件
        :param uuid: 邮箱唯一编号
        :return:
        """
        self._server.mark_flag(uuid)

    def delete(self, uuid):
        """
        删除邮件
        :param uuid: 邮箱唯一编号
        :return:
        """
        self._server.delete(uuid)

    def read(self, **kwargs):
        """
        param folder：
              INBOX: (收件箱)
              草稿箱
              已发送
              已删除
              垃圾邮件
              病毒邮件
              广告邮件
        param unread: 未读邮件 bool
        param unflagged: 不是红旗邮件 bool
        param flagged: 红旗邮件 bool
        param sent_from: 读取某个发件人的邮件 str
        param sent_to: 读取某个收件人的邮件 str
        param date__gt: 某天之后
        param date__lt: 某天之前 datetime.date(2019, 10, 28)
        param lookup_error_ignore: 忽略LookUpError 错误 Bool
        param date__on:某天
        param subject: 主提邮件
        :param kwargs:
        :return: iter obj  example (email_id: str, msg:object )
        """
        lookup_error_ignore = kwargs.pop('lookup_error_ignore', False)

        self.__parser_folders(kwargs)
        all_messages = self._server.messages(**kwargs)
        if lookup_error_ignore:
            return self.iter_all_messages(all_messages)
        return all_messages

    @staticmethod
    def iter_all_messages(all_messages):
        n = 0
        length = len(all_messages._uid_list)  # noqa
        while n < length:
            try:
                uid = all_messages._uid_list[n]  # noqa
                msg = all_messages._fetch_email(uid)  # noqa
                n += 1
                yield uid, msg
            except LookupError as e:
                logging.error('uid %s error %s', uid, e)  # noqa
                n += 1

    @staticmethod
    def __parser_folders(folder_other):
        folder = folder_other.pop('folder', None)
        if folder:
            folder_other['folder'] = mail_encode(folder)

    def copy(self, uid, destination_folder):
        """

        :param uid: 邮箱唯一编号
        :param destination_folder: 目标文件夹
        :return:
        """

        return self._server.copy(uid, destination_folder)

    def move(self, uid, destination_folder):
        """
        :param uid: 邮箱唯一编号
        :param destination_folder: 目标文件夹
        :return:
        """
        self._server.move(uid, destination_folder)

