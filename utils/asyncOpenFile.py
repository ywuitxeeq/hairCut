# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: asyncOpenFile.py
# Month: 七月
# time: 2020/7/17 21:48
# noqa
""" Write an introduction to the module here """
import aiofiles
import os


async def async_open(template_path, filename, *args):
    async with aiofiles.open(os.path.join(template_path, *args, filename), mode='r', encoding="utf8") as f:
        contents = await f.read()
    return contents

