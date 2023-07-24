# test_ctx.py

# 如果自己手动实例化 flask，那么需要手动维护上下文(AppContext)，才能使用 flask 内置的 current_app 对象
from flask import Flask, current_app

app = Flask(__name__)

with app.app_context():
    debug = current_app.config["DEBUG"]
    print(debug)

