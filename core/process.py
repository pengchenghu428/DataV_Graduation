#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> process
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 21:25
@Desc   ：本文件处理数据处理相关
=================================================='''

import pandas as pd
import numpy as np
from core.pinyin import pinyin

# 全国年销量数据处理与拼接
# def extend_merge_nation_year(sales_df, own_df, macro_df, realty_df, finance_df):
def extend_merge_nation_year(dfs):
    print(len(dfs))
    sales_df, own_df, macro_df, realty_df, finance_df = dfs
    sales_df = diff_feats(sales_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    own_df = diff_feats(own_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    macro_df = diff_feats(macro_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    realty_df = diff_feats(realty_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    finance_df = diff_feats(finance_df, levels=None, key=['year'], drop=False, avoid_cols=[])

    tdf = sales_df.copy()
    for df in [own_df, macro_df, realty_df, finance_df]:
        tdf = tdf.merge(df, on='year', how='left')

    tdf['target'] = tdf['sales'].shift(-1)  # 标签构建
    tdf.sort_values(['year'], inplace=True, ignore_index=True)
    return tdf


# 全国月销量数据处理与拼接
def extend_merge_nation_month(dfs):
# def extend_merge_nation_month(sales_df, own_df, macro_df, realty_year_df, realty_month_df, finance_df):
    sales_df, own_df, macro_df, realty_year_df, realty_month_df, finance_df = dfs
    lags = 3
    sales_df = extract_seq_feat(sales_df, 'sales', lags=lags)  # 序列特征抽取
    own_df = diff_feats(own_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    own_df['year'] = own_df['year'].shift(-1)  # 拼接上一年的数据
    macro_df = diff_feats(macro_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    macro_df['year'] = macro_df['year'].shift(-1)  # 拼接上一年的数据
    realty_year_df = diff_feats(realty_year_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    realty_year_df['year'] = realty_year_df['year'].shift(-1)  # 拼接上一年的数据
    realty_month_df = diff_feats(realty_month_df, levels=None, key=['year', 'month'], drop=False, avoid_cols=[])
    finance_df = diff_feats(finance_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    finance_df['year'] = finance_df['year'].shift(-1)  # 拼接上一年的数据

    tdf = sales_df.copy()
    for df in [own_df, macro_df, realty_year_df, realty_month_df, finance_df]:
        tdf = tdf.merge(df, on='year', how='left')

    tdf.sort_values(['year'], inplace=True, ignore_index=True)
    tdf['target'] = tdf['sales'].shift(-1)  # 标签构建
    return tdf


# 分类型年销量数据处理与拼接
def extend_merge_type_year(dfs):
# def extend_merge_type_year(sales_nation_df, sales_type_df, own_df, macro_df, realty_df, finance_df):
    sales_nation_df, sales_type_df, own_df, macro_df, realty_df, finance_df = dfs
    sales_nation_df = diff_feats(sales_nation_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    sales_type_df = diff_feats(sales_type_df, levels='type', key=['year'], drop=False, avoid_cols=[])
    own_df = diff_feats(own_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    realty_df = diff_feats(realty_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    finance_df = diff_feats(finance_df, levels=None, key=['year'], drop=False, avoid_cols=[])

    trn_df = sales_type_df.merge(sales_nation_df, on='year', how='left', suffixes=('', '_nation'))
    trn_df = merge_data(trn_df, [own_df, macro_df, realty_df, finance_df])
    trn_df.sort_values(['year', 'type'], inplace=True, ignore_index=True)
    trn_df['target'] = trn_df['sales'].shift(-3)  # 标签构建
    trn_df.fillna(trn_df.mean(), inplace=True)
    return trn_df


# 分类型月销量数据处理与拼接
def extend_merge_type_month(dfs):
# def extend_merge_type_month(sales_nation_year_df, sales_nation_month_df, sales_type_year_df, sales_type_month_df,
#                             own_df, macro_df, realty_year_df, realty_month_df, finance_df):
    sales_nation_year_df, sales_nation_month_df, sales_type_year_df, sales_type_month_df,\
            own_df, macro_df, realty_year_df, realty_month_df, finance_df = dfs
    # 销售序列特征提取
    sales_nation_year_df = diff_feats(sales_nation_year_df, key=['year'], drop=False)  # 年
    sales_type_year_df = diff_feats(sales_type_year_df, levels='type', key=['year'], drop=False)  # 类型-年
    sales_nation_month_df = extract_seq_feats(sales_nation_month_df, 'sales', lags=12, levels='')
    sales_type_month_df = extract_seq_feats(sales_type_month_df, 'sales', lags=12, levels='type')

    # 其他通用特征
    own_df = diff_feats(own_df, key=['year'], drop=True)
    own_df['year'] = own_df['year'].shift(-1)
    macro_df = diff_feats(macro_df, key=['year'], drop=True)
    macro_df['year'] = macro_df['year'].shift(-1)
    realty_year_df = diff_feats(realty_year_df, key=['year'], drop=True, avoid_cols=[])
    realty_year_df['year'] = realty_year_df['year'].shift(-1)
    realty_month_df = diff_feats(realty_month_df, key=['year', 'month'], drop=True,
                                 avoid_cols=['roadwork_area_rise', 'new_area_rise', 'complete_area_rise'])
    finance_df = diff_feats(finance_df, key=['year'], drop=True, avoid_cols=[])
    finance_df['year'] = finance_df['year'].shift(-1)

    # 数据拼接
    trn_df = sales_type_month_df.copy()
    trn_df = trn_df.merge(sales_nation_year_df, on='year', how='left', suffixes=('', '_year'))
    trn_df = trn_df.merge(sales_type_year_df, on=['year', 'type'], how='left', suffixes=('', '_year_type'))
    trn_df = trn_df.merge(sales_nation_month_df, on=['year', 'month'], how='left', suffixes=('', '_nation_month'))
    trn_df = trn_df.merge(own_df, on='year', how='left')
    trn_df = trn_df.merge(macro_df, on='year', how='left')
    trn_df = trn_df.merge(realty_year_df, on='year', how='left')
    trn_df = trn_df.merge(realty_month_df, on=['year', 'month'], how='left')
    trn_df = trn_df.merge(finance_df, on=['year'], how='left')

    trn_df = extract_dt_feats(trn_df)

    trn_df.sort_values(['year', 'month', 'type'], inplace=True, ignore_index=True)
    trn_df['target'] = trn_df['sales'].shift(-3)  # 标签构建
    return trn_df


# 分省市年销量数据处理与拼接
def extend_merge_province_year(dfs):
# def extend_merge_province_year(sales_nation_year_df, sales_province_year_df, own_df, macro_nation_df, macro_province_df,
#                                realty_nation_df, realty_province_df, finance_nation_df, finance_province_df):
    sales_nation_year_df, sales_province_year_df, own_df, macro_nation_df, macro_province_df, \
        realty_nation_df, realty_province_df, finance_nation_df, finance_province_df = dfs
    # 数据差分
    sales_nation_year_df = diff_feats(sales_nation_year_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    sales_province_year_df = diff_feats(sales_province_year_df, levels='province', key=['year'], drop=False,
                                        avoid_cols=[])
    own_df = diff_feats(own_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    macro_nation_df = diff_feats(macro_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    macro_province_df = diff_feats(macro_province_df, levels='province', key=['year'], drop=True, avoid_cols=[])
    realty_nation_df = diff_feats(realty_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    realty_province_df = diff_feats(realty_province_df, levels='province', key=['year'], drop=True, avoid_cols=[])
    finance_nation_df = diff_feats(finance_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    finance_province_df = diff_feats(finance_province_df, levels='province', key=['year'], drop=True, avoid_cols=[])

    # 数据拼接
    sales_df = pd.merge(left=sales_province_year_df, right=sales_nation_year_df, on=['year'], how='left',
                        suffixes=('', '_nation'))
    macro_df = pd.merge(left=macro_province_df, right=macro_nation_df, on=['year'], how='left',
                        suffixes=('', '_nation'))
    realty_df = pd.merge(left=realty_province_df, right=realty_nation_df, on=['year'], how='left',
                         suffixes=('', '_nation'))
    finance_df = pd.merge(left=finance_province_df, right=finance_nation_df, on=['year'], how='left',
                          suffixes=('', '_nation'))
    trn_df = sales_df.copy()
    trn_df = trn_df.merge(own_df, on=['year'], how='left')
    trn_df = trn_df.merge(macro_df, on=['year', 'province'], how='left')
    trn_df = trn_df.merge(realty_df, on=['year', 'province'], how='left')
    trn_df = trn_df.merge(finance_df, on=['year', 'province'], how='left')

    # 构建标签
    trn_df['target'] = trn_df.groupby('province')['sales'].shift(-1)
    trn_df.sort_values(['year', 'province'], inplace=True, ignore_index=True)
    return trn_df


# 分公司年销量数据处理与拼接
def extend_merge_company_year(dfs):
# def extend_merge_company_year(sales_nation_year_df, sales_company_year_df, own_df,
#                               macro_nation_df, realty_nation_df, finance_nation_df):
    sales_nation_year_df, sales_company_year_df, own_df,\
        macro_nation_df, realty_nation_df, finance_nation_df = dfs
    # 数据差分
    sales_nation_year_df = diff_feats(sales_nation_year_df, levels=None, key=['year'], drop=False, avoid_cols=[])
    sales_company_year_df = diff_feats(sales_company_year_df, levels='company', key=['year'], drop=False, avoid_cols=[])
    own_df = diff_feats(own_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    macro_nation_df = diff_feats(macro_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    realty_nation_df = diff_feats(realty_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])
    finance_nation_df = diff_feats(finance_nation_df, levels=None, key=['year'], drop=True, avoid_cols=[])

    # 数据拼接
    sales_df = pd.merge(left=sales_company_year_df, right=sales_nation_year_df, on=['year'], how='left',
                        suffixes=('', '_nation'))
    macro_df = macro_nation_df
    realty_df = realty_nation_df
    finance_df = finance_nation_df
    trn_df = sales_df.copy()
    trn_df = trn_df.merge(own_df, on=['year'], how='left')
    trn_df = trn_df.merge(macro_df, on=['year'], how='left')
    trn_df = trn_df.merge(realty_df, on=['year'], how='left')
    trn_df = trn_df.merge(finance_df, on=['year'], how='left')

    # 构建标签
    trn_df['target'] = trn_df.groupby('company')['sales'].shift(-1)
    trn_df.sort_values(['year', 'company'], inplace=True, ignore_index=True)
    return trn_df


# 分公司月销量数据处理与拼接
def extend_merge_company_month(dfs):
# def extend_merge_company_month(sales_nation_year_df, sales_nation_month_df, sales_type_year_df, sales_type_month_df,
#                               sales_company_year_df, sales_company_month_df, own_df, macro_nation_df,
#                               realty_nation_year_df, realty_nation_month_df, finance_nation_df):
    sales_nation_year_df, sales_nation_month_df, sales_type_year_df, sales_type_month_df, \
        sales_company_year_df, sales_company_month_df, own_df, macro_nation_df,\
            realty_nation_year_df, realty_nation_month_df, finance_nation_df = dfs
    # 元参数
    companys = list(sales_company_month_df['company'].unique())
    company_lens = len(companys)

    # 销售序列特征提取
    lags = 12
    sales_nation_year_df = diff_feats(sales_nation_year_df, key=['year'], drop=False)  # 年
    sales_nation_year_df['year'] = sales_nation_year_df['year'].shift(-1)
    sales_type_year_df = process_sales_type_year(sales_type_year_df)
    sales_type_year_df = diff_feats(sales_type_year_df, key=['year'], drop=False)  # 类型-年
    sales_type_year_df['year'] = sales_type_year_df['year'].shift(-1)
    sales_company_year_df = diff_feats(sales_company_year_df, levels='company', key=['year'], drop=False)
    sales_company_year_df['year'] = sales_company_year_df['year'].shift(-company_lens)
    sales_nation_month_df = extract_seq_feats(sales_nation_month_df, 'sales', lags=lags, levels='')
    sales_type_month_df = process_sales_type_month(sales_type_month_df)
    sales_type_month_df = extract_seq_feats(sales_type_month_df, 'sales_Zhong', lags=lags, levels='')
    sales_type_month_df = extract_seq_feats(sales_type_month_df, 'sales_Da', lags=lags, levels='')
    sales_type_month_df = extract_seq_feats(sales_type_month_df, 'sales_Xiao', lags=lags, levels='')
    sales_company_month_df.sort_values(['year', 'month', 'company'], inplace=True)
    sales_company_month_df = extract_seq_feats(sales_company_month_df, 'sales', lags=lags, levels='company')

    # 其他通用特征
    own_df = diff_feats(own_df, key=['year'], drop=True)
    macro_df = diff_feats(macro_nation_df, key=['year'], drop=True)
    realty_year_df = diff_feats(realty_nation_year_df, key=['year'], drop=True, avoid_cols=[])
    realty_month_df = diff_feats(realty_nation_month_df, key=['year', 'month'], drop=True,
                                 avoid_cols=['roadwork_area_rise', 'new_area_rise', 'complete_area_rise'])
    finance_df = diff_feats(finance_nation_df, key=['year'], drop=True, avoid_cols=[])

    # 数据拼接
    trn_df = sales_company_month_df.copy()
    trn_df = trn_df.merge(sales_nation_year_df, on='year', how='left', suffixes=('', '_year'))
    trn_df = trn_df.merge(sales_type_year_df, on=['year'], how='left', suffixes=('', '_year_type'))
    trn_df = trn_df.merge(sales_company_year_df, on=['year', 'company'], how='left', suffixes=('', '_year_company'))
    trn_df = trn_df.merge(sales_nation_month_df, on=['year', 'month'], how='left', suffixes=('', '_nation_month'))
    trn_df = trn_df.merge(sales_type_month_df, on=['year', 'month'], how='left', suffixes=('', '_type_month'))
    trn_df = trn_df.merge(own_df, on='year', how='left')
    trn_df = trn_df.merge(macro_df, on='year', how='left')
    trn_df = trn_df.merge(realty_year_df, on='year', how='left')
    trn_df = trn_df.merge(realty_month_df, on=['year', 'month'], how='left')
    trn_df = trn_df.merge(finance_df, on=['year'], how='left')

    trn_df = extract_dt_feats(trn_df)

    trn_df['target'] = trn_df.groupby('company')[['sales']].shift(-1)  # 标签构建
    trn_df.sort_values(['year', 'month', 'company'], inplace=True)
    return trn_df


# 数据汇总
def merge_data(sdf, dfs):
    tdf = sdf.copy()

    for df in dfs:
        tdf = tdf.merge(df, on='year', how='left')
    return tdf


# 一阶差分特征提取
def diff_feats(tdf, levels=None, key=['year'], drop=False, avoid_cols=[]):
    tdf.sort_values(key, inplace=True)  # 按照key排序

    # 一阶差分处理核心
    def core(tdf):
        for col in tdf.columns:
            if col not in ['year', 'month', 'type', 'province', 'company']:  # 非时间列
                tdf.loc[tdf.index,'{}_diff_1'.format(col)] = tdf[col].diff(1).copy()  # 差分

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

# 序列特征抽取
def extract_seq_feat(tdf, col, lags=3):
    # 滞后特征
    for i in range(1, lags):
        tdf['{}_lag_{}'.format(col, i)] = tdf[col].shift(i)

    # 差分特征
    for i in range(1, lags):
        tdf['{}_diff_{}'.format(col, i)] = tdf[col].diff(i)

    # 统计特征
    cols = [col] + ['{}_lag_{}'.format(col, i) for i in range(1, lags)]
    tdf['last{}_{}_mean'.format(lags, col)] = tdf[cols].mean(axis=1)
    tdf['last{}_{}_std'.format(lags, col)] = tdf[cols].std(axis=1)
    tdf['last{}_{}_range'.format(lags, col)] = tdf[cols].max(axis=1) - tdf[cols].min(axis=1)

    # 衰减特征
    for i in range(9, 4, -1):
        pw = np.power(0.1 * i, np.arange(lags))
        colname = 'last{}_{}_pw0{}'.format(col, lags, i)
        tdf[colname] = tdf[col] * pw[0]
        for j in range(1, lags):
            tdf[colname] += tdf['{}_lag_{}'.format(col, j)] * pw[j]
    return tdf


# 滞后特征抽取
def lag_feats(df, col, lags):
    for i in range(1, lags + 1):
        df.loc[df.index, '{}_lag_{}'.format(col, i)] = df[col].shift(i).copy()
    return df


# 统计特征抽取
def win_stat_feats(df, col, lags):
    cols = [col] + ['{}_lag_{}'.format(col, i) for i in range(1, lags)]
    df['last{}_{}_mean'.format(lags, col)] = df[cols].mean(axis=1).copy()
    df['last{}_{}_std'.format(lags, col)] = df[cols].std(axis=1).copy()
    df['last{}_{}_range'.format(lags, col)] = (df[cols].max(axis=1) - df[cols].min(axis=1)).copy()
    return df


# 趋势特征抽取
def damp_feats(df, col, lags):
    # 衰减特征
    for i in range(9, 4, -1):
        pw = np.power(0.1 * i, np.arange(lags))
        colname = 'last{}_{}_pw0{}'.format(col, lags, i)
        df[colname] = (df[col] * pw[0]).copy()
        for j in range(1, lags):
            df[colname] += (df['{}_lag_{}'.format(col, j)] * pw[j]).copy()

    return df


# 交互特征
# 差分
def seq_diff_feats(df, col, order):
    for i in range(1, 1 + order):
        df['{}_diff_{}'.format(col, i)] = df[col].diff(i).copy()
    return df


# 同比、环比
def ratio_feats(df, col, peroid=12):
    df['{}_chain_relative_ratio'.format(col)] = (df['{}_diff_{}'.format(col, 1)] / df['{}_lag_{}'.format(col, 1)]).copy()
    df['{}_year_basis'.format(col)] = ((df[col] - df['{}_lag_12'.format(col)]) / df['{}_lag_12'.format(col)]).copy()
    return df


# 序列特征抽取
def extract_seq_feats(df, col, lags=12, levels=''):
    # 特征提取核心
    def core(df):
        df = lag_feats(df, col, lags)  # 滞后特征
        df = win_stat_feats(df, col, lags)  # 统计特征
        df = damp_feats(df, col, lags)  # 趋势特征
        df = seq_diff_feats(df, col, 1)  # 交互特征
        df = ratio_feats(df, col, peroid=12)  # 周期特征
        return df

    if not levels:  #
        df = core(df)
        return df

    dfs = []
    for name, tdf in df.groupby(levels):
        tdf = core(tdf)
        dfs.append(tdf)
    return pd.concat(dfs, ignore_index=True)


# 时间特征抽取
def extract_dt_feats(df):
    df['datetime'] = df[['year', 'month']].apply(lambda x: '{}-{}'.format(x[0], x[1]), axis=1)
    df['datetime'] = pd.to_datetime(df['datetime'])

    df['quarter'] = df['datetime'].dt.quarter
    df['season'] = df['month'].map(lambda x: x // 3 if x > 2 else (x + 12) // 3)
    month_to_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 30}
    df['days'] = df['month'].map(month_to_days)  # 天数
    df.loc[((df['year'] % 4 == 0) & (df['year'] % 100 != 0)) | (df['year'] % 400 == 0), 'days'] += 1

    year_to_spring_month = {2009: 1, 2010: 2, 2011: 2, 2012: 1, 2013: 2,
                            2014: 1, 2015: 2, 2016: 2, 2017: 1, 2018: 2}
    df['spring'] = df['year'].map(year_to_spring_month)
    df['spring'] = (df['month'] == df['spring']).astype(int)

    return df


# 处理类型销量月数据
def process_sales_type_year(df_):
    tdf = None

    for name, df in df_.groupby('type'):
        df['sales_{}'.format(pinyin(name))] = df['sales'].copy()
        df.drop(['sales', 'type'], inplace=True, axis=1)

        if type(tdf) != type(df):
            tdf = df
        else:
            tdf = tdf.merge(df, on=['year'], how='left')

    return tdf


# 处理类型销量月数据
def process_sales_type_month(df_):
    tdf = None

    for name, df in df_.groupby('type'):
        df['sales_{}'.format(pinyin(name))] = df['sales'].copy()
        df.drop(['sales', 'type'], inplace=True, axis=1)

        if type(tdf) != type(df):
            tdf = df
        else:
            tdf = tdf.merge(df, on=['year', 'month'], how='left')

    return tdf

