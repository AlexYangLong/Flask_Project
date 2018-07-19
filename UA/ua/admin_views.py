import re

import os
from flask import Blueprint, render_template, request, jsonify, session
from flask_restful import Resource

from ua.models import Admin
from utils import status_code
from utils.config import ROOT_DIR
from utils.exts import api

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin_list/', methods=['GET'])
def admin_list():
    return render_template('admin_list.html')


@admin_blueprint.route('/Admin_add/', methods=['GET'])
@admin_blueprint.route('/Admin_edit/', methods=['GET'])
def admin_addoredit():
    return render_template('admin_addoredit.html')


class AdminApi(Resource):
    def get(self, adid=None):
        if adid == 0:
            adid = session.get('adid')
            admin = Admin.query.filter(Admin.id == adid).first()
            res = status_code.SUCCESS
            res['data'] = admin.to_basic_dict()
            return jsonify(res)
        elif not adid:
            kw = request.args.get('kw')
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))
            if not kw:
                counter = Admin.query.filter(Admin.is_delete == False).count()
                paginations = Admin.query.filter(Admin.is_delete == False).order_by('-create_time').paginate(pn, ps)
                admins = paginations.items
            else:
                counter = Admin.query.filter(Admin.name.like('%' + kw + '%'), Admin.is_delete == False).count()
                paginations = Admin.query.filter(Admin.name.like('%' + kw + '%'), Admin.is_delete == False).order_by('-create_time').paginate(pn, ps)
                admins = paginations.items
            res = status_code.SUCCESS
            res['data_list'] = [admin.to_basic_dict() for admin in admins]
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            return jsonify(res)

        admin = Admin.query.filter(Admin.id == adid).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        if admin.is_delete:
            return jsonify(status_code.ADMIN_ACCOUNT_DELETED)
        res = status_code.SUCCESS
        res['data'] = admin.to_full_dict()
        return jsonify(res)

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not all([username, password, name, phone]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        admin = Admin.query.filter(Admin.phone == phone).first()
        if admin:
            return jsonify(status_code.ADMIN_PHONE_EXISTS)
        try:
            admin = Admin()
            admin.name = name
            admin.phone = phone
            admin.email = email
            admin.username = username
            admin.password = password
            admin.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def put(self, adid=None):
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not all([adid, username, password, name, phone]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        admin = Admin.query.filter(Admin.id == adid).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        if admin.is_delete:
            return jsonify(status_code.ADMIN_ACCOUNT_DELETED)
        try:
            admin.name = name
            admin.phone = phone
            admin.email = email
            admin.username = username
            admin.password = password
            admin.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def patch(self, adid=None):
        img_file = request.files.get('avatar')
        # 验证图片格式
        if not re.match(r'image/.*', img_file.mimetype):
            return jsonify({'code': 400, 'msg': '上传图片格式不正确，png/jpg/gif'})
        try:
            # 创建上传图片的文件夹
            file_dir = os.path.join(ROOT_DIR, 'static/upload/avatar')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_name = str(adid) + '.' + img_file.filename.split('.')[-1]
            img_path = os.path.join(file_dir, file_name)
            # 保存图片到服务器本地
            img_file.save(img_path)
        except BaseException as e:
            print(e)
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '上传图片失败'})

        admin = Admin.query.filter(Admin.id == adid).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        try:
            admin.avatar = 'avatar/' + file_name
            admin.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def delete(self, adid=None):
        if not adid:
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        admin = Admin.query.filter(Admin.id == adid).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        try:
            admin.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(AdminApi, '/api/admin/', '/api/admin/<int:adid>/')
