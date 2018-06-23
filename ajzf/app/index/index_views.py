from flask import Blueprint, render_template, request, session, jsonify
from sqlalchemy import or_

from app.models import House, Order
from utils import status_code

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index/', methods=['GET'])
@index_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@index_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@index_blueprint.route('/get_houses/', methods=['GET'])
def get_houses():
    aid = request.args.get('aid')
    begin = request.args.get('sd')
    end = request.args.get('ed')
    sk = request.args.get('sk')
    pn = request.args.get('pn')

    # 区域过滤
    houses = House.query.filter(House.area_id == aid)
    # 过滤房主
    if 'user_id' in session:
        houses = houses.filter(House.user_id.notin_(session['user_id']))
    # 判断搜索的开始时间、结束时间
    orders = Order.query.filter(or_(Order.status == 'WAIT_PAYMENT', Order.status == 'PAID'))

    orders1 = orders.filter(Order.begin_date <= begin, Order.end_date >= begin).all()
    orders2 = orders.filter(Order.begin_date <= end, Order.end_date >= end).all()
    orders3 = orders.filter(Order.begin_date <= begin, Order.end_date <= end).all()

    orders_ids1 = [order.house_id for order in orders1]
    orders_ids2 = [order.house_id for order in orders2]
    orders_ids3 = [order.house_id for order in orders3]

    houses_ids = list(set(orders_ids1 + orders_ids2 + orders_ids3))

    if sk == 'new':
        houses = houses.filter(House.id.notin_(houses_ids)).order_by('-create_time')
    elif sk == 'booking':
        houses = houses.filter(House.id.notin_(houses_ids)).order_by('-order_count')
    elif sk == 'price-inc':
        houses = houses.filter(House.id.notin_(houses_ids)).order_by('price')
    elif sk == 'price-des':
        houses = houses.filter(House.id.notin_(houses_ids)).order_by('-price')

    res = status_code.SUCCESS
    res['data_list'] = [house.to_full_dict() for house in houses]
    return jsonify(res)
