# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: account.py
# Month: 七月
# time: 2020/7/17 18:49
# noqa
""" Write an introduction to the module here """
from abc import ABCMeta
from utils.asyncUtil import logger
from utils.secretPwd import SecretPwd
from utils.asyncOpenFile import async_open
from utils.tormHelp import TorMysqlHelp
from utils.CheckEmail import check_email
from haircut.BaseRequestHandler import BaseRequestHandler
from utils.jwtToken import token_class
from settings.config import TOKEN_EXPIRE_TIME


class AccountHandler(BaseRequestHandler, metaclass=ABCMeta):

    STRING_DICT = {
        "@hairCutBaseTitle": "",
        "@hairCutBaseUrl": "http://192.168.32.1",
        "@username": ''
    }

    def __init__(self, *args, **kwargs):
        super(AccountHandler, self).__init__(*args, **kwargs)
        self.user = None
        self.auth = None

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
            self.STRING_DICT['@username'] = self.user['username']
            self.auth = True

    async def get(self, method=None, **kwargs):

        return await self.dispatch(method, 'get')

    async def post(self, method=None, **kwargs):

        return await self.dispatch(method, 'post')

    async def dispatch(self, method, request_method='get'):
        """
        分发
        :param method:
        :param request_method:
        :return:
        """
        if method is None:
            content = await async_open(self.get_template_path(), 'login.html')
            return self.finish(content)
        elif method.title() == 'Login':
            obj = Login()
        elif method.title() == "Register":
            obj = Register()
        elif method.title() == "Modify":
            obj = Modify()
        elif method.title() == "Retrieve":
            obj = RetrievePassword()
        elif method == "active_token":
            return await active_token(self)
        elif method == "emailPassword":
            return await email_to_password(self)
        else:
            return self.write("404: Not Found")
        return await getattr(obj, request_method)(self)

    @staticmethod
    def replace_string(string: str, string_dict: dict):

        for k, v in string_dict.items():
            string = string.replace(k, v)
        return string

    def is_ajax(self):
        """
        是否是第一次访问
        真 第一次访问
        :return:
        """
        res = self.get_query_argument("async", "false")
        if res != 'true':
            self.set_header('Content-Type', 'text/html; charset=utf-8')
            return True
        else:
            return False


class Login(object):
    """
    登陆
    """

    async def get(self, obj):
        if obj.auth:
            return obj.redirect("/haircut/index")
        if obj.is_ajax():
            result = await async_open(obj.get_template_path(), 'base.html')
            obj.STRING_DICT['@hairCutBaseTitle'] = "登陆"
            return obj.finish(obj.replace_string(result, obj.STRING_DICT))
        return obj.write({"status": 1000})

    async def post(self, obj):
        if obj.auth:
            return obj.write({"status": 1006, "msg": "已经登陆"})
        username = obj.get_body_argument("username", None, strip=True)
        password = obj.get_body_argument("password", None, strip=True)
        query_sql = "select username, phone, email from haircut_user where username=%s and password=%s limit 0, 1"
        if not all((username, password)):
            data = {
                "status": 1001,
                "msg": "params recv error you should user Content-Type ->"
                       " application/x-www-form-urlencoded"}
            return obj.write(data)
        result = await TorMysqlHelp.query_one_execute(query_sql, [username, SecretPwd.encode(password)], to_dict=True)
        if result:
            token = token_class.create_token(result, interval=6, expire_time=TOKEN_EXPIRE_TIME)
            data = {
                "status": 1000,
                "msg": "登陆成功",
                "username": username,
                "token": token,
                "expire": TOKEN_EXPIRE_TIME
            }
            return obj.write(data)
        return obj.write({"status": 1003, "errorMsg": "账号或密码错误"})


