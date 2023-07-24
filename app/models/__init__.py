""" flask_sqlalchemy.SQLAlchemy 实例 """
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from app import app


db = SQLAlchemy()
db.init_app(app)

"""
# 和下面的 with 语句等价的，使用 db.create_all() 时需要激活 flask app context，
# 因为 db.create_all() 用到了 current_app 对象
    try:
        ctx = app.app_context()
        ctx.push()
        db.create_all()
    finally:
        ctx.pop()
"""
# 手动激活 app_context，因为 db.create_all() 用到了 current_app 对象
# 而 要用 current_app，那就要将 AppContext 推入栈中
with app.app_context():
    # 创建所有的表结构（如果表不存在的话）
    db.create_all()


# contextmanager 可以提供 with 语法
@contextmanager
def auto_commit():
    try:
        yield db
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        raise e
