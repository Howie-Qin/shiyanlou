#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#连接到数据库
app.config.update(dict(SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/shiyanlou'))

db = SQLAlchemy(app)

#文章表
class File(db.Model):
    __tablename__= 'file'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    
    #文章的分类
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #文章的内容
    content = db.Column(db.Text)
    category = db.relationship('Category',
            backref=db.backref('file', lazy='dynamic'))

    def __init__(self, title, datetime, category, content):
        self.title = title
        self.datetime = datetime
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title

#类别表
class Category(db.Model):
    __tablename__= 'category'

    id = db.Column(db.Integer, primary_key=True)
    #类别的名称
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

def insert_datas():
    java = Category('java')
    python = Category('python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

@app.route('/')
def index():
    
    return render_template('index.html',files=File.query.all() )


@app.route('/files/<int:file_id>')
def file(file_id):
    #获取所有与file_id对应的文章表数据
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()

