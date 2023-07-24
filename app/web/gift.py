from flask_login import login_required, current_user
from flask import current_app, url_for, redirect, flash, render_template
from app.models.gift import Gift
from app.models.wish import Wish
from app.models import auto_commit
from app.view_models.trade import MyTrade
from . import web


__author__ = "yangxin"


@web.route("/my/gifts")
@login_required  # 表示访问该接口，必须要登录
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Wish.get_wish_counts(isbn_list)
    view_model = MyTrade(gifts_of_mine, wish_count_list)
    return render_template("my_gifts.html", gifts=view_model.trades)


@web.route("/gifts/book/<isbn>")
@login_required  # 表示访问该接口，必须要登录
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with auto_commit() as db:
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(gift)
        ## 上面的 with auto_commit() 是简化的写法，下面的是复杂的写法
        # try:
        #     gift = Gift()
        #     gift.isbn = isbn
        #     gift.uid = current_user.id
        #     current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
        #     db.session.add(gift)
        #     db.session.commit()
        # except Exception as exception:
        #     db.session.rollback()
        #     raise exception
    else:
        flash("这本书已添加进您的 赠送清单 或 已经存在于您的心愿清单，请不要重复添加")

    # 重定向，将这个URL发给客户端，让客户端请求这个url
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/gifts/<gid>/redraw")
def redraw_from_gifts(gid):
    pass
