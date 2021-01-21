#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> data
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 20:39
@Desc   ：本脚本处理和数据相关
=================================================='''

import pandas as pd
from collections import defaultdict

class DataLoader:
    def __init__(self, pdir):
        self.pdir = pdir

        self.data = defaultdict(dict)

    def read_data(self):
        # 读取 sales 数据
        sales_nation_year_df = pd.read_csv('{}/sales_nation_year.csv')
        sales_nation_month_df = pd.read_csv('{}/sales_nation_month.csv')
        sales_type_year_df = pd.read_csv('{}/sales_nation_year.csv')
        sales_type_month_df = pd.read_csv('{}/sales_nation_month.csv')
        sales_province_year_df = pd.read_csv('{}/sales_nation_year.csv')
        sales_company_year_df = pd.read_csv('{}/sales_nation_year.csv')
        sales_company_month_df = pd.read_csv('{}/sales_nation_month.csv')

        # 读取保有量数据
        own_nation_year_df = pd.read_csv('{}/own_nation_year.csv')

        # 读取宏观数据
        macro_nation_year_df = pd.read_csv('{}/macro_nation_year.csv')
        macro_province_year_df = pd.read_csv('{}/macro_province_year.csv')

        # 读取房地产数据
        realty_nation_year_df = pd.read_csv('{}/realty_nation_year.csv')
        realty_nation_month_df = pd.read_csv('{}/realty_nation_month.csv')
        realty_province_year_df = pd.read_csv('{}/realty_province_year.csv')
        realty_province_month_df = pd.read_csv('{}/realty_province_month.csv')

        # 财政支出数据
        finance_nation_year_df = pd.read_csv('{}/finance_nation_year.csv')
        finance_province_year_df = pd.read_csv('{}/finance_province_year.csv')

        # 数据拼接
        self.data['nation']['year']
        self.data['nation']['month']


    def get_data(self, mode, time_dimension, name):
        """
        获取对应数据
        :param mode: nation/type/province/company
        :param name:
        :param time_dimension: year/month
        :return:
        """
        assert mode in ['nation', 'type', 'province', 'company'], "DataLoader: 出现非法的MODE"


        tdf = self.data[mode][time_dimension]

        return tdf.loc[tdf[mode]==name] if mode != 'nation' else tdf


# 一阶差分特征提取
def diff_feats(tdf, levels=None, key=['year'], drop=False, avoid_cols=[]):
    tdf.sort_values(key, inplace=True)  # 按照key排序

    # 一阶差分处理核心
    def core(tdf):
        for col in tdf.columns:
            if col not in ['year', 'month', 'type', 'province', 'company']:  # 非时间列
                tdf['{}_diff_1'.format(col)] = tdf[col].diff(1)  # 差分

                if drop and col not in avoid_cols:  # 是否删除原有列
                    tdf.drop(col, inplace=True, axis=1)
        return tdf

    if not levels:
        tdf = core(tdf)
    else:
        dfs = []
        for name, df in tdf.groupby(levels):
            dfs.append(core(df))
        tdf = pd.concat(dfs, ignore_index=True)

    return tdf