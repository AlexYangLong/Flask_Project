from flask import Blueprint, request, render_template, jsonify
from flask_restful import Resource

from bms.models import Authority
from utils import status_code
from utils.exts import api

authority_blueprint = Blueprint('authority', __name__)


@authority_blueprint.route('/auth_list/')
def auth_list():
    if request.method == 'GET':
        return render_template('auth/permissions.html')


class AuthorityApi(Resource):
    def get(self, aid=None):
        if not aid:
            pn = int(request.args.get('pn', 1))
            ps = 10
            paginations = Authority.query.order_by('-create_time').paginate(pn, ps)
            auths = paginations.items

            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps,
            res['page_total'] = paginations.pages,
            res['data_list'] = [auth.to_dict() for auth in auths]
            return jsonify(res)

        auth = Authority.query.get(aid)
        if auth:
            res = status_code.SUCCESS
            res['data'] = auth.to_dict()
            return jsonify(res)

        return jsonify(status_code.AUTHORITY_NOT_EXISTS)

    def post(self):
        aid = request.form.get('aid')
        name = request.form.get('name')

        if not name:
            return jsonify(status_code.AUTHORITY_PARAMS_ERROR)

        if not aid:
            auth = Authority.query.filter_by(name=name)
            if auth:
                return jsonify(status_code.AUTHORITY_EXISTED)

            auth = Authority()
            auth.name = name
            auth.add_update()
        else:
            auth = Authority.query.get(aid)
            auth.name = name
            auth.add_update()

        res = status_code.SUCCESS
        res['data'] = auth.to_dict()
        return jsonify(res)

    def delete(self, aid):
        if aid:
            auth = Authority.query.get(aid)
            if not auth:
                return jsonify(status_code.AUTHORITY_NOT_EXISTS)

            auth.delete()
            return jsonify(status_code.SUCCESS)

        return jsonify(status_code.AUTHORITY_PARAMS_ERROR)


api.add_resource(AuthorityApi, '/authority_api/', '/authority_api/<int:aid>/')