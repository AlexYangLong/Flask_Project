from flask import Blueprint

from cms.models import db

db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/create_tb/')
def create_tb():
    try:
        db.create_all()
        return '创建数据表成功'
    except BaseException as e:
        print(e)
        return '创建数据表失败'


@db_blueprint.route('/drop_tb/')
def drop_tb():
    try:
        db.drop_all()
        return '删除数据表成功'
    except BaseException as e:
        print(e)
        return '删除数据表失败'
