from flask import Blueprint, render_template, request, jsonify, session
from flask_restful import Resource

from ua.models import User
from utils import status_code
from utils.exts import api

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/user_list/', methods=['GET'])
def user_list():
    return render_template('user/user_list.html')


@user_blueprint.route('/user_add/', methods=['GET'])
@user_blueprint.route('/user_edit/', methods=['GET'])
def user_addoredit():
    return render_template('user/user_addoredit.html')


class UserApi(Resource):
    def get(self, uid=None):
        adid = session.get('adid')

        if uid == 0:
            user_list = User.query.filter(User.is_delete == False, User.admin_id == adid).order_by('-create_time')
            res = status_code.SUCCESS
            res['data_list'] = [user.to_basic_dict() for user in user_list]
            return jsonify(res)

        if not uid:
            kw = request.args.get('sk')
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))
            if not kw:
                counter = User.query.filter(User.is_delete == False, User.admin_id == adid).count()
                user_list = User.query.filter(User.is_delete == False, User.admin_id == adid).order_by('-create_time')
                paginations = user_list.paginate(pn, ps)
                users = paginations.items
            else:
                counter = User.query.filter(User.name.like('%' + kw + '%'), User.is_delete == False, User.admin_id == adid).count()
                paginations = User.query.filter(User.name.like('%' + kw + '%'), User.is_delete == False, User.admin_id == adid).order_by('-create_time').paginate(pn, ps)
                users = paginations.items
            res = status_code.SUCCESS
            res['data_list'] = [user.to_basic_dict() for user in users]
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            return jsonify(res)

        user = User.query.filter(User.id == uid).first()
        if not user:
            return jsonify(status_code.USER_NOT_EXISTS)
        if user.admin_id != adid:
            return jsonify(status_code.ADMIN_AUTHORITY_ERROR)
        if user.is_delete:
            return jsonify(status_code.USER_DELETED)
        res = status_code.SUCCESS
        res['data'] = user.to_full_dict()
        return jsonify(res)

    def post(self):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        # reason = request.form.get('reason')
        adid = session.get('adid')

        if not all([name, phone]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        user = User.query.filter(User.phone == phone).first()
        if user:
            return jsonify(status_code.USER_PHONE_EXISTS)
        try:
            user = User()
            user.name = name
            user.phone = phone
            user.email = email
            user.address = address
            # user.reason = reason
            user.admin_id = adid
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def put(self, uid=None):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        # reason = request.form.get('reason')
        if not all([uid, name, phone]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        user = User.query.filter(User.id == uid).first()
        if not user:
            return jsonify(status_code.USER_NOT_EXISTS)
        if user.is_delete:
            return jsonify(status_code.USER_DELETED)
        try:
            user.name = name
            user.phone = phone
            user.email = email
            user.address = address
            # user.reason = reason
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def delete(self, uid=None):
        if not uid:
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        user = User.query.filter(User.id == uid).first()
        if not user:
            return jsonify(status_code.USER_NOT_EXISTS)
        try:
            user.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(UserApi, '/api/user/', '/api/user/<int:uid>/')
