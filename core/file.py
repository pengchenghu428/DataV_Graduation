#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> file
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 20:39
@Desc   ：本脚本处理和文件相关
=================================================='''

import os


def check_directory(tdir):
    """
    确保文件夹存在
    :param tdir:文件/文件夹目录
    :return:
    """
    dirs = tdir.split('/')
    if '.' in dirs[-1]:
        dirs.pop(-1)

    tdir = '/'.join(dirs)

    if not os.path.exists(tdir):
        os.makedirs(tdir)


def dir_exist(tdir):
    """
    检查文件是否存在
    :param tdir: 文件/文件夹目录
    :return:
    """
    return os.path.exists(tdir)