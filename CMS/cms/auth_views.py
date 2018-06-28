from flask import Blueprint, render_template, jsonify, request, session
from flask_restful import Resource

from cms.models import Admin
from utils import status_code
from utils.exts import api

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


class AuthenticateApi(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        admin = Admin.query.filter(Admin.username == username, Admin.password == password).first()
        if not admin:
            return jsonify(status_code.LOGIN_AUTHENTICATE_FAILED)
        session['aid'] = admin.id
        res = status_code.SUCCESS
        res['data'] = admin.to_dict()
        return jsonify(res)


api.add_resource(AuthenticateApi, '/api/authenticate/')
