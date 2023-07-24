from flask_login import current_user, login_required
from flask import current_app, url_for, redirect, flash, render_template
from app.models.gift import Gift
from app.models import auto_commit
from app.view_models.trade import MyTrade
from . import web
from app.models.wish import Wish

__author__ = "yangxin"


@web.route("/my/wish")
@login_required  # 表示访问该接口，必须要登录
def my_wish():
    uid = current_user.id
    wishs_of_mine = Wish.get_user_wishs(uid)
    isbn_list = [wish.isbn for wish in wishs_of_mine]
    gift_count_list = Gift.get_gift_counts(isbn_list)
    view_model = MyTrade(wishs_of_mine, gift_count_list)
    return render_template("my_wish.html", wishes=view_model.trades)


@web.route("/wish/book/<isbn>")
@login_required  # 表示访问该接口，必须要登录
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with auto_commit() as db:
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书以添加进您的赠送清单或已经存在于您的心愿清单，请不要重复添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route("/satisfy/wish/<int:wid>")
def satisfy_wish(wid):
    pass


@web.route("/wish/book/<isbn>/redraw")
def redraw_from_wish(isbn):
    pass
