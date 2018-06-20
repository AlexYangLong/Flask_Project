from flask import Blueprint, render_template, jsonify, request, session

from app.models import Area, Facility, House, db
from utils import status_code
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
@login_required
def area_facility():
    areas = Area.query.all()
    facilities = Facility.query.all()

    res = status_code.SUCCESS
    res['area_list'] = [area.to_dict() for area in areas]
    res['facility_list'] = [facility.to_dict() for facility in facilities]
    return jsonify(res)


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
    fid_list = check_val.split(',')[:-1]
    try:
        for f_id in fid_list:
            f = Facility.query.get(f_id)
            house.facilities.append(f)

        house.add_update()
        res = status_code.SUCCESS
        res['data'] = house.to_dict()
        return jsonify(res)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
