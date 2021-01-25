#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：DataV_Graduation -> plot
@IDE    ：PyCharm
@Author ：pengchenghu
@Date   ：2021/1/21 20:39
@Desc   ：本脚本处理和绘图相关
=================================================='''

import datetime
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from pyecharts.charts import Timeline, Grid
from pyecharts.charts import Page, Tab
from core.file import check_directory, dir_exist


# 年销量数据大屏图表绘制之保有量数据绘制
def plot_year_own_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    cols = ['year',
            '10year_own', '8year_own', '6year_own',
            '10year_own_diff_1', '8year_own_diff_1', '6year_own_diff_1']
    tdf = df[cols].copy()
    x_data = tdf['year'].astype(str).tolist()

    bar = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis(
            '10年',
            (tdf['10year_own'] / 10000).tolist(),
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            '8年',
            (tdf['8year_own'] / 10000).tolist(),
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            '6年',
            (tdf['6year_own'] / 10000).tolist(),
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name='保有量差分(w)',
                type_='value',
                min_=-10,
                max_=30,
                position='right')
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(
                name='保有量(w)',
                type_='value',
                min_=30,
                max_=180,
                position='left',
                splitline_opts=opts.SplitLineOpts(is_show=True)),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
            legend_opts=opts.LegendOpts(pos_top="5%")
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            '10年差分',
            (tdf['10year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
        .add_yaxis(
            '8年差分',
            (tdf['8year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
        .add_yaxis(
            '6年差分',
            (tdf['6year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            legend_opts=opts.LegendOpts(pos_top="5%")
        )
    )
    bar.overlap(line)

    return bar


# 年销量数据大屏图表绘制之房地产数据绘制
def plot_year_realty_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()
    sales = df['sales'].copy()

    # 生成价格图表
    def price_chart():
        cols = ['ave_price', 'ave_price_residence', 'ave_price_villadom',
                'ave_price_office', 'ave_price_business', 'ave_price_other']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()
        bar = (
            Bar().add_xaxis(x_data)
            .add_yaxis(
                '商品房',
                (tdf['ave_price_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            ).add_yaxis(
                '住宅',
                (tdf['ave_price_residence_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            ).add_yaxis(
                '商业营业用',
                (tdf['ave_price_business_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='单价(元/平方米)',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="均价差分"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '年销量(K)',
                (tdf['sales'] // 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
                is_smooth=True
            ).set_global_opts(
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        bar.overlap(line)
        return bar

    # 生成开发商数量占比图表
    def dev_chart():
        cols = ['dev_nation', 'dev_collectivity', 'dev_HMT', 'dev_foreign']
        names = ['国有', '集体', '港澳台', '外商']
        tdf = df[cols].copy()

        tl = Timeline()
        for idx, year in enumerate(x_data):
            data = tdf.iloc[idx].tolist()
            data = [list((name, data[i])) for i, name in enumerate(names)]

            pie = (
                Pie().add(
                    "开发商类型占比",
                    data,
                    rosetype='radius',
                    radius=["30%", "55%"],
                ).set_global_opts(
                    title_opts=opts.TitleOpts("{}房地产开发商数量".format(year)),
                    legend_opts=opts.LegendOpts(pos_top="5%")
                )
            )
            tl.add(pie, "{}年".format(year))
        return tl

    # 生成投资图表
    def investment_chart():
        cols = ['complete_investment',
                'building_investment', 'equip_investment']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        bar = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis(
                '已完成',
                (tdf['complete_investment_diff_1'] // 1000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                '建筑安装',
                (tdf['building_investment_diff_1'] // 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                '装备',
                (tdf['equip_investment_diff_1'] // 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='投资(千亿)',
                    type_='value',
                    position='right')
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right',
                    offset=50, )
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='总投资(千亿)',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="投资与销量关系"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )

        line = (
            Line()
            .add_xaxis(x_data)
            .add_yaxis(
            '年销量(K)',
                (tdf['sales'] // 1000).tolist(),
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                is_smooth=True
            ).set_global_opts(
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        bar.overlap(line)
        return bar

    # 工量情况
    def job_chart():
        cols = ['complete_area', 'complete_price', 'complete_cost']
        cols = cols + ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()
        bar = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis(
            '竣工面积',
                (tdf['complete_area'] // 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                '竣工价值',
                (tdf['complete_price_diff_1'] // 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            ).add_yaxis(
                '竣工造价',
                (tdf['complete_cost_diff_1']).tolist(),
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='价值',
                    type_='value',
                    position='right')
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='造价',
                    type_='value',
                    position='right',
                    offset=30)
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='left',
                    offset=30)
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='面积',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="工程量与销量关系"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )

        line = (
            Line()
            .add_xaxis(x_data)
            .add_yaxis(
                '年销量(K)',
                (tdf['sales'] // 1000).tolist(),
                yaxis_index=3,
                label_opts=opts.LabelOpts(is_show=False),
                is_smooth=True
            ).set_global_opts(
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        bar.overlap(line)
        return bar

    charts = {"dev": dev_chart().dump_options_with_quotes(),
              "price": price_chart().dump_options_with_quotes(),
              "investment": investment_chart().dump_options_with_quotes(),
              "job": job_chart().dump_options_with_quotes()}
    print(charts)

    return charts

# 年销量数据大屏图表绘制之统计数据绘制
def plot_year_info_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()
    sales = df['sales'].copy()

    total = int(sales.iloc[-1])
    add = int(sales.iloc[-1] - sales.iloc[-2])
    ratio = float(np.round(add / (total + 1), 2)) * 100
    predict = int(np.round(sales.mean()))

    return {
        'total': total,
        'add': add,
        'ratio': ratio,
        'predict': predict
    }