from flask import Blueprint, request, render_template, jsonify
from flask_restful import Resource

from bms.models import Grade
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

grade_blueprint = Blueprint('grade', __name__)


@grade_blueprint.route('/grade_list/')
@login_required
def grade_list():
    if request.method == 'GET':
        return render_template('grade/grade.html')


@grade_blueprint.route('/grade_add/')
@login_required
def grade_add():
    if request.method == 'GET':
        return render_template('grade/addgrade.html')


@grade_blueprint.route('/grade_edit/')
@login_required
def grade_edit():
    if request.method == 'GET':
        return render_template('grade/addgrade.html')


class GradeApi(Resource):
    def get(self, gid=None):
        if gid is None:
            pn = int(request.args.get('pn', 1))
            ps = 10
            paginations = Grade.query.order_by('-create_time').paginate(pn, ps)
            grades = paginations.items

            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['data_list'] = [grade.to_dict() for grade in grades]
            return jsonify(res)

        if gid == 0:
            grades = Grade.query.all()
            res = status_code.SUCCESS
            res['data_list'] = [grade.to_dict() for grade in grades]
            return jsonify(res)

        grade = Grade.query.get(gid)
        if grade:
            res = status_code.SUCCESS
            res['data'] = grade.to_dict()
            return jsonify(res)

        return jsonify(status_code.GRADE_NOT_EXISTS)

    def post(self, gid=None):
        name = request.form.get('name')

        if not name:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not gid:
            grade = Grade.query.filter_by(name=name).first()
            if grade:
                return jsonify(status_code.GRADE_EXISTED)

            grade = Grade()
            grade.name = name
            grade.add_update()
        else:
            grade = Grade.query.get(gid)
            grade.name = name
            grade.add_update()

        res = status_code.SUCCESS
        res['data'] = grade.to_dict()
        return jsonify(res)

    def delete(self, gid):
        if gid:
            role = Grade.query.get(gid)
            if not role:
                return jsonify(status_code.GRADE_NOT_EXISTS)

            role.delete()
            return jsonify(status_code.SUCCESS)

        return jsonify(status_code.PARAMS_NOT_COMPLETE)


api.add_resource(GradeApi, '/api/grade/', '/api/grade/<int:gid>/')
