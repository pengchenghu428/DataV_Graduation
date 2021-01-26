#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> decode
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/26 17:42
@Desc   ：
=================================================='''

from urllib.parse import unquote


def url_decode(s):
    return unquote(s)


