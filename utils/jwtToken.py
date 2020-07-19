# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: jwtToken.py
# Month: 七月
# time: 2020/7/18 11:18
# noqa
""" Write an introduction to the module here """

import jwt
import datetime
from jwt import exceptions
import struct
import base64
from urllib.parse import quote, unquote
import json


class ClassOnlyMethod(classmethod):
    """
    类
    """
    def __get__(self, instance, cls=None):  #
        if instance is not None:
            raise AttributeError("This method is available only on the class, not on instances.")
        return super(ClassOnlyMethod, self).__get__(instance, cls)


classonlymethod = ClassOnlyMethod


class TokenClass(object):

    SALT = '5963af15575143a48a4285e257f2c9b11576223998'  # 盐
    PACK_FORMAT = 'l'
    CAESAR_CIPHER = True  # 凯撒密码是否启用
    CUSTOM_ENCRYPTION = False  # 自定义加密码是否起用
    __TEMP_INFO = 'TEMP_INFO'

    @classonlymethod
    def create_token(cls, payload: dict, salt=None, interval=3, expire_time=10, alg='HS256', expire_flag=True):
        """

        :param payload: {'user_id': 1,  # 自定义用户ID 'username': 'wupeiqi',  # 自定义用户名 'exp':   # 超时时间}
        :param salt:  盐
        :param interval:  凯撒密码步长
        :param alg: 加密方式 HS256 HS384 HS512
        :param expire_time: 10 分钟
        :param expire_flag: 失效标记
        :return:
        """
        # 构造header
        headers = {
            'typ': 'JWT',
            'alg': alg
        }
        new_payload = TokenClass.__my_encode(payload) if TokenClass.CUSTOM_ENCRYPTION else payload
        if not new_payload.get('exp') and expire_flag:
            new_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_time)  # 超时时间
        result = jwt.encode(new_payload, key=salt if salt else TokenClass.SALT, algorithm=alg,
                            headers=headers).decode('utf8')
        ret = TokenClass.__caesar_cipher_encode(result, interval=interval) if TokenClass.CAESAR_CIPHER else result
        return ret

    @classonlymethod
    def decode_token(cls, token, interval=3, salt=None, alg=None):
        """

        :param token:
        :param salt: 盐
        :param interval: 凯撒密码步长
        :param alg: list
        :return:
        """

        if not alg:
            alg = ['HS256', 'HS384', 'HS512']
        elif isinstance(alg, str):
            alg = [alg]
        try:
            # 从token中获取payload[不校验合法性]
            # unverified_payload = jwt.decode(token, None, False)
            # print(unverified_payload)

            # 从token中获取payload[校验合法性]
            token = TokenClass.__caesar_cipher_decode(token, interval=interval) if TokenClass.CAESAR_CIPHER else token
            verified_payload = jwt.decode(token, key=salt if salt else TokenClass.SALT, verify=True, algorithms=alg)
            verified_payload.pop('exp', None)
        except exceptions.ExpiredSignatureError:
            # todo token已失效
            return {'ret': 300, 'msg': 'The token has expired'}
        except jwt.DecodeError:
            # todo token认证失败
            return {'ret': 301, 'msg': 'Token authentication failed'}
        except jwt.InvalidTokenError:
            # todo 非法的token
            return {'ret': 302, 'msg': 'Illegal token'}
        except ValueError:
            return {'ret': 303, 'msg': 'Wrong decryption method'}
        else:
            try:
                data = TokenClass.__my_decode(verified_payload) if TokenClass.CUSTOM_ENCRYPTION \
                    else verified_payload

            except KeyError:
                return {'ret': 303, 'msg': 'Wrong decryption method'}
            if TokenClass.__TEMP_INFO in data:
                return {'ret': 304, 'msg': 'Wrong decryption method'}
            elif 'ret' not in data:
                return {'ret': 0, 'data': data}
            return data

    @classonlymethod
    def __my_encode(cls, data):
        """
        对 data 进行编码
        :param data:
        :return:
        """
        exp = data.pop('exp', '')
        new_string = json.dumps(data)

        key = '-'.join([str(oct(ord(_))).lstrip('0o') for _ in new_string])
        temp_list = []
        for pack in key:
            if pack == '-':
                temp_list.append('-')
            else:
                temp_list.append(struct.pack(TokenClass.PACK_FORMAT, int(pack)).decode('utf8'))
        new_key = '&'.join(temp_list)
        new_key = str(base64.b64encode(bytes(quote(new_key), encoding='utf8')), encoding='utf8')
        if exp:
            dict_info = {TokenClass.__TEMP_INFO: new_key, 'exp': exp}
        else:
            dict_info = {TokenClass.__TEMP_INFO: new_key}
        return dict_info

    @classonlymethod
    def __my_decode(cls, data):
        """
        对 data 进行解码
        :param data:
        :return:
        """
        info = data[TokenClass.__TEMP_INFO]
        url_unquote = unquote(str(base64.b64decode(info), encoding='utf8'))
        tm_list = []
        for _ in url_unquote.split('&'):
            if _ == '-':
                tm_list.append(_)
            else:
                temp_char = struct.unpack(TokenClass.PACK_FORMAT, bytes(_, encoding='utf8'))
                tm_list.append(str(temp_char[0]))

        target_info = f"{''.join([chr(int(nb, 8)) for nb in ''.join(tm_list).split('-')])}"
        return {'ret': 0, 'data': json.loads(target_info)}

    @classonlymethod
    def __caesar_cipher_encode(cls, data: str, interval=3):
        """

        :param data:
        :param interval:
        :return:
        """
        assert 1 <= interval <= 25
        header, body, md5 = data.split('.')
        data = '\\'.join([md5, body, header])
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

    @classonlymethod
    def __caesar_cipher_decode(cls, data: str, interval=3):
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
        md5, body, header = new_key.split('\\')
        new_key = '.'.join([header, body, md5])
        return new_key


token_class = TokenClass

