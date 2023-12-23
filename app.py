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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import render_template, send_file

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


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

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(240))  # 姓名
    gender = db.Column(db.String(20))  # 性别
    country = db.Column(db.String(120))  # 国家


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
# 全局的变量移动到这个函数内
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
    {'title': '霍元甲', 'year': '2006', 'country': '中国', 'type': '动作', 'box': '1.76亿'},
    {'title': '战狼', 'year': '2015', 'country': '中国', 'type': '战争', 'box': '8.43亿'},
    {'title': '红海行动', 'year': '2018', 'country': '中国', 'type': '战争', 'box': '36.5亿'},
    {'title': '唐人街探案', 'year': '2015', 'country': '中国', 'type': '喜剧', 'box': '12.8亿'},
    {'title': '大话西游之大圣娶亲', 'year': '1995', 'country': '香港', 'type': '喜剧', 'box': '7.8亿'},
        {'title': '少年派的奇幻漂流', 'year': '2012', 'country': '美国', 'type': '冒险', 'box': '9.01亿'},
        {'title': '完美陌生人', 'year': '2016', 'country': '意大利', 'type': '喜剧', 'box': '8.86亿'},
        {'title': '钢琴师', 'year': '2002', 'country': '法国', 'type': '剧情', 'box': '2.65亿'},
        {'title': '心灵捕手', 'year': '1998', 'country': '美国', 'type': '剧情', 'box': '3.21亿'},
        {'title': '疯狂的石头', 'year': '2006', 'country': '中国', 'type': '喜剧', 'box': '1.61亿'},
        {'title': '当幸福来敲门', 'year': '2006', 'country': '美国', 'type': '剧情', 'box': '8.3亿'},
        {'title': '怦然心动', 'year': '2010', 'country': '美国', 'type': '喜剧', 'box': '4.68亿'},
        {'title': '摔跤吧！爸爸', 'year': '2016', 'country': '印度', 'type': '剧情', 'box': '4.37亿'},
        {'title': '放牛班的春天', 'year': '2004', 'country': '法国', 'type': '剧情', 'box': '3.05亿'},
        {'title': '乱世佳人', 'year': '1939', 'country': '美国', 'type': '剧情', 'box': '39.2亿'},
        {'title': '千与千寻', 'year': '2001', 'country': '日本', 'type': '动画', 'box': '25.03亿'},
        {'title': '教父', 'year': '1972', 'country': '美国', 'type': '剧情', 'box': '2.46亿'},
        {'title': '指环王：王者归来', 'year': '2003', 'country': '美国', 'type': '奇幻', 'box': '7.57亿'},
        {'title': '阿甘正传', 'year': '1994', 'country': '美国', 'type': '剧情', 'box': '6.71亿'},
        {'title': '泰坦尼克号', 'year': '1997', 'country': '美国', 'type': '剧情', 'box': '19.76亿'},
        {'title': '盗梦空间', 'year': '2010', 'country': '美国', 'type': '科幻', 'box': '14.68亿'},
        {'title': '楚门的世界', 'year': '1998', 'country': '美国', 'type': '剧情', 'box': '6.94亿'},
        {'title': '海上钢琴师', 'year': '1998', 'country': '意大利', 'type': '剧情', 'box': '2.4亿'},
        {'title': '机器人总动员', 'year': '2008', 'country': '美国', 'type': '动画', 'box': '8.53亿'},
        {'title': 'V字仇杀队', 'year': '2005', 'country': '美国', 'type': '动作', 'box': '1.33亿'},
        {'title': '西游伏妖篇', 'year': '2017', 'country': '中国', 'type': '奇幻', 'box': '16.8亿'},
        {'title': '寻龙诀', 'year': '2015', 'country': '中国', 'type': '奇幻', 'box': '16.75亿'},
        {'title': '战狼', 'year': '2015', 'country': '中国', 'type': '战争', 'box': '14.72亿'},
        {'title': '碟中谍5：神秘国度', 'year': '2015', 'country': '美国', 'type': '动作', 'box': '13.86亿'},
        {'title': '建军大业', 'year': '2017', 'country': '中国', 'type': '历史', 'box': '13.62亿'},
        {'title': '疯狂动物城', 'year': '2016', 'country': '美国', 'type': '动画', 'box': '12.68亿'},
        {'title': '卧底巨星', 'year': '2017', 'country': '中国', 'type': '喜剧', 'box': '12.6亿'},
    ]

    players = [
        {'name':'吴京','gender':'男','country':'中国'},
        {'name': '饺子', 'gender': '男', 'country': '中国'},
        {'name': '屈楚萧', 'gender': '男', 'country': '中国'},
        {'name': '郭帆', 'gender': '男', 'country': '中国'},
        {'name': '乔罗素', 'gender': '男', 'country': '美国'},
        {"name": "小罗伯特·唐尼", "gender": "男", "country": "美国"},
        {"name": "克里斯·埃文斯", "gender": "男", "country": "美国"},
        {"name": "林超贤", "gender": "男", "country": "中国"},
        {"name": "张译", "gender": "男", "country": "中国"},
        {"name": "黄景瑜", "gender": "男", "country": "中国"},
        {"name": "陈思诚", "gender": "男", "country": "中国"},
        {"name": "王宝强", "gender": "男", "country": "中国"},
        {"name": "刘昊然", "gender": "男", "country": "中国"},
        {"name": "文牧野", "gender": "男", "country": "中国"},
        {"name": "徐峥", "gender": "男", "country": "中国"},
        {"name": "刘伟强", "gender": "男", "country": "中国"},
        {"name": "张涵予", "gender": "男", "country": "中国"},
        {"name": "F·加里·格雷", "gender": "男", "country": "美国"},
        {"name": "范·迪塞尔", "gender": "男", "country": "美国"},
        {"name": "杰森·斯坦森", "gender": "男", "country": "美国"},
        {"name": "闫非", "gender": "男", "country": "中国"},
        {"name": "沈腾", "gender": "男", "country": "中国"},
        {"name": "安东尼·罗素", "gender": "男", "country": "美国"},
        {"name": "克里斯·海姆斯沃斯", "gender": "男", "country": "美国"},
        {"name": "许诚毅", "gender": "男", "country": "中国"},
        {"name": "梁朝伟", "gender": "男", "country": "中国"},
        {"name": "白百何", "gender": "女", "country": "中国"},
        {"name": "井柏然", "gender": "男", "country": "中国"},
        {"name": "管虎", "gender": "男", "country": "中国"},
        {"name": "王千源", "gender": "男", "country": "中国"},
        {"name": "姜武", "gender": "男", "country": "中国"},
        {"name": "宁浩", "gender": "男", "country": "中国"},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'], country=m['country'], type=m['type'],box=m['box'])
        db.session.add(movie)
    for m in players:
        player = Player(name=m['name'], gender=m['gender'], country=m['country'])
        db.session.add(player)
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
        country = request.form.get('country')
        type = request.form.get('type')
        box = request.form.get('box')
# 验证数据
        if not title or not year or not country or not type or not box or len(year) > 4 or len(title)> 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
# 保存表单数据到数据库
        movie = Movie(title=title, year=year, country=country, type=type, box=box) # 创建记录
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
        country = request.form['country']
        type = request.form['type']
        box = request.form['box']
        if not title or not year or not country or not type or not box or len(year) > 4 or len(title)> 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
# 重定向回对应的编辑页面
        movie.title = title # 更新标题
        movie.year = year # 更新年份
        movie.country = country  # 更新国家
        movie.type = type  # 更新类型
        movie.box = box  # 更新票房
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

@app.route('/search', methods=['POST'])
def search():
    movies = Movie.query.all()
    search_term = request.form['searchTerm'].lower()
    results = [movie for movie in movies if search_term in movie.title.lower()]
    return render_template('index.html', movies=results)

@app.route('/cate', methods=['POST'])
def cate():
    movies = Movie.query.all()
    search_term = request.form['searchTerm'].lower()
    results = [movie for movie in movies if search_term in movie.type.lower()]
    return render_template('index.html', movies=results)

@app.route('/act', methods=['GET', 'POST'])
def act():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        name = request.form.get('name')  # 传入表单对应输入字段的name 值
        gender = request.form.get('gender')
        country = request.form.get('country')

        # 验证数据
        if not name or not gender or not country:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('act'))  # 重定向回主页
        # 保存表单数据到数据库
        player = Player(name=name, gender=gender, country=country)  # 创建记录
        db.session.add(player)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('act'))  # 重定向回主页
    user = User.query.first()
    players = Player.query.all()
    return render_template('actor.html', user=user, players=players)

