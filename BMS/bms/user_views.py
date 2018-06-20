from flask import Blueprint, request, render_template, jsonify, session
from flask_restful import Resource

from bms.models import Admin
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/user_list/')
@login_required
def user_list():
    if request.method == 'GET':
        return render_template('user/users.html')


@user_blueprint.route('/user_add/')
@login_required
def user_add():
    if request.method == 'GET':
        return render_template('user/add_edit.html')


@user_blueprint.route('/user_edit/')
@login_required
def user_edit():
    if request.method == 'GET':
        return render_template('user/add_edit.html')


class UserApi(Resource):
    def get(self, uid=None):
        if uid is None:
            pn = int(request.args.get('pn', 1))
            ps = 10
            paginations = Admin.query.order_by('-create_time').paginate(pn, ps)
            stus = paginations.items

            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['data_list'] = [stu.to_dict() for stu in stus]
            return jsonify(res)

        if uid == 0:
            user = Admin.query.get(session.get('admin_id'))
            if user:
                res = status_code.SUCCESS
                res['data'] = user.to_dict()
                return jsonify(res)

            return jsonify(status_code.USER_NOT_EXISTS)

        stu = Admin.query.get(uid)
        if stu:
            res = status_code.SUCCESS
            res['data'] = stu.to_dict()
            return jsonify(res)

        return jsonify(status_code.USER_NOT_EXISTS)

    def post(self, uid=None):
        username = request.form.get('username')
        real_name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')

        if not all([username, real_name, password, role]):
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not uid:
            user = Admin.query.filter_by(username=username).first()
            if user:
                return jsonify(status_code.USER_USERNAME_EXISTED)

            user = Admin(username=username, name=real_name, password=password)
            user.role_id = role
            # user.username = username
            # user.name = real_name
            # user.password = password
            user.add_update()
        else:
            user = Admin.query.get(uid)
            user.username = username
            user.name = real_name
            user.password = password
            user.role_id = role
            user.add_update()

        res = status_code.SUCCESS
        res['data'] = user.to_dict()
        return jsonify(res)

    def delete(self, uid):
        if uid:
            user = Admin.query.get(uid)
            if not user:
                return jsonify(status_code.USER_NOT_EXISTS)

            user.delete()
            return jsonify(status_code.SUCCESS)

        return jsonify(status_code.PARAMS_NOT_COMPLETE)


api.add_resource(UserApi, '/api/user/', '/api/user/<int:uid>/')