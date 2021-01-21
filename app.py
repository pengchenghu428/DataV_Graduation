#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


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


# 数据大屏页面
@app.route('/dscreen/<mode>/<name>/')
def data_screen(mode, name):
    return render_template('dscreen.html', mode=mode, name=name)


if __name__ == "__main__":
    app.run()