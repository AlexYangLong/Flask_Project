from flask import Blueprint, render_template, session, jsonify

from cms.models import Admin
from utils import status_code

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@index_blueprint.route('/welcome/', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@index_blueprint.route('/admin_auths/', methods=['GET'])
def admin_auths():
    aid = session.get('aid')
    admin = Admin.query.filter(Admin.id == aid).first()
    admin_auth_list = admin.role.authorities
    parent_list = admin_auth_list.filter_by(parent_id=None).all()
    data_list = []
    for parent in parent_list:
        admin_auth_list.remove(parent)
        p_dict = parent.to_dict()
        p_dict['sub_list'] = []
        for sub in admin_auth_list:
            if parent.id == sub.parent_id:
                s_dict = sub.to_dict()
                p_dict['sub_list'].append(s_dict)
        data_list.append(p_dict)
    res = status_code.SUCCESS
    res['data_list'] = data_list
    return jsonify(res)
