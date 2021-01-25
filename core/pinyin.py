#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> pinyin
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 23:12
@Desc   ：
=================================================='''

import pypinyin


# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word, style='title'):
    res = []
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        cur = ''.join(i)
        if style == 'title':
            cur = cur.title()

        res.append(cur)
    return ' '.join(res)
