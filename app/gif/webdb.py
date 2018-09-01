#-*- coding: UTF-8 -*-    

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import  SQLAlchemy

from . import gif  #移植新增
from .. import db  #移植新增
#import json  #解决print 中文显示为unicode的方法，用json,暂未解决

#from flask.ext.bootstrap import Bootstrap  #https://www.jianshu.com/p/102afa96bc4b bootstrap的使用

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



#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xiaozhu123!@localhost:3306/testdb?charset=utf8mb4'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True    #设置这一项是每次请求结束后都会自动提交数据库中的变动
#db = SQLAlchemy(app)    #实例化

#bootstrap = Bootstrap(app)  #https://www.jianshu.com/p/102afa96bc4b bootstrap的使用   {% extends "bootstrap/base.html" %}会自动引用，不需要copy过来这个模板

#class Role(db.Model):
#    __tablename__ = 'roles'
#    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
#    name = db.Column(db.String(16), nullable=False, server_default='', unique=True)
#    def __repr__(self):  #返回一个可以用来表示对象的可打印的友好的字符串
#        return '<Role %r>' % self.name
        
#class User(db.Model):
#    __tablename__ = 'users'
#    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
#    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
#    role_id = db.Column(db.Integer, nullable=False, server_default='0')
#    def __repr__(self):
#        return '<User %r,Role id %r>' %(self.username,self.role_id)

#class Fuck(db.Model):   #这里的类名和下面的tablename随便取
#    __tablename__ = 'fuckers'
#    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
#    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
#    role_id = db.Column(db.Integer, nullable=False, server_default='0')
#    def __repr__(self):
#        return '<Fucker %r,Role id %r>' %(self.username,self.role_id)

class Tupian(db.Model):   #这里的类名和下面的tablename随便取
    __tablename__ = 'tupian'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True, server_default='', index=True)
    label = db.Column(db.String(255), nullable=False, server_default='')
    text = db.Column(db.String(255), nullable=True, server_default='')
    def __repr__(self):
        return '<name %r,label %r,text %r>' %(self.name,self.label,self.text)
        
        
@gif.route('/')  #route定义以/结尾时， 用户输入带或不带/都会定向到这里，和大多数http服务器一致。 所以为了容错，最好尾部都带一个/
def index():
    #return 'Index Page：you know nothing'
    return render_template('gif/user_bootstrap_page.html')
    
#@gif.route('/jinja/<feature>')
#def templ(feature):
#    print feature
#    return render_template('gif/user.html',name=feature)
    
    
@gif.route('/label/<feature>')  #URL中的参数带空格时可用%20表示  #http://123.207.60.61:5000/label/%E7%89%B9%E6%9C%97%E6%99%AE%20%E5%A4%A7%E7%AC%91
def show_user_profile(feature):
    # show the user profile for that user  变量是字符串
    #data = Tupian.query.filter_by(label='希拉里').all()
    #print data
    #print data[0].name
    #return 'label %s:%s' %(feature,Tupian.query.all())
    #return render_template('user.html',name=Tupian.query.filter(Tupian.label.ilike('%特朗普%')).all())  #模糊查询
    #return render_template('user.html',name=Tupian.query.filter(Tupian.label.ilike('%{}%'.format(feature))).all())  #模糊查询
    #return render_template('user.html',name=Tupian.query.filter_by(label=feature).all())
    print 'url:  ', url_for('gif.show_user_profile', feature = feature, page=2,  _external = True)
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
        return render_template('gif/user_bootstrap_page.html',name='', pagination = '', feature = feature)  #模糊查询， 分页查询 
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
    return render_template('gif/user_bootstrap_page.html',name=posts, pagination = pagination, feature = feature)  #模糊查询， 分页查询
    
@gif.route('/settext', methods = ['GET','POST'])  # 从请求中提取两个参数 图片id 和 text #http://123.207.60.61:5000/gif/settext?name=3.jpg&text=haha
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
        #print 'url:', url_for('gif.settext')
        print 'cur path:', sys.path[0]  
        im = Image.open('app/static/init/'+request.args.get('name'))
        print "format: ", im.format
        if im.format == 'GIF':
            #processImage(sys.argv[1], sys.argv[2]) duration不影响gif文件的大小
            processGif('app/static/init/'+request.args.get('name'), request.args.get('text'), 'app/static/temp/'+timestr+request.args.get('name'))
            return render_template('gif/returntupian.html',name=timestr+request.args.get('name'))
        else:
            processPngJpg('app/static/init/'+request.args.get('name'), request.args.get('text'), 'app/static/temp/'+timestr+request.args.get('name'))
            return render_template('gif/returntupian.html',name=timestr+request.args.get('name'))
            
      
    
    
#debug=True 表示调试模式，flask检测到文件内容修改会重新启动服务
#host='0.0.0.0' 表示监听监听所有公网 IP，否则只能本地测试http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #db.create_all()
    #db.session.add(Tupian(name='1.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'))
    #db.session.add_all([Tupian(name='2.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='3.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='4.jpg',label='特朗普',text='嘲讽  笨蛋 你狠')])
    #db.session.commit()
    #Tupian.query.all()