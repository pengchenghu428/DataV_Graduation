#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from core.match import match_screen_title
from core.data import DataLoader
from core.plot import *

"""
    初始化：1.APP 2.DataLoader
"""
# APP 初始化
app = Flask(__name__)
bootstrap = Bootstrap(app)
# 数据 初始化
data_loader = DataLoader('data/raw')
data_loader.read_data()


# 404 页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500 页面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 根目录
@app.route('/')
def index():
    return render_template('index.html')


# 总览页面
@app.route('/overview/<mode>/')
def overview(mode):
    return render_template('overview.html')


# 年数据大屏页面
@app.route('/dscreen/<mode>/<name>/year/')
def year_data_screen(mode, name):
    cmode, cname = match_screen_title(mode, name)
    params = {
        'mode': mode,
        'name': name,
        'cmode': cmode,
        'cname': cname
    }
    return render_template('screen_year.html', params=params)

# 年-保有量数据绘图接口
@app.route('/year/ownChart/', methods=['GET', 'POST'])
def year_own_chart():
    mode, name = request.args.get('mode'), request.args.get('name')
    chart = plot_year_own_chart(data_loader, mode, name)
    return chart.dump_options_with_quotes()

# 年-房地产数据绘图接口
@app.route('/year/realtyChart/', methods=['GET', 'POST'])
def year_realty_chart():
    mode, name = request.args.get('mode'), request.args.get('name')
    charts = plot_year_realty_chart(data_loader, mode, name)
    return charts

# 年-统计数据接口
@app.route('/year/infoChart/', methods=['GET', 'POST'])
def year_info_chart():
    mode, name = request.args.get('mode'), request.args.get('name')
    charts = plot_year_info_chart(data_loader, mode, name)
    return charts

# 年数据大屏页面
@app.route('/dscreen/<mode>/<name>/month/')
def month_data_screen(mode, name):
    cmode, cname = match_screen_title(mode, name)

    return render_template('screen_month.html', mode=cmode, name=cname)


if __name__ == "__main__":
    app.run()