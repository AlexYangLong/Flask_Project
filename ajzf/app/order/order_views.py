from flask import Blueprint, render_template, request, session, jsonify

from app.models import Order, db
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

