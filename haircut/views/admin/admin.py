# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: admin.py
# Month: 七月
# time: 2020/7/20 19:17
# noqa
""" Write an introduction to the module here """
import json
from abc import ABC
from utils.tormHelp import TorMysqlHelp
from settings.config import TABLE_NAME
from utils.asyncOpenFile import async_open
from haircut.BaseRequestHandler import BaseRequestHandler
from utils.asyncUtil import logger
from utils.secretPwd import SecretPwd
from utils.CustomPage import CustomPage
from utils.DecimalDatetimeEncoder import new_format_encoder


class CssHandler(object):

    async def get(self, method, admin, render=False):
        res = await async_open(admin.settings['static_path'], method, 'x-admin', 'css')
        return res


class HtmlHandler(object):

    async def get(self, method, admin, render=False, params=None):
        if render:
            if params:
                return admin.render(f'admin/{method}', **params)
            return admin.render(f'admin/{method}')
        res = await async_open(admin.get_template_path(), method, 'admin')

        # res = res[res.find("<body>"): res.rfind("</body>")+len('</body>')]
        return admin.finish(res)


css = CssHandler()
html = HtmlHandler()


class AdminHandler(BaseRequestHandler, ABC):

    def __init__(self, *args, **kwargs):
        super(AdminHandler, self).__init__(*args, **kwargs)

    async def get(self, method: str, **kwargs):

        if self.auth:
            if method == 'index' or method == 'index.html':
                data = {
                    "username": self.user['username']
                }
                return await self.render(f'admin/index.html', **data)
            elif method.endswith('.html'):
                return await html.get(method, self, render=True)
            elif '_change_' in method:
                html_str, params = method.split("_change_")
                try:
                    param = params.split('_')
                    data = {"user_edit": {
                        "username": param[0],
                        "phone": param[1],
                        "address": param[2],
                        "id": param[3],
                        "email": param[4],
                    }}
                except Exception:
                    return

                return await html.get(html_str, self, render=True, params=data)
        else:
            return self.redirect('/haircut/admin/login.html')

    def set_default_headers(self) -> None:

        super().set_default_headers()
        self.set_header('Content-Type', 'text/html;charset=utf-8')


class AdminLoginHandler(BaseRequestHandler, ABC):
    """
    登陆
    """

    def __init__(self, *args, **kwargs):
        super(AdminLoginHandler, self).__init__(*args, **kwargs)

    async def get(self, *args, **kwargs):
        if not self.auth:
            return await html.get('login.html', self, render=True)
        else:
            return self.redirect(self.reverse_url('admin', 'index'))

    async def post(self, *args, **kwargs):
        return self.write('ok')

    def set_default_headers(self) -> None:

        super().set_default_headers()
        self.set_header('Content-Type', 'text/html;charset=utf-8')


