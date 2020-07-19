# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: secretPwd.py
# Month: 七月
# time: 2020/7/17 23:22
# noqa
""" Write an introduction to the module here """
import base64
import json
import struct
from urllib.parse import quote, unquote


class SecretPwd(object):

    PACK_FORMAT = 'l'

    @staticmethod
    def encode(pwd, interval=5):

        result = SecretPwd.__my_encode(pwd)
        return SecretPwd.__caesar_cipher_encode(result, interval=interval)

    @staticmethod
    def decode(string, interval=5):
        result = SecretPwd.__caesar_cipher_decode(string, interval=interval)
        return SecretPwd.__my_decode(result)

    @staticmethod
    def __my_encode(data):
        """
        对 data 进行编码
        :param data:
        :return:
        """

        new_string = data

        key = '-'.join([str(oct(ord(_))).lstrip('0o') for _ in new_string])
        new_key = str(base64.b64encode(bytes(quote(key), encoding='utf8')), encoding='utf8')

        return new_key

    @staticmethod
    def __my_decode(data):
        """
        对 data 进行解码
        :param data:
        :return:
        """

        try:
            url_unquote = unquote(str(base64.b64decode(data), encoding='utf8'))
            target_info = f"{''.join([chr(int(nb, 8)) for nb in url_unquote.split('-')])}"
        except UnicodeDecodeError:
            return ''
        except ValueError:
            return ''

        return target_info

    @staticmethod
    def __caesar_cipher_encode(data: str, interval=3):
        """

        :param data:
        :param interval:
        :return:
        """
        assert 1 <= interval <= 25
        new_key = ''
        for i in data:
            if i.isdigit():
                new_key += i
            else:
                number = ord(i)
                if 'A' <= i <= 'Z':
                    target_num = number + interval
                    if target_num > 90:
                        target_num = 64 + target_num - 90
                elif 'a' <= i <= 'z':
                    number = ord(i)
                    target_num = number + interval
                    if target_num > 122:
                        target_num = 96 + target_num - 122
                else:
                    target_num = number
                new_key += chr(target_num)
        return new_key

    @staticmethod
    def __caesar_cipher_decode(data: str, interval=3):
        """

        :param data:
        :param interval:
        :return:
        """
        assert 1 <= interval <= 25
        new_key = ''
        for i in data:
            if i.isdigit():
                new_key += i
            else:
                number = ord(i)
                if 'A' <= i <= 'Z':
                    target_num = number - interval
                    if target_num < 65:
                        target_num = 91 + target_num - 65
                elif 'a' <= i <= 'z':
                    target_num = number - interval
                    if target_num < 97:
                        target_num = 123 + target_num - 97
                else:
                    target_num = number
                new_key += chr(target_num)
        return new_key


if __name__ == '__main__':
    result1 = SecretPwd.encode('123456')

    pwd1 = SecretPwd.decode(result1)
    print(result1)

