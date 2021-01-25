#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> myTab
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/24 11:56
@Desc   ：
=================================================='''
import datetime
import simplejson as json
from pyecharts.commons import utils
from pyecharts.charts import Tab
from pyecharts.types import Sequence
from pyecharts.options.series_options import BasicOpts

class myTab(Tab):

    # def __init__(self):
    #     super()
    def get_options(self) -> dict:
        return utils.remove_key_with_none_value(self.options)

    def dump_options(self) -> str:
        return utils.replace_placeholder(
            json.dumps(self.get_options(), indent=4, default=default, ignore_nan=True)
        )

    def dump_options_with_quotes(self) -> str:
        return utils.replace_placeholder_with_quotes(
            json.dumps(self.get_options(), indent=4, default=default, ignore_nan=True)
        )

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, utils.JsCode):
        return (
            o.replace("\\n|\\t", "").replace(r"\\n", "\n").replace(r"\\t", "\t").js_code
        )
    if isinstance(o, BasicOpts):
        if isinstance(o.opts, Sequence):
            return [utils.remove_key_with_none_value(item) for item in o.opts]
        else:
            return utils.remove_key_with_none_value(o.opts)