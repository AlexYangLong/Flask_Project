from flask import Blueprint

from utils.exts import db

db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/create_tb/')
def create_tb():
    db.create_all()
    return '创建数据库表成功'


@db_blueprint.route('/drop_tb/')
def drop_tb():
    db.drop_all()
    return '删除数据库表成功'