class Register(object):
    """
    注册会员
    """

    async def get(self, obj):
        if obj.auth:
            return obj.redirect("/haircut/index")
        if obj.is_ajax():
            result = await async_open(obj.get_template_path(), 'base.html')
            obj.STRING_DICT['@hairCutBaseTitle'] = "注册"
            return obj.finish(obj.replace_string(result, obj.STRING_DICT))
        return obj.write({"status": 1000})

    async def post(self, obj):
        if obj.auth:
            return obj.write({"status": 1006, "errorMsg": "请先退出登陆"})
        username = obj.get_body_argument("username", None, strip=True)
        password = obj.get_body_argument("password", None, strip=True)
        re_password = obj.get_body_argument("re_password", None, strip=True)
        email = obj.get_body_argument("email", None, strip=True)
        phone = obj.get_body_argument("phone", None, strip=True)
        question = obj.get_body_argument("question", None, strip=True)
        answer = obj.get_body_argument("answer", None, strip=True)
        balance = obj.get_body_argument("balance", 0, strip=True)
        if not isinstance(balance, int):
            try:
                balance = int(balance)
            except ValueError:
                return obj.write({"status": 1001, "errorMsg": "数据不完整"})
        if re_password != password:
            return obj.write({"status": 1001, "errorMsg": "两次密码不一致"})
        if not all((username, password, re_password, email, phone)):
            return obj.write({"status": 1001, "errorMsg": "数据不完整"})
        if not check_email(email):
            return obj.write({"status": 1001, "errorMsg": "邮箱不正确"})
        commit_sql = """
        insert into haircut_user(username, password, email, phone, balance) values (%s, %s, %s, %s, %s)
        """

        if not phone.isdecimal() and len(phone) != 11:
            return obj.write({"status": 1001, "errorMsg": "手机号不对"})

        if len(password) < 6:
            return obj.write({"status": 1001, "errorMsg": "密码太短"})
        if password.isdecimal():
            return obj.write({"status": 1001, "errorMsg": "密码不能全是数字"})

        arg = [username, SecretPwd.encode(password), email, phone, balance]
        if question:
            if not answer:
                return obj.write({"status": 1002, "errorMsg": "answer 为空"})
            commit_sql = commit_sql.replace(") values (", ", question, answer) values (%s, %s,")
            arg.append(question)
            arg.append(answer)

        query_sql = "select username, phone from haircut_user where username=%s or phone=%s"
        result = await TorMysqlHelp.query_one_execute(query_sql, [username, phone])
        if result:
            return obj.write({"status": 1003, "errorMsg": "手机号或用户名已经存在"})
        await TorMysqlHelp.commit_one_execute(commit_sql, arg)
        return obj.write({"status": 1000, "data": {}, "msg": "注册成功", "href": obj.reverse_url("account", "login")})


class Modify(object):
    """
    修改密码
    """

    async def get(self, obj):

        if not obj.auth:
            return obj.redirect("/account/login")

        if obj.is_ajax():
            result = await async_open(obj.get_template_path(), 'base.html')
            obj.STRING_DICT['@hairCutBaseTitle'] = "修改密码"
            return obj.finish(obj.replace_string(result, obj.STRING_DICT))

        return obj.write({"status": 1000})

    async def post(self, obj):
        if not obj.auth:
            return obj.write({"status": 1006, "errorMsg": "请先登陆"})
        username = obj.user['username']
        password = obj.get_body_argument("password", None, strip=True)
        new_password = obj.get_body_argument("new_password", None, strip=True)
        re_password = obj.get_body_argument("re_password", None, strip=True)
        email = obj.get_body_argument("email", None, strip=True)
        phone = obj.get_body_argument("phone", None, strip=True)
        if new_password != re_password or not all((new_password, re_password)):
            return obj.write({"status": 1001, "errorMsg": "两次密码不一致"})
        if not password or password == new_password:
            return obj.write({"status": 1001, "errorMsg": "密码不能为空或与原来的一致"})

        if len(new_password) < 6:
            return obj.write({"status": 1001, "errorMsg": "密码长度太短"})
        elif new_password.isdecimal():
            return obj.write({"status": 1002, "errorMsg": "密码为纯数字"})
        sql = "select id, username from haircut_user where username=%s and password=%s"
        result = await TorMysqlHelp.query_one_execute(sql, [username, SecretPwd.encode(password)], to_dict=True)
        if not result:
            return obj.write({"status": 1004, "errorMsg": "密码错误"})
        com_sql = f"update haircut_user set password=%s where id={result['id']}"
        args = [SecretPwd.encode(new_password)]
        if email:
            if not check_email(email):
                return obj.write({"status": 1005, "errorMsg": "邮箱错误"})
            com_sql = com_sql.replace("where", ", email=%s where")
            args.append(email)
        if phone:
            if not phone.isdecimal() or len(phone) != 11:
                return obj.write({"status": 1006, "errorMsg": "手机号错误"})
            com_sql = com_sql.replace("where", ", phone=%s where")
            args.append(phone)

        await TorMysqlHelp.commit_one_execute(
            com_sql, args
        )
        data = {
            "status": 1000,
            "msg": "修改成功",
            "href": obj.reverse_url("account", "login")
        }
        return obj.write(data)


