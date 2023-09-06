from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread

"""
    Here, for sending email, I am using simple normal function
    that will take parameters as below:- 
"""
# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)

"""
    Here, for async email sending, here i am using Thread, Whenever send_email function will call, 
    then function will return immediately and then background task will execute using Thread.
    Sending of the email will run in the thread, and when the process completes the thread will
     end and clean itself up.
"""


def send_async_email(flask_app, msg):
    with flask_app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

