#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Software: PyCharm
# __author__ == "HAI"
# FileName: 我的日志模块.py
# Date  : 2018/10/12
# Time  : 22:50
"""日志模块"""

import os
import logging as own_log
import platform
import datetime as log_datetime
from logging.handlers import RotatingFileHandler


class NewRotatingFileHandler(RotatingFileHandler):
    """给base模块增加方法"""

    def __init__(self, *args, **kwargs):
        before = 15
        try:
            self._before = int(kwargs.pop('before', before))
        except ValueError:
            self._before = before
        except TypeError:
            self._before = before
        else:
            if self._before < 0:
                self._before = 0
        super(NewRotatingFileHandler, self).__init__(*args, **kwargs)
        self.namer = self._change_name  # noqa
        self.rotator = self._rm_log  # noqa

    @staticmethod
    def _change_name(name):
        date = log_datetime.datetime.now().date().__str__()
        return "%s.%s" % (name, date)

    def _rm_log(self, source, dest):
        if os.path.exists(source):
            os.rename(source, dest)
        date = (log_datetime.datetime.now() -
                log_datetime.timedelta(days=self._before)).date()
        base = os.path.split(source)[0]
        file_list = os.listdir(base)
        rm_file_list = []
        for file_name in file_list:
            rm_file_path = os.path.join(base, file_name)
            if os.path.isfile(rm_file_path):
                date_str = file_name.rsplit(".", 1)[-1]  # type: str
                try:
                    y, m, d = date_str.split('-')
                except ValueError:
                    continue
                if all((y.isdecimal(), m.isdecimal(), d.isdecimal())):
                    expire_time = log_datetime.datetime(int(y), int(m), int(d)).date()
                    if expire_time < date:
                        rm_file_list.append(rm_file_path)
        for file_name in rm_file_list:
            os.remove(file_name)


