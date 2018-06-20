from flask import Blueprint, request, render_template, jsonify
from flask_restful import Resource

from bms.models import Role
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

role_blueprint = Blueprint('role', __name__)


@role_blueprint.route('/role_list/')
@login_required
def role_list():
    if request.method == 'GET':
        return render_template('role/roles.html')


@role_blueprint.route('/role_edit/')
@login_required
def role_edit():
    if request.method == 'GET':
        return render_template('role/addroles.html')


@role_blueprint.route('/role_add/')
@login_required
def role_add():
    if request.method == 'GET':
        return render_template('role/addroles.html')


class RoleApi(Resource):
    def get(self, rid=None):
        if rid is None:
            pn = int(request.args.get('pn', 1))
            ps = 10
            paginations = Role.query.order_by('-create_time').paginate(pn, ps)
            roles = paginations.items

            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['data_list'] = [role.to_dict() for role in roles]
            return jsonify(res)

        if rid == 0:
            roles = Role.query.all()
            res = status_code.SUCCESS
            res['data_list'] = [role.to_dict() for role in roles]
            return jsonify(res)

        role = Role.query.get(rid)
        if role:
            res = status_code.SUCCESS
            res['data'] = role.to_dict()
            return jsonify(res)

        return jsonify(status_code.ROLE_NOT_EXISTS)

    def post(self, rid=None):
        name = request.form.get('name')

        if not name:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not rid:
            role = Role.query.filter_by(name=name).first()
            if role:
                return jsonify(status_code.ROLE_EXISTED)

            role = Role()
            role.name = name
            role.add_update()
        else:
            role = Role.query.get(rid)
            role.name = name
            role.add_update()

        res = status_code.SUCCESS
        res['data'] = role.to_dict()
        return jsonify(res)

    def delete(self, rid):
        if rid:
            role = Role.query.get(rid)
            if not role:
                return jsonify(status_code.ROLE_NOT_EXISTS)

            role.delete()
            return jsonify(status_code.SUCCESS)

        return jsonify(status_code.PARAMS_NOT_COMPLETE)


api.add_resource(RoleApi, '/api/role/', '/api/role/<int:rid>/')
