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
from statsmodels.tsa.seasonal import seasonal_decompose


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
            legend_opts=opts.LegendOpts(pos_top="5%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
            # toolbox_opts=opts.ToolboxOpts(),
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
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
        )
            .add_yaxis(
            '8年差分',
            (tdf['8year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            symbol='rect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
        )
            .add_yaxis(
            '6年差分',
            (tdf['6year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            symbol='triangle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
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
            Bar()
                .add_xaxis(x_data)
                .add_yaxis(
                '商品房',
                (tdf['ave_price_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                '住宅',
                (tdf['ave_price_residence_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                '商业营业用',
                (tdf['ave_price_business_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            )
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='单价(元/平方米)',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="均价差分"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '年销量(K)',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False
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
                Pie()
                    .add(
                    "开发商类型占比",
                    data,
                    rosetype='radius',
                    radius=["30%", "55%"],
                ).set_global_opts(
                    title_opts=opts.TitleOpts("{}房地产开发商数量".format(year)),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
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
                (tdf['complete_investment_diff_1'] / 1000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                '建筑安装',
                (tdf['building_investment_diff_1'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                '装备',
                (tdf['equip_investment_diff_1'] / 1000).tolist(),
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
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '年销量(K)',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False
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
                (tdf['complete_area'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                '竣工价值',
                (tdf['complete_price_diff_1'] / 1000).tolist(),
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
                title_opts=opts.TitleOpts(title="工程量"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '年销量(K)',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=3,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False
            )
        )
        bar.overlap(line)
        return bar

    # tab = Tab()
    # tab.add(dev_chart(), '企业')
    # tab.add(price_chart(), '均价')
    # tab.add(investment_chart(), '投资')
    # tab.add(job_chart(), '工量')

    charts = {"dev": dev_chart().dump_options_with_quotes(),
              "price": price_chart().dump_options_with_quotes(),
              "investment": investment_chart().dump_options_with_quotes(),
              "job": job_chart().dump_options_with_quotes()}
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


# 年销量数据大屏图表绘制之序列数据绘制
def plot_year_seq_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()
    sales = df['sales'].copy()
    diff_sales = df['sales'].diff(1)

    res = seasonal_decompose(sales, period=2)
    trend = res.trend
    season = res.seasonal
    resid = res.resid

    line1 = (
        Line(
            init_opts=opts.InitOpts(width="644px", height="260px")
        ).add_xaxis(
            x_data
        ).add_yaxis(
            "销量",
            (sales / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "差分销量",
            (diff_sales / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='rect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            title_opts=opts.TitleOpts(title="销量"),
            legend_opts=opts.LegendOpts(pos_top="5%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
        )
    )

    line2 = (
        Line(
            init_opts=opts.InitOpts(width="644px", height="260px")
        ).add_xaxis(
            x_data
        ).add_yaxis(
            "销量趋势",
            (trend / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "销量周期",
            (season / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='roundRect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "销量残差",
            (resid / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='triangle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            title_opts=opts.TitleOpts(title="销量分解", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="55%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
        )
    )

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="644px", height="520px")
        ).add(
            line1, grid_opts=opts.GridOpts(pos_bottom="60%")
        ).add(
            line2, grid_opts=opts.GridOpts(pos_top="60%")
        )

    )

    return grid


# 年销量数据大屏图表绘制之宏观数据绘制
def plot_year_macro_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()

    def gdp_chart():
        cols = ['gni', 'gdp', 'fgdp', 'sgdp', 'tgdp']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "GNI",
                (tdf['gni_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "GDP",
                (tdf['gdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "F-GDP",
                (tdf['fgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "S-GDP",
                (tdf['sgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "T-GDP",
                (tdf['tgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分经济"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    def add_chart():
        cols = ['industry_add', 'architecture_add', 'bank_add', 'realty_add']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "工业",
                (tdf['industry_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "建筑业",
                (tdf['architecture_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "银行业",
                (tdf['bank_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "房地产业",
                (tdf['realty_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分增加值"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    # tab = Tab()
    # tab.add(gdp_chart(), "GDP")
    # tab.add(add_chart(), "ADD")

    charts = {
        'gdp': gdp_chart().dump_options_with_quotes(),
        'add': add_chart().dump_options_with_quotes()
    }

    return charts


# 年销量数据大屏图表绘制之财政支出数据绘制
def plot_year_finance_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()

    def fin_line():
        cols = ['fin_pub_service', 'fin_society', 'fin_environment', 'fin_services']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "一级公共服务",
                (tdf['fin_pub_service_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "社会保障和就业",
                (tdf['fin_society_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "环境保护",
                (tdf['fin_environment_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='roundRect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "财政农林",
                (tdf['fin_services_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='diamond', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分增加值"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    def fin_pie():
        cols = ['fin_pub_service', 'fin_society', 'fin_environment', 'fin_services']
        names = ["一级公共服务", '社会保障和就业', "环境保护", "财政农林"]
        tdf = df[cols].copy()
        tl = Timeline()
        for i, year in enumerate(x_data):
            data = tdf.iloc[i].tolist()
            data = [[names[idx], dd] for idx, dd in enumerate(data)]
            pie = (
                Pie()
                    .add(
                    "部分财政支出",
                    data,
                    rosetype='radius',
                    radius=["30%", "55%"],
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("{}部分财政支出".format(year)),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
                )
            )
            tl.add(pie, "{}年".format(year))
        return tl

    # tab = Tab()
    # tab.add(fin_pie(), "财政支出占比")
    # tab.add(fin_line(), "支出差分曲线")

    charts = {
        'pie': fin_pie().dump_options_with_quotes(),
        'line': fin_line().dump_options_with_quotes()
    }

    return charts


# 月销量数据大屏图表绘制之保有量数据绘制
def plot_month_own_chart(data_loader, mode, name):
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
            legend_opts=opts.LegendOpts(pos_top="5%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
            # toolbox_opts=opts.ToolboxOpts(),
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
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
        )
            .add_yaxis(
            '8年差分',
            (tdf['8year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            symbol='rect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
        )
            .add_yaxis(
            '6年差分',
            (tdf['6year_own_diff_1'] / 10000).tolist(),
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            symbol='triangle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),
            is_smooth=False
        )
    )

    bar.overlap(line)

    return bar


# 月销量数据大屏图表绘制之房地产数据绘制
def plot_month_realty_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'month', name)
    x_data = df[['year', 'month']].apply(lambda x: "{}-{:0>2d}".format(x[0], x[1]), axis=1).tolist()
    sales = df['sales'].copy()

    def total_chart():
        cols = ['roadwork_area_total',
                'new_area_total',
                'complete_area_total']
        cols = ["{}_diff_1".format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '施工面积',
                (tdf['roadwork_area_total_diff_1'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            )
                .add_yaxis(
                '新开施工面积',
                (tdf['new_area_total_diff_1'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            )
                .add_yaxis(
                '竣工面积',
                (tdf['complete_area_total_diff_1'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='triangle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万平方米',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="施、竣工与销量关系"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)

        return line

    def rise_chart():
        cols = ['roadwork_area_rise',
                'new_area_rise',
                'complete_area_rise']
        cols = cols + ["{}_diff_1".format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis(
                '施工面积',
                (tdf['roadwork_area_rise'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            )
                .add_yaxis(
                '新开施工面积',
                (tdf['new_area_rise'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            )
                .add_yaxis(
                '竣工面积',
                (tdf['complete_area_rise'] / 1).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                symbol='triangle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2),
                is_smooth=False,
                is_connect_nones=True
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万平方米',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="施、竣工与销量关系"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    total = total_chart()
    rise = rise_chart()

    # tab = Tab()
    # tab.add(total, "累计值")
    # tab.add(rise, "累计增长率")

    charts = {
        'total': total.dump_options_with_quotes(),
        'rise': rise.dump_options_with_quotes()
    }

    return charts


# 月销量数据大屏图表绘制之统计数据绘制
def plot_month_info_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'month', name)
    x_data = df[['year', 'month']].apply(lambda x:"", axis=1).tolist()
    sales = df['sales'].copy()

    now = int(sales.iloc[-1])
    pre = int(sales.iloc[-2])
    pre_pre = int(sales.iloc[-13])
    add = int(now - pre)
    ratio1 = float(np.round(add / (now + 1), 2)) * 100
    ratio2 = float(np.round((now-pre_pre) / (now + 1), 2)) * 100
    predict = int(np.round(sales.mean()))

    return {
        'total': now,
        'add': add,
        'ratio1': ratio1,
        'ratio2': ratio2,
        'predict': predict
    }


# 月销量数据大屏图表绘制之销量序列数据绘制
def plot_month_seq_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'month', name)
    x_data = df[['year', 'month']].apply(lambda x: "{}-{:0>2d}".format(x[0], x[1]), axis=1).tolist()
    sales = df['sales'].copy()
    diff_sales = df['sales'].diff(1)

    res = seasonal_decompose(sales, period=12)
    trend = res.trend
    season = res.seasonal
    resid = res.resid

    line1 = (
        Line(
            init_opts=opts.InitOpts(width="644px", height="260px")
        ).add_xaxis(
            x_data
        ).add_yaxis(
            "月销量",
            (sales / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "差分月销量",
            (diff_sales / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='rect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            title_opts=opts.TitleOpts(title="月销量"),
            legend_opts=opts.LegendOpts(pos_top="5%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
        )
    )

    line2 = (
        Line(
            init_opts=opts.InitOpts(width="644px", height="260px")
        ).add_xaxis(
            x_data
        ).add_yaxis(
            "销量趋势",
            (trend / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='circle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "销量周期",
            (season / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='roundRect', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).add_yaxis(
            "销量残差",
            (resid / 10000).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_connect_nones=True,
            symbol='triangle', symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2)
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            title_opts=opts.TitleOpts(title="销量分解", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="55%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=opts.DataZoomOpts(type_="inside")
        )
    )

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="644px", height="520px")
        ).add(
            line1, grid_opts=opts.GridOpts(pos_bottom="60%")
        ).add(
            line2, grid_opts=opts.GridOpts(pos_top="60%")
        )

    )

    return grid


# 月销量数据大屏图表绘制之宏观数据绘制
def plot_month_macro_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()

    def gdp_chart():
        cols = ['gni', 'gdp', 'fgdp', 'sgdp', 'tgdp']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "GNI",
                (tdf['gni_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "GDP",
                (tdf['gdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "F-GDP",
                (tdf['fgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "S-GDP",
                (tdf['sgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "T-GDP",
                (tdf['tgdp_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分经济"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    def add_chart():
        cols = ['industry_add', 'architecture_add', 'bank_add', 'realty_add']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "工业",
                (tdf['industry_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "建筑业",
                (tdf['architecture_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "银行业",
                (tdf['bank_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "房地产业",
                (tdf['realty_add_diff_1'] / 10000).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='万亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分增加值"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    # tab = Tab()
    # tab.add(gdp_chart(), "GDP")
    # tab.add(add_chart(), "ADD")

    charts = {
        'gdp': gdp_chart().dump_options_with_quotes(),
        'add': add_chart().dump_options_with_quotes()
    }

    return charts


# 年销量数据大屏图表绘制之财政支出数据绘制
def plot_month_finance_chart(data_loader, mode, name):
    df = data_loader.get_data(mode, 'year', name)
    x_data = df['year'].astype(str).tolist()

    def fin_line():
        cols = ['fin_pub_service', 'fin_society', 'fin_environment', 'fin_services']
        cols = ['{}_diff_1'.format(col) for col in cols] + ['sales']
        tdf = df[cols].copy()

        line = (
            Line().add_xaxis(
                x_data
            ).add_yaxis(
                "一级公共服务",
                (tdf['fin_pub_service_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='circle', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "社会保障和就业",
                (tdf['fin_society_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='rect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "环境保护",
                (tdf['fin_environment_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='roundRect', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).add_yaxis(
                "财政农林",
                (tdf['fin_services_diff_1']).tolist(),
                yaxis_index=0,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                symbol='diamond', symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(width=2)
            ).extend_axis(
                yaxis=opts.AxisOpts(
                    name='销量',
                    type_='value',
                    position='right')
            ).set_global_opts(
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(
                    name='亿',
                    type_='value',
                    position='left',
                    splitline_opts=opts.SplitLineOpts(is_show=True)),
                title_opts=opts.TitleOpts(title="差分增加值"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
            )
        )

        bar = (
            Bar().add_xaxis(
                x_data
            ).add_yaxis(
                '销量',
                (tdf['sales'] / 1000).tolist(),
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        line.overlap(bar)
        return line

    def fin_pie():
        cols = ['fin_pub_service', 'fin_society', 'fin_environment', 'fin_services']
        names = ["一级公共服务", '社会保障和就业', "环境保护", "财政农林"]
        tdf = df[cols].copy()
        tl = Timeline()
        for i, year in enumerate(x_data):
            data = tdf.iloc[i].tolist()
            data = [[names[idx], dd] for idx, dd in enumerate(data)]
            pie = (
                Pie()
                    .add(
                    "部分财政支出",
                    data,
                    rosetype='radius',
                    radius=["30%", "55%"],
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts("{}部分财政支出".format(year)),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
                )
            )
            tl.add(pie, "{}年".format(year))
        return tl

    # tab = Tab()
    # tab.add(fin_pie(), "财政支出占比")
    # tab.add(fin_line(), "支出差分曲线")

    charts = {
        'pie': fin_pie().dump_options_with_quotes(),
        'line': fin_line().dump_options_with_quotes()
    }

    return charts