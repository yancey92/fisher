"""
    flask core application layer
    实例化 flask core app
"""
from logging.handlers import RotatingFileHandler
from flask import Flask
import logging
from flask_login import LoginManager
from flask_mail import Mail


""" 实例化一个 flask 应用实例 """
app = Flask(__name__, static_url_path="/static", static_folder="./static")
app.config.from_object("app.common_config")
app.config.from_object("app.secure_config")


""" 设置日志的格式 """
# 发生时间   日志等级   日志信息文件名   函数名   行数   日志信息
my_format = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s"
# logging.basicConfig(format=my_format)
formatter = logging.Formatter(fmt=my_format)
file_log_handler = RotatingFileHandler(
    app.name + ".log", maxBytes=1024 * 1024, backupCount=7
)
file_log_handler.setFormatter(formatter)
app.logger.addHandler(file_log_handler)


""" LoginManager 用来管理用户登录的状态，如 Cookie, Session, 登录成功重定向等 """
login_manager = LoginManager()
login_manager.login_view = "web.login"
login_manager.login_message = "请先登录或注册"
login_manager.init_app(app)


""" flask email 发送设置 """
mail = Mail()
mail.init_app(app)


