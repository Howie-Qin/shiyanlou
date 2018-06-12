# 从数据库中读取内容
> 通过插件flask-sqlalchemy创建两个表，插入数据（python shell）,之后再读取其中内容，通过render_template在网页中显示

==注意点==
1. 注意配置app.config连接到数据库
2. Flask插件模块flask-sqlalchemy
快速上手手册(http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application)
3. 在使用flask shell时，在db.create.all()要先从app中引入db，即from app import db，同理使用函数也得先导入
4. 读取表中所有内容：
```
 return render_template('index.html',files=File.query.all() )
```
其中要显示所有的标题，html页面中：
```
{% for file in files %}

  <p><a href="{{ url_for('file', file_id=file.id) }} " target="_black">{{ file.title}} </a></p>
  {% endfor %}
```
5.#获取所有与file_id对应的文章表数据：
```
file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item
```
对应file.html网页中显示所有内容：
```
<h1>{{ file_item['title']}}</h1>
<P>{{ file_item['created_time']}}</P>
<p>{{ file_item['content']}}</p>
```





