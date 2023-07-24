"""
    用户相关 api (view function)
"""
from app.forms.auth import EmailForm
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user
from app.forms.auth import RegisterForm, LoginForm, ResetPasswordForm
from . import web
from app.models import auto_commit
from app.models.user import User
from app.libs.email import send_mail

__author__ = "yangxin"


# GET: 用户打开注册页面  http://127.0.0.1:5000/register
# POST: 用户提交注册信息
@web.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)  # 校验 request form 表单提交的数据
    if request.method == "POST" and form.validate():
        with auto_commit() as db:
            user = User()
            user.nickname = form.nickname.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data)
            # 保存到数据库
            db.session.add(user)

        return redirect(url_for("web.login"))

    return render_template("auth/register.html", form=form)


# GET: 用户打开登录页面 http://127.0.0.1:5000/login
# POST: 用户提交登录信息
# flask-login
@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data, enable_status=1).first()
        if user and user.check_password(form.password.data):
            # 让浏览器保存用户登录的票据（Cookie），这里用到 flask_login.login_user，如果不会用，自己实现 Cookie 也行
            # login_user 需要知道用户的唯一标识是啥，这样才能区分不同的user，所以 login_user 要求传入的对象必须实现 get_id() 方法
            login_user(user, remember=True)

            # next 是一个URL query 参数，其值也是一个url
            next_url = request.args.get("next")
            if not next_url or not next_url.startswith("/"):
                return redirect(url_for("web.index"))
            return redirect(next_url)
        else:
            flash("账号不存在或者密码错误")

    return render_template("auth/login.html", form=form)


# 重置密码页面：http://127.0.0.1:5000/reset/password
@web.route("/reset/password", methods=["GET", "POST"])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == "POST" and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(
            email=account_email, enable_status=1
        ).first_or_404()  # TODO：如果没有找到数据，将会抛出异常，这个异常会被 @web.app_errorhandler 拦截

        # 异步发送邮件
        send_mail(
            account_email,
            "[鱼书] 重置你的密码",
            "email/reset_password.html",
            user=user,
            token=user.generate_token(),
        )
        flash("重置密码邮件已经发送成功，请到邮箱中查收")
    return render_template("auth/forget_password_request.html", form=form)


@web.route("/reset/password/<token>", methods=["GET", "POST"])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(
            token, generate_password_hash(form.password1.data)
        )
        if success:
            flash("您的密码已重置，请使用新密码登录")
            return redirect(url_for("web.login"))
        flash("密码重置失败")
    return render_template("auth/forget_password.html")


@web.route("/change/password", methods=["GET", "POST"])
def change_password():
    pass


@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web.index"))
