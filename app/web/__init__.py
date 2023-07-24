""" this is a flask blueprint layer (蓝图层)"""
from flask import Blueprint, render_template

__author__ = "yangxin"

# 蓝图初始化
web = Blueprint("web", __name__)


# flask app_errorhandler 这个装饰器，会监听程序 http 的返回状态码是404的时候才会执行
@web.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# 加载 web 蓝图下面的所有模块 (视图函数)、控制层Controller
from app.web import book
from app.web import hello
from app.web import auth
from app.web import gift
from app.web import main
from app.web import wish
from app.web import drift