class Logger(object):
    """日志"""

    @staticmethod
    def file_name_help(logger_name):
        logger_name = os.path.split(logger_name)[-1]
        suffix = os.path.splitext(logger_name)[-1]
        if not suffix:
            logger_name += '.log'
        return logger_name

    @staticmethod
    def create_file(path):
        with open(path, 'w'):
            pass

    @staticmethod
    def log_name(logger_name, path, flag=True):
        default_log_name = 'log.log'
        if flag:
            if logger_name:
                logger_name = Logger.file_name_help(logger_name)
                ph = os.path.join(path, logger_name)
                if logger_name not in os.listdir(path):
                    Logger.create_file(ph)
                file_path = ph
            else:
                file_path = os.path.join(path, default_log_name)
        else:
            if logger_name:
                logger_name = Logger.file_name_help(logger_name)
            else:
                logger_name = default_log_name
            ph = os.path.join(path, logger_name)
            if logger_name not in os.listdir(path):
                Logger.create_file(ph)
            file_path = ph
        return file_path

    @staticmethod
    def dir_file_help(path):
        """
        去除文件侠路径中的后缀名
        :param path:
        :return:
        """
        suffix = os.path.splitext(path)[-1]
        while suffix:
            path = path.rstrip(suffix)
            suffix = os.path.splitext(path)[-1]
        return path

    @staticmethod
    def wne_path(new_path, current_path=None):
        new_path_args = new_path.split('/') if new_path.find('/') != -1 else new_path.split('\\')
        if current_path:
            path = os.path.join(current_path, *new_path_args)
        else:
            sys_str = Logger.get_sys()
            if sys_str == "Windows":
                if new_path_args[0].find(':') != -1:
                    new_path_args[0] += os.sep
                path = os.path.join(*new_path_args)
            elif sys_str == "Linux":
                if new_path_args[0] == '':
                    new_path_args[0] = os.sep
                path = os.path.join(*new_path_args)
            elif sys_str == "Darwin":
                if new_path_args[0] == '':
                    new_path_args[0] = os.sep
                path = os.path.join(*new_path_args)
            else:
                path = new_path
        path = Logger.dir_file_help(path)
        return path

    @staticmethod
    def get_sys():
        sys_str = platform.system()
        return sys_str

    @staticmethod
    def parse(path, current_path):
        """
        解析 .. 路径
        :param path:
        :param current_path:
        :return:
        """
        new_path_args = path.split('/') if path.find('/') != -1 else path.split('\\')
        new_path_args = list(filter(lambda x: x != '', new_path_args))
        length = len(new_path_args)
        row = 0
        while row < length:
            if new_path_args[row] == '..':
                current_path = os.path.dirname(current_path)
                new_path_args.remove(new_path_args[row])
                row -= 1
                length -= 1
            else:
                break
            row += 1
        return os.path.join(current_path, *new_path_args)

    @staticmethod
    def parser_safe_path(path):
        # todo 如果文件中有\f开头的目录会有报错情况 这是解决他的方法
        path = path.encode('unicode_escape').decode('utf-8')
        return path

    @staticmethod
    def my_log(file_path=None, logger_name=None, stream_handler=False,
               set_logging_level=None, before=15,
               print_save_path=False, system_name=None, rotating_file=True, max_bytes=(1 << 20) * 500, backup_count=50,
               end_chr=True, chrset='utf-8'):
        """
        :param stream_handler: 是否打印打屏幕
        :param rotating_file: 控制 max_bytes backup_count 是否生效
        :param max_bytes:  日志文件最大大小
        :param backup_count:  日志保留最大个数
        :param print_save_path:  打印文件保存路径
        :param file_path: 文件路径 默认桌面 . 当前路径  ./acd/acd 当前文件路径下的acd/acd路径
        :param system_name:  系统名 默认 root
        :param logger_name:  日志文件名 默认 mylog.log
        :param set_logging_level:  日志级别
        :param before:  删除多少天以前的
        :param chrset:  utf-8
        :param end_chr:  结尾加回车
        :return:
        """
        if file_path is None:
            path = Logger.parser_safe_path(os.path.join(os.path.expanduser("~"), 'Desktop', 'mylog'))
            if not os.path.isdir(path):
                os.makedirs(path)
            file_path = Logger.log_name(logger_name, path)
        elif file_path.startswith('..'):
            current_path = os.getcwd()
            file_path = Logger.parse(file_path, current_path)
            path = Logger.wne_path(file_path)
            if not os.path.isdir(path):
                os.makedirs(path)
            file_path = Logger.log_name(logger_name, path)
        elif file_path.startswith('.'):
            current_path = os.getcwd()
            new_path = file_path[1:]
            path = Logger.wne_path(new_path, current_path)
            if not os.path.isdir(path):
                os.makedirs(path)
            file_path = Logger.log_name(logger_name, path)
        elif file_path:
            path = Logger.wne_path(file_path)
            if not os.path.isdir(path):
                os.makedirs(path)
            file_path = Logger.log_name(logger_name, path, flag=False)
        else:
            raise ValueError('文件路径错误')
        file_path = Logger.parser_safe_path(file_path)
        logger = own_log.getLogger(name=system_name)
        if rotating_file:
            #  maxBytes = 文件日志大小超过另起一个文件  backupCount 日志保留最大个数
            fh = NewRotatingFileHandler(
                file_path, maxBytes=max_bytes, backupCount=backup_count,
                encoding=chrset, before=before)
        else:
            fh = own_log.FileHandler(file_path, encoding=chrset)

        sys_str = Logger.get_sys()
        if sys_str == "Windows" and end_chr:
            char = '\r'
        elif sys_str == "Linux" and end_chr:
            char = '\n'  # \000
        elif sys_str == "Darwin" and end_chr:
            char = '\r'
        else:
            char = ''
        mat = 'process ID%(process)d: %(asctime)s-%(name)s-%(levelname)s' \
              '-%(module)s-[line:%(lineno)d]-[function: %(funcName)s]-%(message)s{}'.format(char)
        formatter = own_log.Formatter(mat)

        # 文件操作符和格式关联
        fh.setFormatter(formatter)

        # logger 对象和文件操作符关联
        logger.addHandler(fh)
        if stream_handler is True:
            sh = own_log.StreamHandler()  # 创建一个屏目控制对象
            stream_handler_formater = own_log.Formatter(
                'PROCESS ID:%(process)d: %(asctime)s-%(name)s-%(levelname)s -[function: %(funcName)s]-'
                '[line:%(lineno)d]: %(message)s')
            sh.setFormatter(stream_handler_formater)
            logger.addHandler(sh)
        if set_logging_level:
            level = dict(
                CRITICAL=50, FATAL=50, ERROR=40,
                WARNING=30, WARN=30, INFO=20,
                DEBUG=10, NOTSET=0,
            )
            if isinstance(set_logging_level, int):
                log_lev = set_logging_level
            elif set_logging_level.isdigit():
                log_lev = int(set_logging_level)
            elif isinstance(set_logging_level, str):
                log_lev = level.get(set_logging_level.upper(), None)
            else:
                log_lev = 10
            if log_lev and log_lev <= 50:
                logger.setLevel(log_lev)
        else:
            logger.setLevel(10)
        if print_save_path is True:
            print(file_path)
        return logger


def logging_config(*args, **kwargs):
    """
    filepath=None 打印日志的文件路径
    streamhandler=False  屏目对象
    logger_name=None  日志文件名
    set_logging_level=None  设置等级
    system_name=None  改变系统名字
    :return:
    """
    obj = Logger.my_log(*args, **kwargs)
    return obj


def error_detail(log_fuc):
    """

    :param log_fuc: 函数对象 如 logging.info logging.debug
    :return:
    """
    import traceback

    log_fuc(traceback.format_exc())


if __name__ == '__main__':

    def test1():
        print(1 / 0)


    logging = logging_config(
        stream_handler=True,
        logger_name='getbooking',
        set_logging_level=None,
        system_name=' ',
        before=0,
        print_save_path=True
    )
    # logger_obj.error('错误')
    # logger_obj.debug('...')
    # logger_obj.warning('警告信息')
    #
    # logger_obj2 = main(streamhandler=True, filepath=r'D:\python_learning\study\mylog.log', system_name='你好')
    for i in range(10):
        logging.error('错误')
        logging.debug('...')
        logging.warning('警告信息')

    # try:
    #     test1()
    # except ZeroDivisionError as e:
    #
    #     error_detail(logger_obj.info)