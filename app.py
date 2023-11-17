import click
from flask import Flask,render_template,request, url_for, redirect, flash
from flask_sqlalchemy  import SQLAlchemy # 导入扩展类
import os
import sys
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统， 使用三个斜线
      prefix = 'sqlite:///'
else: # 否则使用四个斜线
      prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app)

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
      """Initialize the database."""
      if drop: # 判断是否输入了选项
            db.drop_all()
      db.create_all()
      click.echo('Initialized database.') # 输出提示信息

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
# 返回布尔值
class Movie(db.Model): # 表名将会是 movie
      id = db.Column(db.Integer, primary_key=True) # 主键
      title = db.Column(db.String(60)) # 电影标题
      year = db.Column(db.String(4)) # 电影年份

import click
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
@app.cli.command()
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user(): # 函数名可以随意修改
      user = User.query.first()
      return dict(user=user) # 需要返回字典， 等同于return {'user': user}

@app.errorhandler(404)
def page_not_found(e):
      return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
      if request.method == 'POST': # 判断是否是 POST 请求
# 获取表单数据
            title = request.form.get('title') # 传入表单对应输入字段的name 值
            year = request.form.get('year')
# 验证数据
            if not title or not year or len(year) > 4 or len(title)> 60:
                  flash('Invalid input.') # 显示错误提示
                  return redirect(url_for('index')) # 重定向回主页

# 保存表单数据到数据库
            movie = Movie(title=title, year=year) # 创建记录
            db.session.add(movie) # 添加到数据库会话
            db.session.commit() # 提交数据库会话
            flash('Item created.') # 显示成功创建的提示
            return redirect(url_for('index')) # 重定向回主页

      #user = User.query.first()
      movies = Movie.query.all()
      return render_template('index.html', user=user, movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title)> 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
# 重定向回对应的编辑页面
        movie.title = title # 更新标题
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页
    return render_template('edit.html', movie=movie) # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST']) #限定只接受 POST 请求f
def delete(movie_id):
      movie = Movie.query.get_or_404(movie_id) # 获取电影记录
      db.session.delete(movie) # 删除对应的记录
      db.session.commit() # 提交数据库会话
      flash('Item deleted.')
      return redirect(url_for('index')) # 重定向回主页




