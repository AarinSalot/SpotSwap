import os
from functools import wraps
from secrets import token_hex
from flask import redirect, url_for, render_template, current_app, flash
from flask_login import current_user
from flask_mail import Message
from spotswap import mail
from hashlib import md5
from datetime import datetime
# from PIL import Image



def send_confirmation_mail(reciever_email, otp):
    print("I was called")
    print(reciever_email, otp)
    html_message = render_template('emails/email_confirmation.html', link=otp)
    text_message = render_template('emails/email_confirmation.txt', link=otp)
    print("Hey 1")
    msg = Message('Email Activation link', recipients=[reciever_email])
    print("Hey 2")
    msg.body = text_message
    msg.html = html_message
    print("Sending", msg)
    mail.send(msg)