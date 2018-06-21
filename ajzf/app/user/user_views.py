import re

import os
from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from sqlalchemy import or_

from app.models import User, db
from utils import status_code
from utils import common
from utils.decorators import login_required

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    phone = request.form.get('phone')
    username = request.form.get('username')
    password = request.form.get('password')
    repasswd = request.form.get('password2')

    # 验证数据完整性
    if not all([phone, username, password, repasswd]):
        return jsonify(status_code.USER_PARAMS_NOT_COMPLETE)
    # 验证手机号码
    if not re.match(r'^1[34578][0-9]{9}$', phone):
        return jsonify(status_code.USER_PHONE_ERROR)
    # 验证两次密码是否一致
    if password != repasswd:
        return jsonify(status_code.USER_TWICE_PASSWORD_DIFFERENT)
    # 验证手机是否存在
    user = User.query.filter_by(phone=phone).first()
    if user:
        return jsonify(status_code.USER_PHONE_REGISTERED)
    # 验证用户名
    user = User.query.filter_by(name=username).first()
    if user:
        return jsonify(status_code.USER_USERNAME_EXISTED)

    user = User()
    user.phone = phone
    user.name = username
    user.password = password

    user.add_update()
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    # 验证请求数据完整性
    if not all([mobile, password]):
        return jsonify(status_code.USER_PARAMS_NOT_COMPLETE)
    # 查询用户
    user = User.query.filter(or_(User.phone == mobile, User.name == mobile)).first()
    if not user:
        return jsonify(status_code.USER_NOT_EXISTS)
    # 验证密码
    if not user.check_pwd(password):
        return jsonify(status_code.USER_PASSWORD_ERROR)

    session['user_id'] = user.id
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/logout/', methods=['GET'])
@login_required
def logout():
    del session['user_id']
    return redirect(url_for('user.login'))


@user_blueprint.route('/mine/', methods=['GET'])
@login_required
def mine():
    return render_template('my.html')


@user_blueprint.route('/profile/', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


@user_blueprint.route('/get_name_img/', methods=['GET'])
@login_required
def get_name_img():
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        res = status_code.SUCCESS
        res['data'] = user.to_basic_dict()
        return jsonify(res)
    except BaseException as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/avatar/', methods=['PATCH'])
@login_required
def avatar():
    file = request.files.get('avatar')
    user_id = session.get('user_id')
    # 验证图片格式
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_IMAGE_FORMAT_ERROR)

    # 保存
    file_dir = os.path.join(common.UPLOAD_DIR, 'avatar/' + str(user_id))
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file_name = str(user_id) + '.' + file.filename.split('.')[-1]
    img_path = os.path.join(file_dir, file_name)
    file.save(img_path)

    try:
        user = User.query.filter_by(id=user_id).first()
        user.avatar = os.path.join('avatar/' + str(user_id), file_name)

        user.add_update()
        res = status_code.SUCCESS
        res['user_id'] = user.id
        res['img_url'] = user.avatar
        return jsonify(res)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/username/', methods=['PATCH'])
@login_required
def username():
    name = request.form.get('username')

    if not all([name]):
        return jsonify(status_code.USER_PARAMS_NOT_COMPLETE)

    try:
        user = User.query.filter_by(name=name).first()
        if user:
            return jsonify(status_code.USER_USERNAME_EXISTED)

        user = User.query.filter_by(id=session.get('user_id')).first()
        user.name = name

        user.add_update()
        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/authenticate/', methods=['GET'])
@login_required
def authenticate():
    return render_template('auth.html')


@user_blueprint.route('/authenticate/', methods=['PATCH'])
@login_required
def user_authenticate():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')

    # 验证数据不为空
    if not all([real_name, id_card]):
        return jsonify(status_code.USER_AUTH_DATA_NOT_NULL)
    # 简单验证身份证号
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_INVALID)

    try:
        user = User.query.filter_by(id=session['user_id']).first()
        user.id_name = real_name
        user.id_card = id_card
        user.add_update()

        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@user_blueprint.route('/auth_info/', methods=['GET'])
@login_required
def auth_info():
    try:
        user = User.query.filter_by(id=session['user_id']).first()
        res = status_code.SUCCESS
        res['data'] = user.to_auth_dict()
        return jsonify(res)
    except BaseException as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)