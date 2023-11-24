from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
from flask import request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
from flask_login import LoginManager
from flask_login import login_required, current_user
from flask_login import login_required, logout_user
from flask_login import login_user
from flask_login import UserMixin

WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统， 使用三个斜线
    prefix = 'sqlite:///'
else: # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 设置密钥
app.secret_key = '123456zaq'
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(128)) # 密码散列值
    def set_password(self, password): # 用来设置密码的方法， 接受密码作为参数
        self.password_hash = generate_password_hash(password) #将生成的密码保持到对应字段
    def validate_password(self, password): # 用于验证密码的方法， 接受密码作为参数
        return check_password_hash(self.password_hash, password)
# 返回布尔值

class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(240)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份
    country = db.Column(db.String(120)) # 出品国家
    type = db.Column(db.String(120))#电影类型
    box = db.Column(db.String(50))#电影票房

import click
@app.cli.command()
@click.option('--username', prompt=True, help='The username usedto login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password) # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password) # 设置密码
        db.session.add(user)
    db.session.commit() # 提交数据库会话
    click.echo('Done.')

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

import click
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
# 全局的两个变量移动到这个函数内
    name = '旺小仔'
    movies = [
    {'title': '战狼2', 'year': '2017', 'country': '中国', 'type': '战争', 'box': '56.84亿'},
    {'title': '哪吒之魔童降世', 'year': '2019', 'country': '中国', 'type': '动画', 'box': '50.15亿'},
    {'title': '流浪地球', 'year': '2019', 'country': '中国', 'type': '科幻', 'box': '46.86亿'},
    {'title': '复仇者联盟4', 'year': '2019', 'country': '美国', 'type': '科幻', 'box': '42.5亿'},
    {'title': '红海行动', 'year': '2018', 'country': '中国', 'type': '战争', 'box': '36.5亿'},
    {'title': '唐人街探案2', 'year': '2018', 'country': '中国', 'type': '喜剧', 'box': '33.97亿'},
    {'title': '我不是药神', 'year': '2018', 'country': '中国', 'type': '喜剧', 'box': '31亿'},
    {'title': '中国机长', 'year': '2019', 'country': '中国', 'type': '剧情', 'box': '29.12亿'},
    {'title': '速度与激情8', 'year': '2017', 'country': '美国', 'type': '动作', 'box': '26.7亿'},
    {'title': '西虹市首富', 'year': '2018', 'country': '中国', 'type': '喜剧', 'box': '25.47亿'},
    {'title': '复仇者联盟3', 'year': '2018', 'country': '美国', 'type': '科幻', 'box': '23.9亿'},
    {'title': '捉妖记2', 'year': '2018', 'country': '中国', 'type': '喜剧', 'box': '22.37亿'},
    {'title': '八佰', 'year': '2020', 'country': '中国', 'type': '战争', 'box': '30.10亿'},
    {'title': '姜子牙', 'year': '2020', 'country': '中国', 'type': '动画', 'box': '16.02亿'},
    {'title': '我和我的家乡', 'year': '2020', 'country': '中国', 'type': '剧情', 'box': '28.29亿'},
    {'title': '你好，李焕英', 'year': '2021', 'country': '中国', 'type': '喜剧', 'box': '54.13亿'},
    {'title': '长津湖', 'year': '2021', 'country': '中国', 'type': '战争', 'box': '53.48亿'},
    {'title': '速度与激情9', 'year': '2021', 'country': '美国', 'type': '动作', 'box': '13.92亿'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'], country=m['country'], type=m['type'],box=m['box'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典， 等同于return {'user': user}

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    return render_template('404.html'), 404 # 返回模板和状态码


login_manager = LoginManager(app) # 实例化扩展类
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数， 接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
# 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user) # 登入用户
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页
        flash('Invalid username or password.') # 如果验证失败， 显示错误消息
        return redirect(url_for('login')) # 重定向回登录页面
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
# current_user 会返回当前登录用户的数据库记录对象
# 等同于下面的用法
# user = User.query.first()
# user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        if not current_user.is_authenticated: # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向回主页
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
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required # 用于视图保护， 后面会详细介绍
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

@app.route('/movie/delete/<int:movie_id>', methods=['POST']) #限定只接受 POST 请求
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页






