#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> match
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/22 12:01
@Desc   ：
=================================================='''


def match_screen_title(mode, name):
    """
    数据大屏页面标题匹配
    :param mode: 模式
    :param name: 名字
    :return:
    """
    if mode == 'nation':
        return "全国", ""

    if mode == "type":
        return "", name

