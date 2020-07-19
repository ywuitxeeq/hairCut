# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: tormHelp.py
# Month: 七月
# time: 2020/7/17 16:43
# noqa
""" Write an introduction to the module here """
import tormysql
from settings.config import MYSQL_CONFIG
from functools import wraps
import logging
from utils.secretPwd import SecretPwd

MYSQL_CONFIG["passwd"] = SecretPwd.decode(MYSQL_CONFIG["passwd"])

pool = tormysql.ConnectionPool(
    # cursorclass=tormysql.DictCursor,
    **MYSQL_CONFIG
)


def decorator(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        to_dict = kwargs.pop('to_dict', None)
        if not isinstance(to_dict, bool):
            to_dict = None
        elif to_dict is True:
            to_dict = tormysql.DictCursor
        async with await pool.Connection() as conn:

            async with conn.cursor(cursor_cls=to_dict) as cursor:
                n = await func(__conn__=conn, __cursor__=cursor, *args, **kwargs)

        return n
    return wrapper


class TorMysqlHelp(object):

    @staticmethod
    @decorator
    async def query_all_execute(sql, args=None, **kwargs):
        """

        :param sql:
        :param args: ['a', 'b', 'c']
        :return:
        """
        cursor = kwargs['__cursor__']
        if not sql.strip().lower().startswith('select'):
            return None
        await cursor.execute(sql, args)
        return cursor.fetchall()

    @staticmethod
    @decorator
    async def query_one_execute(sql, args=None, **kwargs):
        """

        :param sql:
        :param args: ['a', 'b', 'c']
        :return:
        """

        cursor = kwargs['__cursor__']
        if not sql.strip().lower().startswith('select'):
            return None
        await cursor.execute(sql, args)
        return cursor.fetchone()

    @staticmethod
    @decorator
    async def commit_one_execute(sql, args=None, **kwargs):
        """
        返回最后一条记录的ID
        :param sql:
        :param args: ['a', 'b', 'c']
        :param kwargs:
        :return:
        """
        cursor = kwargs['__cursor__']
        conn = kwargs['__conn__']
        try:
            await cursor.execute(sql, args)
        except:
            await conn.rollback()
            logging.error(f"{sql} execute error")
            return
        else:
            await conn.commit()

        return cursor.lastrowid

    @staticmethod
    @decorator
    async def commit_executemany(sql, args=None, **kwargs):
        """

        last rowid  第一条记录的id
        last rowcount 插入的数量
        :param sql:
        :param args: [('a', 'b'), ('c', 'd')]
        :param kwargs:
        :return:
        """
        cursor = kwargs['__cursor__']
        conn = kwargs['__conn__']
        try:
            await cursor.executemany(sql, args)
        except:
            await conn.rollback()
            logging.error(f"{sql} executemany error")
            return
        else:
            await conn.commit()
        return cursor.lastrowid, cursor.rowcount

