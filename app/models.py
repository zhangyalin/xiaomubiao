#-*- coding: UTF-8 -*-    
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager

'''
在标准的SQL数据中,我们设置外键时往往只需要在要设置外键的表中添加外键,而不需要在被关联表中进行任何操作.但是在SQLAlchemy建模中,我们看到还需要在被关联的模型Role中添加关系.这其实是面向对象的思想,这里的的新建了一个名叫users的属性用来表示当前角色中包含的用户列表.users被定义成一个db.relationship对象,该对象的构造函数由两部分组成:
第一部分 —— 'User'表示关系的另一端模型的名称.
第二部分 —— 是一个名叫backref的参数,叫做反向关系,我们将其设置成'role',它会像User模型中添加一个名叫做role的属性,这个属性可以替代role_id访问Role模型,但是它获取的是Role模型的对象,而非Role模型对应的id的值。
'''
class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')  #表明

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #表明这列的值是roles表中行的id值
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


@login_manager.user_loader
def load_user(user_id):   #login_user，用户登录时会用到，进行请求和用户session的绑定。绑定后就可以使用current_user的状态了。很重要的一个函数啊
    return User.query.get(int(user_id))
