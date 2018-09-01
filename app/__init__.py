#-*- coding: UTF-8 -*-    
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'none' #none, basic, strong
login_manager.login_view = 'auth.login'  #设置登录页面的端点,因为是blueprint中定义的，所以有auth，  
#login_manager.login_view  的作用是： 未登录时，访问需要登录的页面，会跳转过去的登录页面。比如这里就是auth里定义的view都是需要登录的，main下面的不需要


def create_app(config_name):  #app/__init__.py的主要作用就是使用程序工厂函数创建app主进程
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    print 'config MAIL_USERNAME:', config[config_name].MAIL_USERNAME, 'config MAIL_PASSWORD:', config[config_name].MAIL_PASSWORD
    
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint  #from A import b ==import A，b=A.b；  从main这个包里引入main类（蓝本），import xx导入模块对于模块中的函数，每次调用需要“模块.函数”来用。from xx import fun 直接导入模块中某函数，直接fun()就可用。
    app.register_blueprint(main_blueprint)   #url_prefix关键字 参数（这个参数默认是/），注两个blueprint不能使用重复的url_prefix，否则后面的会不生效，bug
    #app.register_blueprint(main_blueprint, url_prefix='/main')
    
    from .auth import auth as auth_blueprint   #as 表示别名
    #app.register_blueprint(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  #url_prefix关键字 参数（这个参数默认是/）

    from .gif import gif as auth_blueprint   #as 表示别名
    #app.register_blueprint(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/gif')  #url_prefix关键字 参数（这个参数默认是/）
    
    return app
