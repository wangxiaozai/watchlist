from flask import Flask,render_template
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import os
import sys
from flask import Flask

WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统， 使用三个斜线
      prefix = 'sqlite:///'
else: # 否则使用四个斜线
      prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model): # 表名将会是 user（ 自动生成， 小写处理）
      id = db.Column(db.Integer, primary_key=True) # 主键
      name = db.Column(db.String(20)) # 名字
class Movie(db.Model): # 表名将会是 movie
      id = db.Column(db.Integer, primary_key=True) # 主键
      title = db.Column(db.String(60)) # 电影标题
      year = db.Column(db.String(4)) # 电影年份

import click
@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
      """Initialize the database."""
      if drop: # 判断是否输入了选项
            db.drop_all()
      db.create_all()
      click.echo('Initialized database.') # 输出提示信息

@app.route('/')
def index():
      movies = Movie.query.all()
      return render_template('index.html', movies=movies)

import click
@app.cli.command()
def forge():
      """Generate fake data."""
      db.create_all()
      # 全局的两个变量移动到这个函数内
      name = 'Wang xiaozai'
      movies = [
            {'title': 'My Neighbor Totoro', 'year': '1988'},
            {'title': 'Dead Poets Society', 'year': '1989'},
            {'title': 'A Perfect World', 'year': '1993'},
            {'title': 'Leon', 'year': '1994'},
            {'title': 'Mahjong', 'year': '1996'},
            {'title': 'Swallowtail Butterfly', 'year': '1996'},
            {'title': 'King of Comedy', 'year': '1999'},
            {'title': 'Devils on the Doorstep', 'year': '1999'},
            {'title': 'WALL-E', 'year': '2008'},
            {'title': 'The Pork of Music', 'year': '2012'},
      ]
      user = User(name=name)
      db.session.add(user)
      for m in movies:
            movie = Movie(title=m['title'], year=m['year'])
            db.session.add(movie)

      db.session.commit()
      click.echo('Done.')

@app.context_processor
def inject_user(): # 函数名可以随意修改
      user = User.query.first()
      return dict(user=user) # 需要返回字典， 等同于return {'user': user}

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
      user = User.query.first()
      return render_template('404.html', user=user), 404 # 返回模板和状态码