#-*- coding: UTF-8 -*-    
from flask import render_template
from . import main
from ..models import User, Role
from ..email import send_email

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/video')
def video():
    return render_template('video.html')
    
@main.route('/testmail/<email>')
def testmail(email):
    user = User(email = "yarlin@163.com",username = "yalinzhang")
    token = user.generate_confirmation_token()
    send_email(email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)

