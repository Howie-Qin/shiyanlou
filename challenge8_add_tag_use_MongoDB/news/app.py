#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#连接到数据库
app.config.update(dict(SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/shiyanlou'))

db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).shiyanlou

#文章表
class File(db.Model):
    __tablename__= 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    
    #文章的分类
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #文章的内容
    content = db.Column(db.Text)
    category = db.relationship('Category',
            backref=db.backref('file', lazy='dynamic'))
    
    def __init__(self, title, created_time, category, content):
         self.title = title
         self.created_time = created_time
         self.category = category
         self.content = content


    #像文章添加标签
    def add_tag(self, tag_name):
        #为文章添加tag标签存入到MongoDB
        file_item = mongo.files.find_one({'file_id':self.id})
        if file_item:
           # tags = file_item.get('tags')
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id': self.id}, {'$set':{'tags':tags}} )
        else:
            tags = [tag_name]
            mongo.files.insert_one({'file_id': self.id, 'tags':tags})
      #  return tags

    #移出标签
    def remove_tag(self, tag_name):
        #从MongoDB中移出 tag_name标签
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:
                return tags
            mongo.files.update_one({'file_id': self.id}, {'$set': {'tags': new_tags}})
            return new_tags
        return []

    #标签列表
    @property
    def tags(self):
        #读取mongodb,返回当前文章的标签列表
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            return file_item['tags']
        else:
            return []


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
    db.create_all()
    java = Category('java')
    python = Category('python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    #增加MongoDB中的数据
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


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


if __name__ == '__main__':
    insert_datas()
