from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from exts import db
from models import User, Question, Answer
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app=app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tel_num = request.form.get('tel_num')
        password = request.form.get('password')
        user = User.query.filter(User.tel_num == tel_num, User.password == password).first()
        if user:
            # 登录成功，设置session，并设置存活时间
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号或密码错误！请重试！'

    return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        tel_num = request.form.get('tel_num')
        username = request.form.get('username')
        password = request.form.get('password')
        re_passwd = request.form.get('re_passwd')

        # 验证两次输入的密码是否一致
        if password != re_passwd:
            return '两次输入的密码不一致！请重新输入！'

        # 验证手机号是否已经被注册过了
        user = User.query.filter(User.tel_num == tel_num).first()
        if user:
            return '该手机号已被注册！请更换手机号！'

        # 验证通过，开始注册
        user = User(tel_num=tel_num, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        # 注册成功，跳转到登录页面
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    # 清除session
    session.pop('user_id')
    # del session['user_id']
    # session.clear()

    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        ques = Question(title=title, content=content)

        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        ques.author = user

        db.session.add(ques)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('question.html')


@app.route('/detail/<q_id>/', methods=['GET'])
def detail(q_id):
    ques = Question.query.filter(Question.id == q_id).first()
    return render_template('detail.html', question=ques)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    answer_con = request.form.get('answer_con')
    ques_id = request.form.get('ques_id')
    answer = Answer(content=answer_con)

    user = User.query.filter(User.id == session.get('user_id')).first()
    answer.author = user

    ques = Question.query.filter(Question.id == ques_id).first()
    answer.question = ques

    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', q_id=ques_id))


@app.route('/search/')
def search():
    search_key = request.args.get('kw')
    context = {
        'kw': search_key,
        'questions': Question.query.filter(Question.title.like('%' + search_key + '%')).all()
    }
    return render_template('search.html', **context)


@app.context_processor
def get_some_info():
    """
    钩子函数，context_processor 在视图执行过程中执行，主要是用来获取一些需要传入模板的信息
    :return:
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
