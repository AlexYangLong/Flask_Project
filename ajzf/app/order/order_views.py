from flask import Blueprint, render_template, request, session, jsonify

from app.models import Order, db, House
from utils import status_code
from utils.decorators import login_required

book_blueprint = Blueprint('book', __name__)


@book_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@book_blueprint.route('/check_in/', methods=['POST'])
@login_required
def check_in():
    uid = session.get('user_id')
    hid = request.form.get('hid')
    begin = request.form.get('begin')
    end = request.form.get('end')
    days = request.form.get('days')
    price = request.form.get('price')
    amount = request.form.get('amount')

    if not all([hid, begin, end, days, price, amount]):
        return jsonify(status_code.ORDER_PARAMS_NOT_COMPLETE)

    if begin > end:
        return jsonify(status_code.ORDER_TIME_PARAMS_ERROR)

    try:
        order = Order()
        order.user_id = uid
        order.house_id = hid
        order.begin_date = begin
        order.end_date = end
        order.days = days
        order.house_price = price
        order.amount = amount

        order.add_update()
        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)


@book_blueprint.route('/my_orders/', methods=['GET'])
@login_required
def my_orders():
    return render_template('orders.html')


@book_blueprint.route('/my_orders_list/', methods=['GET'])
@login_required
def my_orders_list():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by('-create_time')
    res = status_code.SUCCESS
    res['data_list'] = [order.to_dict() for order in orders]
    return jsonify(res)


@book_blueprint.route('/custom_orders/', methods=['GET'])
@login_required
def custom_orders():
    return render_template('lorders.html')


@book_blueprint.route('/custom_orders_list/', methods=['GET'])
@login_required
def custom_orders_list():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    houses_ids = [house.id for house in houses]
    order_list = Order.query.filter(Order.house_id.in_(houses_ids)).order_by('-create_time')
    # order_list = []
    # for house in houses:
    #     orders = Order.query.filter_by(house_id=house.id).order_by('-create_time').all()
    #     order_list.extend(orders)
    res = status_code.SUCCESS
    res['data_list'] = [order.to_dict() for order in order_list]
    return jsonify(res)


@book_blueprint.route('/change_order_status/', methods=['PATCH'])
@login_required
def change_order_status():
    oid = request.form.get('oid')
    status = request.form.get('status')
    comment = request.form.get('comment')

    if status == '已完成' or status == '已拒单':
        if not all([oid, status, comment]):
            return jsonify(status_code.ORDER_PARAMS_NOT_COMPLETE)
    else:
        if not all([oid, status]):
            return jsonify(status_code.ORDER_PARAMS_NOT_COMPLETE)

    if status == '待支付':
        status = 'WAIT_PAYMENT'
    elif status == '已支付':
        status = 'PAID'
    elif status == '待评价':
        status = 'WAIT_COMMENT'
    elif status == '已完成':
        status = 'COMPLETE'
    elif status == '已取消':
        status = 'CANCELED'
    elif status == '已拒单':
        status = 'REJECTED'
    else:
        return jsonify(status_code.ORDER_STATUS_DATA_ERROR)

    try:
        order = Order.query.filter(Order.id == oid).first()
        order.status = status
        order.comment = comment
        order.add_update()
        return jsonify(status_code.SUCCESS)
    except BaseException as e:
        print(e)
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
