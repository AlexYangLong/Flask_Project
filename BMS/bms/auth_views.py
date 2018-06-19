from flask import Blueprint, request, render_template, session, redirect, url_for, jsonify
from flask_restful import Resource

from bms.models import Admin
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('auth/login.html')


@auth_blueprint.route('/logout/', methods=['GET'])
@login_required
def logout():
    del session['admin_id']
    del session['admin_name']
    return redirect(url_for('index.index'))


class AuthApi(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            return jsonify(status_code.USER_PARAMS_NOT_COMPLETE)

        admin = Admin.query.filter_by(username=username, password=password).first()
        if not admin:
            return jsonify(status_code.USER_USERNAME_OR_PASSWORD_ERROR)

        session['admin_id'] = admin.id
        session['admin_name'] = admin.name
        return jsonify(status_code.SUCCESS)


# 绑定url对应的Api类
api.add_resource(AuthApi, '/auth_api/')
