from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_restful import Resource

from ua.models import Admin, LoginRecord
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@auth_blueprint.route('/logout/', methods=['GET'])
@login_required
def logout():
    del session['adid']
    return redirect(url_for('auth.login'))


class AuthApi(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if request.headers.environ.get('HTTP_X_FORWARDED_FOR'):
            ip = request.headers.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.headers.environ['REMOTE_ADDR'] + ':' + str(request.headers.environ['REMOTE_PORT'])

        if not all([username, password]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})

        admin = Admin.query.filter(Admin.username == username).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        if admin.is_delete:
            return jsonify(status_code.ADMIN_ACCOUNT_DELETED)
        if not admin.check_pwd(password):
            return jsonify(status_code.ADMIN_AUTH_PASSWORD_ERROR)
        try:
            lr = LoginRecord()
            lr.admin_id = admin.id
            lr.login_ip = ip
            lr.add_update()
            session['adid'] = admin.id
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.ADMIN_LOGIN_RECORD_INSERT_ERROR)


api.add_resource(AuthApi, '/api/auth/')
