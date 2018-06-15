from flask import Blueprint, request, render_template, session

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index/')
def index():
    if request.method == 'GET':
        return render_template('index.html')


@index_blueprint.route('/head/')
def head():
    if request.method == 'GET':
        name = session.get('admin_name')
        return render_template('head.html', name=name)


@index_blueprint.route('/left/')
def left():
    if request.method == 'GET':
        return render_template('left.html')
