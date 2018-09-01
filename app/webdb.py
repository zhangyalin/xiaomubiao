#-*- coding: UTF-8 -*-    

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import  SQLAlchemy

#import json  #解决print 中文显示为unicode的方法，用json,暂未解决

from flask.ext.bootstrap import Bootstrap  #https://www.jianshu.com/p/102afa96bc4b bootstrap的使用

import sys
import os  
from PIL import Image  
import imageio
from PIL import Image,ImageDraw,ImageFont  
from tphandle import processGif, processPngJpg

#https://www.cnblogs.com/weedboy/p/6862158.html  解决.format(feature)抛异常：UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )   #这里定义后，后面字符串就不需要额外使用unicode(comment,'utf-8')， 否则会报错，提示TypeError: decoding Unicode is not supported

import time

from flask_wtf import FlaskForm #处理表单专用， pip install flask-wtf
#WTForms是一个支持多个web框架的form组件，主要用于对用户请求数据进行验证。
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_login import login_user, logout_user, login_required, current_user  #pip install flask-login  
from flask_login import UserMixin  #使用flask_login进行用户的登录和登出管理，需要将我们的User模型继承flask_login的UserMixin基类
from flask import current_app  # current_app代表当前的flask程序实例,使用时需要flask的程序上下文激活， 便于在多文件结构时获取app的app.config
from flask_mail import Message # pip install flask-mail
from flask_login import LoginManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xiaozhu123!@localhost:3306/testdb?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True    #设置这一项是每次请求结束后都会自动提交数据库中的变动


#################################user 相关
app.config['SECRET_KEY'] = 'fuck money'         # 必须 用于加密


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



##################################下面都是处理数据库的##############################################################################
##################################下面都是处理数据库的##############################################################################





db = SQLAlchemy(app)    #实例化

bootstrap = Bootstrap(app)  #https://www.jianshu.com/p/102afa96bc4b bootstrap的使用   {% extends "bootstrap/base.html" %}会自动引用，不需要copy过来这个模板


class Tupian(db.Model):   #这里的类名和下面的tablename随便取
    __tablename__ = 'tupian'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True, server_default='', index=True)
    label = db.Column(db.String(255), nullable=False, server_default='')
    text = db.Column(db.String(255), nullable=True, server_default='')
    def __repr__(self):
        return '<name %r,label %r,text %r>' %(self.name,self.label,self.text)
        
        
@app.route('/')  #route定义以/结尾时， 用户输入带或不带/都会定向到这里，和大多数http服务器一致。 所以为了容错，最好尾部都带一个/
def index():
    #return 'Index Page：you know nothing'
    return render_template('user_bootstrap_page.html')
    
@app.route('/jinja/<feature>')
def templ(feature):
    print feature
    return render_template('user.html',name=feature)
    
    
