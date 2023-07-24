"""
    我们把 sqlalchemy model 和 flask_sqlalchemy.SQLAlchemy 关联起来；
    然后，把 flask_sqlalchemy.SQLAlchemy 的实例 "db" 关联给 flask app
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from app.models import db


class Base(db.Model):
    """其他的 model 继承 Base 类"""

    __abstract__ = True  # 告诉 sqlalchemy，不创建 base 表

    create_time = Column(Integer)  # 记录的创建时间
    enable_status = Column(SmallInteger, default=1)  # 是否可用

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    
    def to_dict(self):
        """ 将查询的对象转化为字典 """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def format_create_time(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
