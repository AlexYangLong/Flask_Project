import re

import os
from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import and_

from app.models import Area, Facility, House, db, HouseImage, Order
from utils import status_code, common
from utils.decorators import login_required

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/my_house/', methods=['GET'])
@login_required
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('/new_house/', methods=['GET'])
@login_required
def new_house():
    return render_template('newhouse.html')


@house_blueprint.route('/area_facility/', methods=['GET'])
# @login_required
def area_facility():
    areas = Area.query.all()
    facilities = Facility.query.all()

    res = status_code.SUCCESS
    res['area_list'] = [area.to_dict() for area in areas]
    res['facility_list'] = [facility.to_dict() for facility in facilities]
    return jsonify(res)


@house_blueprint.route('/house_list/', methods=['GET'])
@login_required
def house_list():
    try:
        houses = House.query.filter_by(user_id=session['user_id'])
        res = status_code.SUCCESS
        res['data_list'] = [house.to_dict() for house in houses]
        return jsonify(res)
    except BaseException as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


@house_blueprint.route('/publish_house/', methods=['POST'])
@login_required
def publish_house():
    title = request.form.get('title')
    price = request.form.get('price')
    area_id = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    check_val = request.form.get('check_val')

    if not all([title, price, area_id, address, room_count, acreage, unit, capacity,
                beds, deposit, min_days, max_days, check_val]):
        return jsonify(status_code.HOUSE_PARAMS_NOT_COMPLETE)

    house = House()
    house.user_id = session.get('user_id')
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    fid_list = check_val[:-1]
    try:
        f_list = Facility.query.filter(Facility.id.in_(fid_list)).all()
        house.facilities = f_list

        house.add_update()
        res = status_code.SUCCESS
        res['data'] = house.to_dict()
        return jsonify(res)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@house_blueprint.route('/upload_image/', methods=['POST'])
@login_required
def upload_image():
    hid = request.form.get('house_id')
    img_list = request.files.getlist('house_image')

    # 验证图片格式
    # if not re.match(r'image/.*', file.mimetype):
    #     return jsonify(status_code.USER_IMAGE_FORMAT_ERROR)

    # 保存
    file_dir = os.path.join(common.UPLOAD_DIR, 'house/' + hid)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    try:
        for img in img_list:
            img_path = os.path.join(file_dir, img.filename)
            img.save(img_path)

            himg = HouseImage()
            himg.house_id = hid
            himg.url = os.path.join('house/' + hid, img.filename)
            db.session.add(himg)
        house = House.query.filter_by(id=hid).first()
        house.index_image_url = os.path.join('house/' + hid, img_list[0].filename)
        db.session.add(house)
        db.session.commit()
        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@house_blueprint.route('/house_detail/', methods=['GET'])
def house_detail():
    return render_template('detail.html')


@house_blueprint.route('/house_info/<int:hid>/', methods=['GET'])
def house_info(hid):
    if not hid:
        return jsonify(status_code.HOUSE_PARAMS_NOT_COMPLETE)
    try:
        house = House.query.filter_by(id=hid).first()
        comments = Order.query.filter_by(house_id=hid, status='COMPLETE').all()
        res = status_code.SUCCESS
        res['data'] = house.to_full_dict()
        res['comments'] = [comment.to_dict() for comment in comments]
        return jsonify(res)
    except BaseException as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


@house_blueprint.route('/index/')
def index():
    return render_template('index.html')

@house_blueprint.route('/lorder/')
def lorder():
    return render_template('lorders.html')