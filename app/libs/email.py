"""
create by gaowenfeng on 
"""
from threading import Thread
from app import mail
from flask_mail import Message
from flask import current_app, render_template


def __send_mail_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except:
            print("邮件发送失败")


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        subject,
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[to],
    )
    msg.html = render_template(template, **kwargs)

    # current_app 只是 flask app 的代理对象，通过 _get_current_object() 获取真正的 flask app 实例
    app = current_app._get_current_object()

    # TODO：创建一个新的线程，异步发送，因为线程中需要用到 flask app 对象，而
    thr = Thread(target=__send_mail_async, args=[app, msg])
    thr.start()
