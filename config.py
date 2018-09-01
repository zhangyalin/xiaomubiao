#-*- coding: UTF-8 -*-    
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print 'config basedir:', basedir

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')  #gkiefmxuqzhfiieg   ntocsylgypkgfgej  #https://www.jianshu.com/p/32e2f82a63c3  POP3/SMTP 和IMAP/SMTP都需要开启
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1120111205@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ntocsylgypkgfgej'  
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <1120111205@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://root:xiaozhu123!@localhost:3306/testdb?charset=utf8mb4'     ##'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql://root:xiaozhu123!@localhost:3306/testdb?charset=utf8mb4'     ##'sqlite://'
        


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:xiaozhu123!@localhost:3306/testdb?charset=utf8mb4'     ##'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
