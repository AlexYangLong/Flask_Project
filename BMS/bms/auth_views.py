from flask import Blueprint, request, render_template, session
from flask_restful import Resource, reqparse

from bms.models import Admin
from utils.exts import api

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')


class AuthApi(Resource):
    def post(self):
        # 获取请求
        parser = reqparse.RequestParser()
        # 在请求中解析需要的参数，type表示该参数的类型，location表示存在该参数的域，help表示在解析出现错误时被触发，它将会被作为错误信息给呈现出来，没有指定则返回错误本身信息
        parser.add_argument('username', type=str, location=['form', 'json'], help='username cannot be blank!')
        parser.add_argument('password', type=str, location=['form', 'json'], help='password cannot be blank!')
        # 解析参数
        args = parser.parse_args()

        if not all([args.get('username'), args.get('password')]):
            return {
                'code': 500,
                'msg': '参数传递错误'
            }
        username = args.get('username')
        password = args.get('password')
        admin = Admin.query.filter_by(username=username, password=password).first()
        if not admin:
            return {
                'code': 404,
                'msg': '用户名或密码错误'
            }
        session['admin_id'] = admin.id
        session['admin_name'] = admin.name
        return {
            'code': 200,
            'msg': '认证成功',
            'data': admin.to_dict()
        }


# 绑定url对应的Api类
api.add_resource(AuthApi, '/api/auth/')
