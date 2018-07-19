from flask import Blueprint, render_template, session

from ua.models import LoginRecord
from utils.decorators import login_required

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index/', methods=['GET'])
@index_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@index_blueprint.route('/welcome/', methods=['GET'])
@login_required
def welcome():
    adid = session.get('adid')
    login_count = LoginRecord.query.filter(LoginRecord.admin_id == adid).count()
    if login_count > 1:
        last_login_record = LoginRecord.query.filter(LoginRecord.admin_id == adid).order_by('-create_time').limit(2).all()[-1]
    else:
        last_login_record = None
    return render_template('welcome.html', login_count=login_count, last_login_record=last_login_record)
