from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.models.base import Base
from app.models.book import Book
# from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from authlib.jose import jwt
from flask import current_app
from app.models import auto_commit
from datetime import datetime, timedelta


# UserMixin, 视频解释: 《Python Flask高级编程之从0到1开发《鱼书》精品项目》第 9-13、9-14
class User(Base, UserMixin):
    __tablename__ = "user"  # 指定数据库表名，如果不设置，默认是类名的小写

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    password = Column(String(128), nullable=False)  # 密文密码
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)  # 拥有的鱼豆数量
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    def check_password(self, password):
        if not password:
            return False
        return check_password_hash(self.password, password)

    # 该方法是 flask_login.login_user 要求实现的，get_id() 名字是固定的，用来让 login_user 知道唯一标识是什么
    def get_id(self):
        return self.id

    def can_save_to_list(self, isbn):
        """
        判断可以将书籍加入心愿清单
        1.如果isbn编号不符合合法
        2.如果isbn编号对应的书籍不存在，不允许添加
        3.一本书必须即不在心愿清单又不在赠书列表里才可以添加
        """
        short_isbn = isbn.replace("-", "")
        if (
            not (len(short_isbn) == 13 or len(short_isbn) == 10)
            or not short_isbn.isdigit()
        ):
            return False

        bookCollection=Book.search_by_isbn(isbn)
        if not bookCollection.first_element:
            return False

        gifting = Gift.query.filter_by(
            uid=self.id, isbn=isbn, launched=False, enable_status=1
        ).first()
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False, enable_status=1
        ).first()
        return not wishing and not gifting

    def has_in_gifts(self, isbn):
        return (
            Gift.query.filter_by(uid=self.id, isbn=isbn, enable_status=1).first()
            is not None
        )

    def has_in_wishs(self, isbn):
        return (
            Wish.query.filter_by(uid=self.id, isbn=isbn, enable_status=1).first()
            is not None
        )

    # 生成 token，过期时间 60*60 秒
    def generate_token(self, expiration=60 * 60):
        header = {"alg": "HS256"}
        key = current_app.config["SECRET_KEY"]
        payload = {"id": self.id, "exp": datetime.now() + timedelta(seconds=expiration)}
        return jwt.encode(header=header, payload=payload, key=key)

    # 重置密码
    @classmethod
    def reset_password(cls, token, new_password):
        key = current_app.config["SECRET_KEY"]
        try:
            data = jwt.decode(token, key)  # 如果token过期，或者token非法，则抛出异常
        except Exception as e:
            print(e)
            return False

        uid = data.get("id")
        with auto_commit() as db:
            user = User.query.get_or_404(uid)
            user.password = new_password
        return True


# login_manager.current_user 会用到这个这个函数
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
