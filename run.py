from app import app
from app.web import web


__author__ = "yangxin"

# 将 蓝图对象 注册到 flask app 实例中
app.register_blueprint(web)

# 如果该文件是 python 的入口文件，则下面的代码会被执行，如果改文件被导入到其他模块了，则下面的代码不会被执行
if __name__ == "__main__":
    # 其实，在生产环境中，我们是使用 nginx + uwsgi 来启动项目的，下面的代码根本不会被执行
    # 因为，我们的项目是作为一个模块导入到 uwsgi 服务器里面
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
        threaded=True,
    )
