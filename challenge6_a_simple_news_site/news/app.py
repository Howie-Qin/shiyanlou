#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json, os
from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route('/')
def index():
    filename = []
    filename.append(os.path.abspath('/home/shiyanlou/files/helloshiyanlou.json'))
    filename.append(os.path.abspath('/home/shiyanlou/files/helloworld.json'))
    with open(filename[0]) as file1:
        file_helloshiyanlou = json.loads(file1.read())
    with open(filename[1]) as file2:
        file_helloworld = json.loads(file2.read())
    titles = [file_helloshiyanlou['title'], file_helloworld['title']]
    return render_template('index.html', titles=titles)


@app.route('/files/<filename>')
def file(filename):
    road_file = '/home/shiyanlou/files/'+ filename +'.json'
   # if filename == 'invalid':
   #     abort(404)
    with open(road_file) as file:
        file_content = json.loads(file.read())
    
    return render_template('file.html', file_content=file_content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()

