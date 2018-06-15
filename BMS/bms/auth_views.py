from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_restful import Resource, reqparse

from bms.models import Admin, Authority, db, Role
from utils.decorators import login_required
from utils.exts import api

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')


@auth_blueprint.route('/logout/')
@login_required
def logout():
    if request.method == 'GET':
        del session['admin_id']
        del session['admin_name']
        return redirect(url_for('index.index'))


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
api.add_resource(AuthApi, '/auth_api/authenticate/')


@auth_blueprint.route('/auth_list/')
def auth_list():
    if request.method == 'GET':
        return render_template('auth/permissions.html')


class AuthorityApi(Resource):
    def get(self, aid=None):
        if not aid:
            auths = Authority.query.all()
            return {
                'code': 200,
                'msg': '请求成功',
                'data_list': [auth.to_dict() for auth in auths]
            }

        auth = Authority.query.get(aid)
        if auth:
            return {
                'code': 200,
                'msg': '请求成功',
                'result': auth.to_dict()
            }
        return {
            'code': 404,
            'msg': '不存在该id的权限'
        }

    def post(self):
        # 获取请求
        parser = reqparse.RequestParser()
        # 在请求中解析需要的参数，type表示该参数的类型，location表示存在该参数的域，help表示在解析出现错误时被触发，它将会被作为错误信息给呈现出来，没有指定则返回错误本身信息
        parser.add_argument('aid', type=int, location=['form', 'json'], help='Id cannot be blank!')
        parser.add_argument('name', type=str, required=True, location=['form', 'json'], help='Name cannot be blank!')
        # 解析参数
        args = parser.parse_args()

        if not args.get('name'):
            return {
                'code': 501,
                'msg': '参数传递错误'
            }

        if not args.get('aid'):
            auth = Authority()
            auth.name = args.get('name')
        else:
            auth = Authority.query.get(args.get('aid'))
            auth.name = args.get('name')
        db.session.add(auth)
        db.session.commit()
        return {
            'code': 200,
            'msg': '请求成功',
            'data': auth.to_dict()
        }

    def delete(self, aid):
        if aid:
            auth = Authority.query.get(aid)
            if not auth:
                return {
                    'code': 404,
                    'msg': '不存在该id的权限'
                }
            db.session.delete(auth)
            db.session.commit()
            return {
                'code': 200,
                'msg': '删除成功',
                'data': auth.to_dict()
            }

        return {
            'code': 500,
            'msg': '请求错误,需要参数id'
        }


api.add_resource(AuthorityApi, '/auth_api/authority/', '/auth_api/authority/<int:aid>/')


@auth_blueprint.route('/role_list/')
def role_list():
    if request.method == 'GET':
        return render_template('auth/permissions.html')


class RoleApi(Resource):
    def get(self, rid=None):
        if not rid:
            roles = Role.query.all()
            return {
                'code': 200,
                'msg': '请求成功',
                'data_list': [role.to_dict() for role in roles]
            }

        role = Role.query.get(rid)
        if role:
            return {
                'code': 200,
                'msg': '请求成功',
                'result': role.to_dict()
            }
        return {
            'code': 404,
            'msg': '不存在该id的角色'
        }

    def post(self):
        # 获取请求
        parser = reqparse.RequestParser()
        # 在请求中解析需要的参数，type表示该参数的类型，location表示存在该参数的域，help表示在解析出现错误时被触发，它将会被作为错误信息给呈现出来，没有指定则返回错误本身信息
        parser.add_argument('rid', type=int, location=['form', 'json'], help='Id cannot be blank!')
        parser.add_argument('name', type=str, required=True, location=['form', 'json'], help='Name cannot be blank!')
        # 解析参数
        args = parser.parse_args()

        if not args.get('name'):
            return {
                'code': 501,
                'msg': '参数传递错误'
            }

        if not args.get('rid'):
            role = Role()
            role.name = args.get('name')
        else:
            role = Role.query.get(args.get('rid'))
            role.name = args.get('name')
        db.session.add(role)
        db.session.commit()
        return {
            'code': 200,
            'msg': '请求成功',
            'data': role.to_dict()
        }

    def delete(self, rid):
        if rid:
            role = Role.query.get(rid)
            if not role:
                return {
                    'code': 404,
                    'msg': '不存在该id的角色'
                }
            db.session.delete(role)
            db.session.commit()
            return {
                'code': 200,
                'msg': '删除成功',
                'data': role.to_dict()
            }

        return {
            'code': 500,
            'msg': '请求错误,需要参数id'
        }


api.add_resource(RoleApi, '/auth_api/role/', '/auth_api/role/<int:rid>/')