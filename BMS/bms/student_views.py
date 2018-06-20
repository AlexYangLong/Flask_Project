from flask import Blueprint, request, render_template, jsonify
from flask_restful import Resource

from bms.models import Student
from utils import status_code
from utils.decorators import login_required
from utils.exts import api

student_blueprint = Blueprint('student', __name__)


@student_blueprint.route('/student_list/')
@login_required
def student_list():
    if request.method == 'GET':
        return render_template('student/student.html')


@student_blueprint.route('/student_add/')
@login_required
def student_add():
    if request.method == 'GET':
        return render_template('student/addstu.html')


@student_blueprint.route('/student_edit/')
@login_required
def student_edit():
    if request.method == 'GET':
        return render_template('student/addstu.html')


class StudentApi(Resource):
    def get(self, sid=None):
        if not sid:
            pn = int(request.args.get('pn', 1))
            ps = 10
            paginations = Student.query.order_by('-create_time').paginate(pn, ps)
            stus = paginations.items

            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['data_list'] = [stu.to_dict() for stu in stus]
            return jsonify(res)

        stu = Student.query.get(sid)
        if stu:
            res = status_code.SUCCESS
            res['data'] = stu.to_dict()
            return jsonify(res)

        return jsonify(status_code.STUDENT_NOT_EXISTS)

    def post(self, sid=None):
        name = request.form.get('name')
        gender = True if request.form.get('gender') == '1' else False
        gid = request.form.get('class')

        if not all([name, gender, gid]):
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        # stu = Student.query.filter_by(name=name).first()
        # if stu:
        #     return jsonify(status_code.STUDENT_EXISTED)

        if not sid:
            stu = Student()
            stu.name = name
            stu.gender = gender
            stu.grade_id = gid
            stu.add_update()
        else:
            stu = Student.query.get(sid)
            stu.name = name
            stu.gender = gender
            stu.grade_id = gid
            stu.add_update()

        res = status_code.SUCCESS
        res['data'] = stu.to_dict()
        return jsonify(res)

    def delete(self, sid):
        if sid:
            stu = Student.query.get(sid)
            if not stu:
                return jsonify(status_code.STUDENT_NOT_EXISTS)

            stu.delete()
            return jsonify(status_code.SUCCESS)

        return jsonify(status_code.PARAMS_NOT_COMPLETE)


api.add_resource(StudentApi, '/api/student/', '/api/student/<int:sid>/')
