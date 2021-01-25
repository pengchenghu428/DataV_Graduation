#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> datetime
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/22 14:55
@Desc   ：
=================================================='''

import time, datetime


def get_current_sdt():
    """
    获取当前格式化时间
    :return:
    """
    datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return datetime

