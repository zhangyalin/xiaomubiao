#-*- coding: UTF-8 -*-    
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth    #  form .表示从当前目录下的__init__中导入auth符号（这里定义是blueprint）
from .. import db     #  form ..表示从上级目录下的__init__中导入db符号（这里定义是db）
from ..models import User, Role
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm

#request.endpoint, 实际上这个endpoint就是一个Identifier，每个视图函数都有一个endpoint
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    #print  'role id:', Role.query.filter(Role.name == 'User').first().id
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)   #https://segmentfault.com/q/1010000010253582  解释了login_user 和 models.py里login_manager.user_loader 的load_user关系
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')  #blueprint  的url_for和 app的url_for不太一样，这里的参数是blueprint端点名+路由函数。看到这种格式就说明有个main的模块以及它有路由函数index. 如果没有端点名说明是本blueprint自己的路由函数。
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #user_role = Role(name = 'User')  #新建role时使用
        #user = User(email = form.email.data,username = form.username.data,password = form.password.data,role = user_role) #新建role时使用
        #user = User(email = form.email.data,username = form.username.data,password = form.password.data,role_id = 1)  #这句也可以，不过role_id固定写1，通用性太差，改成下面这句
        user = User(email = form.email.data,username = form.username.data,password = form.password.data,role_id = Role.query.filter(Role.name == 'User').first().id)
        #db.session.add(user_role)
        db.session.add(user)   ##db.session.add 和 db.session.commit是SQLAlchemy的修改行的标准方法
        db.session.commit()
        token = user.generate_confirmation_token()
        print 'user.email:', user.email 
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