class AdminAsyncDataHandler(BaseRequestHandler, ABC):

    async def get(self, method, table, **kwargs):
        data = {"status": 1001, "msg": ""}
        if self.auth:

            if hasattr(self, method):
                fn = await getattr(self, method)(table, data)
                return fn
        return self.write(data)

    async def post(self, method, table, **kwargs):
        data = {"status": 1001, "msg": ""}
        if self.auth:
            if hasattr(self, method):
                fn = await getattr(self, method)(table, data)
                return fn
        return self.write(data)

    async def page(self, table, data):
        """
        分页
        :param table:
        :param data:
        :return:
        """
        res = await self.dispatch(table, data, "page")
        return self.write(res)

    async def edit(self, table, data):
        res = await self.dispatch(table, data, "edit")
        return self.write(res)

    async def dispatch(self, table, data, fun_name, *args, **kwargs):
        table_name = TABLE_NAME.get(table)
        if not table_name:
            return data
        res = await getattr(self, f"{table_name}_{fun_name}")(*args, **kwargs)
        return res

    async def haircut_user_page(self):

        admin = self.get_body_argument('admin', '')
        if admin and self.user['role'] == 1:
            base_where = "role = 1"
        else:
            base_where = "role <> 1"

        sql = f"select id, username, email, " \
              f"phone, address, stop, balance, " \
              f"create_time from haircut_user where {base_where}"
        args = []

        p = self.get_query_argument('page', default="1")
        per = self.get_query_argument('per', None)
        username = self.get_query_argument('username', None)
        start = self.get_query_argument('start', None)
        end = self.get_query_argument('end', None)
        up = self.get_query_argument('up', None)
        lw = self.get_query_argument('lw', None)

        count_sql = f'select count(1) from haircut_user where {base_where} '
        if username:
            sql += f" and username like %s "
            count_sql += f" and username like %s "
            args.append(f"{username}%")
        if start:
            sql += f" and create_time >= %s "
            count_sql += f"and create_time >= %s "
            args.append(start)
        if end:
            sql += f" and create_time <= %s "
            count_sql += f"and create_time <= %s "
            args.append(end)
        num = await TorMysqlHelp.query_one_execute(count_sql, args)
        par_dict = dict(self.request.query_arguments)
        par_dict.pop('up', '')
        par_dict.pop('lw', '')
        par_dict.pop('per', '')
        cus_page = CustomPage(
            url='',
            all_count=num[0] if num else 0,
            current_page=p,
            show_page_info=6,
            show_page=3,
            params=par_dict,
            return_url=True,
            flag=True
        )
        revers = False
        if cus_page.current_page > 3 and per:
            if up:
                args.append(up)
                sql += f" and id > %s"
            elif lw:
                args.append(lw)
                sql += f" and id < %s order by id desc "
                revers = True
                # sql = f"select id, username, email, phone, address, stop from ({sql}) as b order by id asc"
            sql += f" limit 0, {cus_page.end_info - cus_page.start_info}"

        else:
            sql += f" limit {cus_page.start_info}, {cus_page.end_info - cus_page.start_info}"
        print(sql % tuple(args))
        info = await TorMysqlHelp.query_all_execute(sql, args, to_dict=True)
        pagers = cus_page.pager()
        if revers:
            lw = info[-1]['id'] if info else 1
            up = info[0]['id'] if info else 1
        else:
            lw = info[0]['id'] if info else 1
            up = info[-1]['id'] if info else 1
        if len(info) > 0:
            data = {
                "data": info,
                "msg": "ok",
                "status": 1000,
                "pager": list(map(lambda x: (x[0].replace(f'?page={x[1]}', ''), x[1]), pagers[1:-1])),
                "pagerEnd": pagers[-1][0].replace("?page=", ''),
                "lw": lw,
                "up": up,
                "current_page": cus_page.current_page
            }
            del pagers
            return json.dumps(data, cls=new_format_encoder("%Y-%m-%d"))
        return {"status": 1001, 'msgError': "no data"}

    async def haircut_user_edit(self):
        email = self.get_body_argument("email", '')
        phone = self.get_body_argument("phone", '')
        address = self.get_body_argument("address", '')
        password = self.get_body_argument("password", '')
        update_id = self.get_body_argument("update_id", '')
        sql = ""
        args = []
        if not update_id:
            return {"status": 1004, "msgError": "信息不完整"}
        if email:
            from utils.CheckEmail import check_email
            if not check_email(email):
                return {"status": 1001, "msgError": "邮箱错误"}
            sql = 'update haircut_user set email=%s '
            args.append(email)
        if phone:
            if not phone.isdecimal() or len(phone) != 11:
                return {"status": 1002, "msgError": "手机号错误"}
            if not sql:
                sql = 'update haircut_user set phone=%s '
            else:
                sql += ', phone=%s '
            args.append(phone)
        if address:
            if not sql:
                sql = 'update haircut_user set address=%s '
            else:
                sql += ', address=%s '
            args.append(address)
        if not password:
            return {"status": 1003, "msgError": "密码不对"}
        if sql:
            sql += " where id=%s"
            args.append(update_id)
            user = self.user
            exist = await TorMysqlHelp.query_one_execute(
                    f"SELECT id FROM `haircut_user` WHERE `username` = "
                    f"'{user['username']}' AND `password` = %s and role = 1",
                    SecretPwd.encode(password))
            if not exist:
                return {"status": 1004, "msgError": "密码错误"}
            res = await TorMysqlHelp.update_execute(sql, args)
            if res:
                return {"status": 1000, "msg": "成功"}

        return {"status": 1004, "msgError": "信息不完整"}

    async def haircut_user_add(self):
        return self.write('ok')

    async def haircut_user_delete(self):
        return self.write('ok')


class DisableUserHandler(BaseRequestHandler, ABC):

    async def post(self, *args, **kwargs):
        if self.auth:
            data = json.loads(self.request.body)
            user_id = data['user_id']
            admin = data.get('admin')
            if admin and self.user['role'] == 1:
                sql = f"update haircut_user set stop=%s where role = 1 and id=%s"
            else:
                sql = f"update haircut_user set stop=%s where role <> 1 and id=%s"
            if user_id and data.get('stop', False) is True:
                await TorMysqlHelp.commit_one_execute(sql, [1, user_id])
                return self.write({'status': 1000, 'msg': 'ok'})
            elif user_id and data.get('stop', False) is False:
                await TorMysqlHelp.commit_one_execute(sql, [0, user_id])
                return self.write({'status': 1000, 'msg': 'ok'})
        return self.write({'status': 1001, 'msg': 'error'})
