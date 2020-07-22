from urllib.parse import urlencode


class CustomPage(object):
    """
    自定义分页
    all_count = queryset.count()
    url = request.path_info
    lists = queryset[fin_ye.start_info: fin_ye.end_info]
    :return render(request, 'xxx.html', {"lists": lists, "html_pager":self.pager()})
    """

    def __init__(self,
                 url,
                 all_count,
                 current_page,
                 params='',
                 add_params=None,
                 page="page",
                 show_page_info=10,
                 show_page=11,
                 page_stylesheet_path=None,
                 return_url=False,
                 flag=True):
        """

        :param url:
        :param all_count:
        :param current_page:
        :param params:
        :param add_params: dict
        :param page: 页码的 key example page=1
        :param show_page_info:
        :param show_page:
        :param page_stylesheet_path:
        :param flag: 是否生成html标签
        """
        if not all_count:
            all_count = 1
        self.all_count = all_count  # 所有信息数据
        self.ShowPageInfo = show_page_info  # 每页展示信息数目
        self.ShowPage = show_page  # 展示页数
        self.url = url
        # params  # 查询参数   {"a": 1, "page": 2}
        self.page = page  # "get中的查询参数"
        try:
            self.current_page = int(current_page)  # 当前页
            if self.current_page == 0:
                self.current_page = 1
        except Exception as E:
            self.current_page = 1
        self._search_param = ''
        self.return_url = return_url  # 返回解析后的url (url, page)
        if params:
            for p in params:
                if p == self.page:
                    continue
                if isinstance(add_params, dict):
                    add_p = add_params.get(p, None)
                    if add_p:
                        add_params.pop(add_p, None)
                try:
                    for i in params.getlist(p):  # noqa
                        self._search_param += f"&{p}={i}"
                except:
                    pars = params.get(p)  # noqa
                    if isinstance(pars, list):
                        for i in pars:
                            if isinstance(i, bytes):
                                i = i.decode('utf8')
                            self._search_param += f"&{p}={i}"
                    else:
                        self._search_param += f"&{p}={pars}"
        if add_params and isinstance(add_params, dict):
            self._search_param += "&" + urlencode(add_params)
        self.flag = flag
        self.pagestylesheet_path = page_stylesheet_path
        all_page, b = divmod(all_count, show_page_info)
        if b:
            all_page += 1

        self.all_page = all_page  # 总页数

    @property
    def start_info(self):
        """

        :return:
        """
        start = (self.current_page - 1) * self.ShowPageInfo
        return start

    @property
    def end_info(self):
        """

        :return:
        """
        end = self.current_page * self.ShowPageInfo
        return end

    def pager(self):
        """

        :return:
        """

        row = self.ShowPage // 2

        # 如果总页数小于 11 页 有多少页就展示多少页
        if self.all_page < self.ShowPage:
            start_page = 1
            end_page = self.all_page
        else:

            # 如果当前页的前5页有负数 展示 1 到11 页
            if self.current_page - row <= 0:
                start_page = 1
                end_page = self.ShowPage
            else:
                # 如果当前页的后5 页大于总页数 展示最后的11页
                if self.current_page + row > self.all_page:
                    start_page = self.all_page - self.ShowPage + 1
                    end_page = self.all_page
                else:
                    # 展示当前页的前5 页和后5 页页码
                    start_page = self.current_page - row
                    end_page = self.current_page + row

        user_list = list()
        if self.flag:
            """
            页面用法
            <nav aria-label="Page navigation">
              <ul class="pagination">
                  user_list 写这里
              </ul>
            </nav>

            """
            if self.pagestylesheet_path:
                strn = """<link rel="stylesheet" href="%s">""" % self.pagestylesheet_path
                user_list.append(strn)
            prev_next = """ <li>
                                <a href="{}?{}={}{}" aria-label="{}">
                                    <span aria-hidden="true">{}</span>
                                </a>
                             </li>
                    """
            head_page = """
                            <li>
                                <a href='{}?{}=1{}'>首页</a>
                            </li>""".format(self.url, self.page, self._search_param)
            last_page = """
                            <li>
                                <a href='{1}?{2}={0}{3}'>尾页</a>
                            </li>""".format(self.all_page, self.url, self.page, self._search_param)
            user_list.append(head_page)
            if self.current_page - 1 > 0:
                user_list.append(prev_next.format(
                    self.url, self.page, self.current_page - 1, self._search_param, 'Previous', '&laquo;'))
            else:
                user_list.append(prev_next.format(self.url, self.page, 1, self._search_param, 'Previous', '&laquo;'))

            for i in range(start_page, end_page + 1):
                if i == self.current_page:
                    #  <li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>
                    user_a = """
                                <li class="active">
                                    <a href='{1}?{2}={0}{3}'>{0}</a>
                                </li>""".format(i, self.url, self.page, self._search_param)
                    # < li > < a href = "#" > 1 < / a > < / li >
                else:
                    user_a = """
                                <li>
                                    <a href='{1}?{2}={0}{3}'>{0}</a>
                                </li>""".format(i, self.url, self.page, self._search_param)
                user_list.append(user_a)

            if self.current_page + 1 <= self.all_page:
                user_list.append(prev_next.format(self.url, self.page, self.current_page + 1, self._search_param, 'Next', '&raquo;'))
            else:
                user_list.append(prev_next.format(self.url, self.page, self.all_page, self._search_param, 'Next', '&raquo;'))
            user_list.append(last_page)
            if self.return_url and self.flag:
                import re
                new_list = []
                reg = re.compile(r"<a href='(.*?)'>(.*?)</a>")
                for u in user_list:
                    new_list.extend(re.findall(reg, u))
                return new_list

        else:
            for i in range(start_page, end_page + 1):
                user_list.append(i)
            return user_list
        return '\n'.join(user_list)