class RetrievePassword(object):
    """找回密码"""

    async def get(self, obj):
        if obj.is_ajax():
            result = await async_open(obj.get_template_path(), 'base.html')
            obj.STRING_DICT['@hairCutBaseTitle'] = "找回密码"
            return obj.finish(obj.replace_string(result, obj.STRING_DICT))
        return obj.write('ok')

    async def post(self, obj):
        username = obj.get_body_argument("username", None, strip=True)
        phone = obj.get_body_argument("phone", None, strip=True)
        email = obj.get_body_argument("email", None, strip=True)
        question = obj.get_body_argument("question", None, strip=True)
        answer = obj.get_body_argument("answer", None, strip=True)
        new_password = obj.get_body_argument("new_password", None, strip=True)
        re_password = obj.get_body_argument("re_password", None, strip=True)
        if not all((new_password, re_password)) or new_password != re_password:
            return obj.write({"status": 1001, "msg": "密码错误"})
        if new_password.isdecimal():
            return obj.write({"status": 1001, "msg": "密码不能全是数字"})
        if not phone or len(phone) != 11:
            return obj.write({"status": 1001, "msg": "手机号错误"})
        result = await TorMysqlHelp.query_one_execute(
            "select id, question, answer, email, find_pwd_time from haircut_user where username=%s and phone=%s",
            [username, phone], to_dict=True)

        if not result:
            return obj.write({"status": 1001, "msg": "信息错误"})
        sql = f"update haircut_user set password=%s where id={result['id']}"
        if all((question, answer)):
            if result['question']:
                if result['question'] == question and answer == result['answer']:
                    await TorMysqlHelp.commit_one_execute(sql, [SecretPwd.encode(new_password)])
                    return obj.write({"status": 1000, 'msg': "密码修改成功"})
            return obj.write({"status": 1001, 'msg': "问题与答案不匹配"})
        if email:
            if result['email'] == email:
                from utils.asyncUtil import send_email

                token = token_class.create_token(
                    {
                        "id": result['id'],
                        "password": new_password,
                     }, expire_time=5
                )
                href = obj.reverse_url("account", "emailPassword")
                contents = [
                    f"{username} 你好",
                    f"""
                    装满一车幸福,
                    让平安开道,
                    抛弃一切烦恼
                    让快乐与你环绕
                    存储所有温暖
                    将寒冷赶跑
                    释放一生真情
                    让幸福永远对您微笑
                    
                    <div>
                        <a href="http://{obj.request.host}{href}?token={token}">邮箱验证</a>
                    </div>
                    """
                ]
                import datetime
                if result['find_pwd_time']:
                    if datetime.datetime.now() - result['find_pwd_time'] < datetime.timedelta(minutes=5):
                        return obj.write({"status": 1000, 'msg': "邮件已发送到你邮箱请查收"})
                send_email(to=[email], subject="密码找回", contents=contents)
                del send_email
                sql = f"update haircut_user set find_pwd_time=%s where id={result['id']}"

                await TorMysqlHelp.commit_one_execute(sql, [datetime.datetime.now()])
                return obj.write({"status": 1000, 'msg': "邮件已发送到你邮箱请查收"})

        return obj.write({"status": 1001, 'msg': "信息不完整"})


async def active_token(obj):
    """
    token激活
    :param obj:
    :return:
    """
    token = obj.get_argument('token', '')
    result = token_class.decode_token(token, interval=6)
    if result['ret'] == 0:
        token = token_class.create_token(result['data'], interval=6, expire_time=TOKEN_EXPIRE_TIME)
        return obj.write({"status": 1000, 'token': token, "expire": TOKEN_EXPIRE_TIME})
    else:
        return obj.write({"status": 1001, 'errorMsg': result['msg']})


async def email_to_password(obj):
    """
    email修改账号密码
    :param obj:
    :return:
    """
    token = obj.get_argument('token', '')
    result = token_class.decode_token(token)
    if result['ret'] == 0:
        await TorMysqlHelp.commit_one_execute(
            f"update haircut_user set password=%s where id=%s",
            [SecretPwd.encode(result['data']['password']), result['data']['id']]
        )
        return obj.write("<h1>密码修改成功</h1>")
    else:
        return obj.write(f"<h1>{result['msg']}</h1>")