@app.route('/label/<feature>')  #URL中的参数带空格时可用%20表示  #http://123.207.60.61:5000/label/%E7%89%B9%E6%9C%97%E6%99%AE%20%E5%A4%A7%E7%AC%91
def show_user_profile(feature):
    # show the user profile for that user  变量是字符串
    #data = Tupian.query.filter_by(label='希拉里').all()
    #print data
    #print data[0].name
    #return 'label %s:%s' %(feature,Tupian.query.all())
    #return render_template('user.html',name=Tupian.query.filter(Tupian.label.ilike('%特朗普%')).all())  #模糊查询
    #return render_template('user.html',name=Tupian.query.filter(Tupian.label.ilike('%{}%'.format(feature))).all())  #模糊查询
    #return render_template('user.html',name=Tupian.query.filter_by(label=feature).all())
    print 'url:  ', url_for('show_user_profile', feature = feature, page=2,  _external = True)   #_external生成url绝对路径
    page=request.args.get('page',1,type=int)   #从url请求里提取?page=xxx
    #pagination = Tupian.query.filter(Tupian.label.ilike('%{}%'.format(feature))).paginate(page,per_page=5,error_out=False)
    strlist = feature.split(' ')
    strfilter = '' 
    for value in strlist:
        print value
        #print 'Tupian.label.ilike(\'%'+value+'%\')'
        
    #没搞定should be explicitly declared as text(u'sdfsafsdf')错误，还是用switch的方法
    #for i in  range(len(strlist)):
    #    print strlist[i]
    #    strfilter = strfilter + 'Tupian.label.ilike(\'%'+strlist[i]+'%\')' 
    #    if i != len(strlist)-1:
    #        strfilter = strfilter +','
    #print strfilter
    #strfilter = strfilter.encode("utf-8")
    #pagination = Tupian.query.filter(strfilter).paginate(page,per_page=5,error_out=False)
    #posts = pagination.items
    #print posts
    #return render_template('user_bootstrap_page.html',name=posts, pagination = pagination, feature = feature)  #模糊查询， 分页查询
    
    filterlen = len(strlist)
    print filterlen
    if filterlen == 0:
        return render_template('user_bootstrap_page.html',name='', pagination = '', feature = feature)  #模糊查询， 分页查询 
    elif filterlen == 1:
        pagination = Tupian.query.filter(Tupian.label.ilike('%{}%'.format(strlist[0])) ).paginate(page,per_page=5,error_out=False)
        posts = pagination.items
        print posts
    elif filterlen == 2:
        pagination = Tupian.query.filter(Tupian.label.ilike('%{}%'.format(strlist[0])), Tupian.label.ilike('%{}%'.format(strlist[1])) ).paginate(page,per_page=5,error_out=False)
        posts = pagination.items
        print posts
    elif filterlen == 3:
        pagination = Tupian.query.filter(Tupian.label.ilike('%{}%'.format(strlist[0])), Tupian.label.ilike('%{}%'.format(strlist[1])) , Tupian.label.ilike('%{}%'.format(strlist[2]))).paginate(page,per_page=5,error_out=False)
        posts = pagination.items
        print posts
    else: #最多支持4个参数，后面的忽略
        pagination = Tupian.query.filter(Tupian.label.ilike('%{}%'.format(strlist[0])), Tupian.label.ilike('%{}%'.format(strlist[1])) , Tupian.label.ilike('%{}%'.format(strlist[2])), Tupian.label.ilike('%{}%'.format(strlist[3]))).paginate(page,per_page=5,error_out=False)
        posts = pagination.items
        print posts
    return render_template('user_bootstrap_page.html',name=posts, pagination = pagination, feature = feature)  #模糊查询， 分页查询
    
@app.route('/settext', methods = ['GET','POST'])  # 从请求中提取两个参数 图片id 和 text #http://123.207.60.61:5000/settext?name=3.jpg&text=hah
def settext():
    time_now = int(time.time())
    timestr = str(time_now)
    print time_now,timestr 
    if request.method == 'POST':
        print request.form['name'], request.form['text']
        print 'path: ', 'static/init/'+request.form['name']
        im = Image.open('static/init/'+request.form['name'])
        print "format: ", im.format
        if im.format == 'GIF':
            #processImage(sys.argv[1], sys.argv[2]) duration不影响gif文件的大小
            processGif('static/init/'+request.form['name'], request.form['text'])
        else:
            processPngJpg('static/init/'+request.form['name'], request.form['text'])
    else:
        #pass
        print request.args.get('name')
        print request.args.get('text')
        im = Image.open('static/init/'+request.args.get('name'))
        print "format: ", im.format
        if im.format == 'GIF':
            #processImage(sys.argv[1], sys.argv[2]) duration不影响gif文件的大小
            processGif('static/init/'+request.args.get('name'), request.args.get('text'), 'static/temp/'+timestr+request.args.get('name'))
            return render_template('returntupian.html',name=timestr+request.args.get('name'))
        else:
            processPngJpg('static/init/'+request.args.get('name'), request.args.get('text'), 'static/temp/'+timestr+request.args.get('name'))
            return render_template('returntupian.html',name=timestr+request.args.get('name'))
            
      
    
    
##################################下面都是处理用户管理系统的##############################################################################
##################################下面都是处理用户管理系统的##############################################################################
####表单处理

class LoginForm(FlaskForm):  #登录
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm): #注册
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):  #修改密码
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')

####用户和数据处理model
class Role(db.Model):  #这里的类名和下面的tablename随便取
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):  #这里的类名和下面的tablename随便取
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

        

@login_manager.user_loader   #这个到底是怎么用的？
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
####视图处理 view
@app.before_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@app.route('/confirm/<token>')
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


@app.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@app.route('/change-password', methods=['GET', 'POST'])
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

    
    
    
    
    
    
    

            
    
    
#debug=True 表示调试模式，flask检测到文件内容修改会重新启动服务
#host='0.0.0.0' 表示监听监听所有公网 IP，否则只能本地测试http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #db.create_all()
    #db.session.add(Tupian(name='1.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'))
    #db.session.add_all([Tupian(name='2.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='3.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='4.jpg',label='特朗普',text='嘲讽  笨蛋 你狠')])
    #db.session.commit()
    #Tupian.query.all()