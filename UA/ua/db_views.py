from flask import Blueprint, jsonify

from ua.models import db, Admin
from utils import status_code

db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/create_tb/', methods=['GET'])
def create_tb():
    db.create_all()
    return '创建数据表成功'


@db_blueprint.route('/drop_tb/', methods=['GET'])
def drop_tb():
    db.drop_all()
    return '删除数据表成功'


@db_blueprint.route('/init_tb/', methods=['GET'])
def init_tb():
    try:
        admin = Admin()
        admin.username = 'sa'
        admin.password = 'admin'
        admin.name = 'AlexYang'
        admin.phone = '18408260044'
        admin.email = 'admin@admin.com'
        admin.add_update()
        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)
