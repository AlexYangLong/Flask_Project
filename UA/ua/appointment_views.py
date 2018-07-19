from flask import Blueprint, render_template, request, jsonify, session
from flask_restful import Resource

from ua.models import Appointment, User
from utils import status_code
from utils.exts import api

appoint_blueprint = Blueprint('appoint', __name__)


@appoint_blueprint.route('/appoint_list/')
def appoint_list():
    return render_template('appointment/appoint_list.html')


@appoint_blueprint.route('/appoint_add/')
@appoint_blueprint.route('/appoint_edit/')
def appoint_addoredit():
    return render_template('appointment/appoint_addoredit.html')


class AppointApi(Resource):
    def get(self, apid=None):
        if not apid:
            sd = request.args.get('sd')
            ed = request.args.get('ed')
            sk = request.args.get('sk')
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))

            appoint_list = Appointment.query.filter(Appointment.is_delete == False).order_by('-create_time')
            if sd:
                appoint_list = appoint_list.filter(Appointment.start_time.__ge__(sd))
            if ed:
                appoint_list = appoint_list.filter(Appointment.end_time.__le__(ed))
            if sk:
                userids = [str(user.id) for user in User.query.filter(User.name.like('%'+sk+'%'), User.is_delete == False).all()]
                # users_id = ','.join(userids)
                appoint_list = appoint_list.filter(Appointment.user_id.in_(userids))
            counter = appoint_list.count()
            paginations = appoint_list.paginate(pn, ps)
            appoints = paginations.items
            # if sd and ed is None:
            #     # counter = Appointment.query.filter(Appointment.start_time.__ge__(sd),
            #     #                                    Appointment.is_delete == False).count()
            #     # paginations = Appointment.query.filter(Appointment.start_time.__ge__(sd),
            #     #                                        Appointment.is_delete == False).order_by('-create_time').paginate(pn, ps)
            #     # appoints = paginations.items
            # elif ed and sd is None:
            #     counter = Appointment.query.filter(Appointment.end_time.__le__(ed),
            #                                        Appointment.is_delete == False).count()
            #     paginations = Appointment.query.filter(Appointment.end_time.__le__(ed),
            #                                            Appointment.is_delete == False).order_by('-create_time').paginate(pn, ps)
            #     appoints = paginations.items
            # elif sd and ed:
            #     counter =Appointment.query.filter(Appointment.end_time.between(sd, ed),
            #                                        Appointment.is_delete == False).count()
            #     paginations = Appointment.query.filter(Appointment.end_time.between(sd, ed),
            #                                            Appointment.is_delete == False).order_by('-create_time').paginate(pn, ps)
            #     appoints = paginations.items
            # else:
            #     counter = Appointment.query.filter(Appointment.is_delete == False).count()
            #     paginations = Appointment.query.filter(Appointment.is_delete == False).order_by('-create_time').paginate(pn, ps)
            #     appoints = paginations.items
            res = status_code.SUCCESS
            res['data_list'] = [appoint.to_full_dict() for appoint in appoints]
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            return jsonify(res)

        appoint = Appointment.query.filter(Appointment.id == apid).first()
        if not appoint:
            return jsonify(status_code.APPOINT_NOT_EXISTS)
        if appoint.is_delete:
            return jsonify(status_code.ADMIN_ACCOUNT_DELETED)
        res = status_code.SUCCESS
        res['data'] = appoint.to_full_dict()
        return jsonify(res)

    def post(self):
        adid = session.get('adid')
        sd = request.form.get('st')
        ed = request.form.get('et')

        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        reason = request.form.get('reason')

        if not all([sd, ed, name, phone, adid]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})

        try:
            user = User.query.filter(User.phone == phone).first()
            if not user:
                # 创建用户
                u = User()
                u.name = name
                u.phone = phone
                u.email = email
                u.address = address
                u.reason = reason
                u.admin_id = adid
                u.add_update()
                uid = u.id
            else:
                if user.is_delete:
                    return jsonify(status_code.USER_DELETED)
                else:
                    uid = user.id
            appoint = Appointment()
            appoint.start_time = sd
            appoint.end_time = ed
            appoint.user_id = uid
            appoint.admin_id = adid
            appoint.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def put(self, apid=None):
        adid = session.get('adid')
        sd = request.form.get('st')
        ed = request.form.get('et')

        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        reason = request.form.get('reason')
        if not all([apid, sd, ed, name, phone, adid]):
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        appoint = Appointment.query.filter(Appointment.id == apid).first()
        if not appoint:
            return jsonify(status_code.APPOINT_NOT_EXISTS)
        if appoint.is_delete:
            return jsonify(status_code.APPOINT_DELETED)
        try:
            user = User.query.filter(User.phone == phone).first()
            if not user:
                # 创建用户
                u = User()
                u.name = name
                u.phone = phone
                u.email = email
                u.address = address
                u.reason = reason
                u.admin_id = adid
                u.add_update()
                uid = u.id
            else:
                if user.is_delete:
                    return jsonify(status_code.USER_DELETED)
                else:
                    uid = user.id
            appoint.start_time = sd
            appoint.end_time = ed
            appoint.user_id = uid
            appoint.admin_id = adid
            appoint.add_update()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    def delete(self, apid=None):
        if not apid:
            return jsonify({'code': status_code.ERROR_CODE, 'msg': '请求参数错误'})
        appoint = Appointment.query.filter(Appointment.id == apid).first()
        if not appoint:
            return jsonify(status_code.APPOINT_NOT_EXISTS)
        try:
            appoint.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(AppointApi, '/api/appoint/', '/api/appoint/<int:apid>/')
