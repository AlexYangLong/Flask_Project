from flask import Blueprint, render_template

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@index_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')