@app.route('/player/deleteact/<int:player_id>', methods=['POST']) #限定只接受 POST 请求
def deleteact(player_id):
    player = Player.query.get_or_404(player_id) # 获取电影记录
    db.session.delete(player) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('act')) # 重定向回主页

@app.route('/player/editact/<int:player_id>', methods=['GET', 'POST'])
def editact(player_id):
    player = Player.query.get_or_404(player_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        name = request.form['name']
        gender = request.form['gender']
        country = request.form['country']
        if not name or not gender or not country:
            flash('Invalid input.')
            return redirect(url_for('editact', player_id=player_id))
# 重定向回对应的编辑页面
        player.name = name # 更新标题
        player.gender = gender # 更新年份
        player.country = country  # 更新国家
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('act')) # 重定向回主页
    return render_template('editact.html', player=player) # 传入被编辑的电影记录

@app.route('/searchactor', methods=['POST'])
def searchactor():
    players = Player.query.all()
    search_term = request.form['searchTerm'].lower()
    results = [player for player in players if search_term in player.name.lower()]  # 使用列表推导式筛选匹配的演员
    return render_template('actor.html', players=results)



@app.route('/visualization', methods=['GET'])
def visualize():
    import plotly.graph_objs as go
    # 生成票房数据可视化图表
    top_movies = Movie.query.order_by(Movie.box.desc()).limit(10).all()
    titles = [movie.title for movie in top_movies]
    box_office = [float(movie.box[:-1]) for movie in top_movies]  # 去除"亿"并转换为浮点数

    # 创建水平柱状图
    fig = go.Figure(go.Bar(
        x=box_office,
        y=titles,
        orientation='h',
        marker_color='skyblue'  # 设置颜色为天蓝色
    ))

    # 设置布局
    fig.update_layout(
        yaxis=dict(tickfont=dict(size=14))  # 设置纵轴坐标标签字体大小
    )

    # 将图表可视化为HTML页面
    graph_html = fig.to_html(full_html=False, default_height=600, default_width=800)

    # 渲染可视化页面，并传入图表HTML字符串
    return render_template('visualization.html', graph_html=graph_html)

@app.route('/box-office-analysis', methods=['GET'])
def box_office_analysis():
    import plotly.graph_objs as go

    # 从数据库中获取不同类型电影的票房数据
    type_box_office = db.session.query(Movie.type, db.func.sum(db.func.replace(Movie.box, '亿', '').cast(db.Float))).group_by(Movie.type).all()
    types = [record[0] for record in type_box_office]
    box_office_by_type = [record[1] for record in type_box_office]

    # 创建水平柱状图
    fig = go.Figure(go.Bar(
        x=box_office_by_type,
        y=types,
        orientation='h',
        marker_color='skyblue'  # 设置颜色为天蓝色
    ))

    # 设置布局
    fig.update_layout(
        title='不同电影类别的票房分析',
        xaxis_title='票房（亿元）',
        yaxis_title='电影类别',
        yaxis=dict(tickfont=dict(size=14))  # 设置纵轴坐标标签字体大小
    )

    # 将图表可视化为HTML页面
    graph_html = fig.to_html(full_html=False, default_height=600, default_width=800)

    # 渲染可视化页面，并传入图表HTML字符串
    return render_template('box_office_analysis.html', graph_html=graph_html)
