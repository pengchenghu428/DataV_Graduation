#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> async
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/22 15:02
@Desc   ：
=================================================='''

import time
import asyncio


async def app_run(app):
    """
    APP启动
    :param app:
    :return:
    """
    app.run()


async def data_loader_run(data_loader):
    """
    数据加载
    :param data_loader:
    :return:
    """
    data_loader.read_data()


# 定义异步函数
async def hello():
    asyncio.sleep(1)
    print('Hello World:%s' % time.time())


def run():
    for i in range(5):
        loop.run_until_complete(hello())


loop = asyncio.get_event_loop()
if __name__ =='__main__':
    run()



