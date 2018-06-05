from flask_mail import Message
from threading import Thread
from flask import current_app

from . import mail


def send_mail():
    """
    发送邮件
    """
    app = current_app._get_current_object()
    message = Message("subject", sender=app.config["MAIL_USERNAME"], recipients=[app.config["MAIL_USERNAME"]])
    message.body = "Hello World!"

    t = Thread(target=send_email, args=(app, message))
    t.start()

    return "<h1>Send Mail...</h1>"


def send_email(app, msg):
    with app.app_context():
        mail.send(msg)
