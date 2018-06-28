from flask import Blueprint, render_template, jsonify, request
from flask_restful import Resource
from sqlalchemy import or_

from cms.models import Authority, Role, Admin
from utils import status_code
from utils.exts import api

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/auth_list/', methods=['GET'])
def auth_list():
    return render_template('admin/auth_list.html')


@admin_blueprint.route('/auth_add/', methods=['GET'])
def auth_add():
    return render_template('admin/auth_addoredit.html')


@admin_blueprint.route('/auth_edit/', methods=['GET'])
def auth_edit():
    return render_template('admin/auth_addoredit.html')


@admin_blueprint.route('/role_list/', methods=['GET'])
def role_list():
    return render_template('admin/role_list.html')


@admin_blueprint.route('/role_add/', methods=['GET'])
def role_add():
    return render_template('admin/role_addoredit.html')


@admin_blueprint.route('/role_edit/', methods=['GET'])
def role_edit():
    return render_template('admin/role_addoredit.html')


@admin_blueprint.route('/admin_list/', methods=['GET'])
def admin_list():
    return render_template('admin/admin_list.html')


@admin_blueprint.route('/admin_add/', methods=['GET'])
def admin_add():
    return render_template('admin/admin_addoredit.html')


@admin_blueprint.route('/admin_edit/', methods=['GET'])
def admin_edit():
    return render_template('admin/admin_addoredit.html')


class AuthApi(Resource):
    def get(self, aid=None):
        if aid == 0:
            auths = Authority.query.filter(Authority.parent_id == None).order_by('-create_time')
            res = status_code.SUCCESS
            res['data_list'] = [auth.to_parent_info_dict() for auth in auths]
            return jsonify(res)

        if not aid:
            kw = request.args.get('kw')
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))
            if not kw:
                counter = Authority.query.count()
                paginations = Authority.query.order_by('-create_time').paginate(pn, ps)
                auths = paginations.items
                res = status_code.SUCCESS
                res['page_now'] = pn
                res['page_size'] = ps
                res['page_total'] = paginations.pages
                res['rows_count'] = counter
                res['data_list'] = [auth.to_dict() for auth in auths]
                return jsonify(res)
            counter = Authority.query.filter(Authority.name.like('%' + kw + '%')).count()
            paginations = Authority.query.filter(Authority.name.like('%' + kw + '%')).order_by('-create_time').paginate(pn, ps)
            auths = paginations.items
            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            res['data_list'] = [auth.to_dict() for auth in auths]
            return jsonify(res)

        auth = Authority.query.filter(Authority.id == aid).first()
        if not auth:
            return jsonify(status_code.AUTHORITY_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = auth.to_dict()
        return jsonify(res)

    def post(self):
        aid = request.form.get('aid')
        name = request.form.get('name')
        url = request.form.get('url')
        pid = request.form.get('pid')

        if not name:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not aid:
            try:
                auth = Authority.query.filter(Authority.name == name).first()
                if auth:
                    return jsonify(status_code.AUTHORITY_ALREADY_EXISTS)

                auth = Authority()
                auth.name = name
                auth.url = url
                auth.parent_id = pid
                auth.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)
        else:
            try:
                auth = Authority.query.filter(Authority.id == aid).first()
                if not auth:
                    return jsonify(status_code.AUTHORITY_NOT_EXISTS)
                auth.name = name
                auth.url = url
                auth.parent_id = pid
                auth.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)

    def delete(self, aid):
        if not aid:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)
        try:
            auth = Authority.query.filter(Authority.id == aid).first()
            if not auth:
                return jsonify(status_code.AUTHORITY_NOT_EXISTS)
            auth.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(AuthApi, '/api/auth/', '/api/auth/<int:aid>/')


class RoleApi(Resource):
    def get(self, rid=None):
        if rid == 0:
            roles = Role.query.order_by('-create_time')
            res = status_code.SUCCESS
            res['data_list'] = [role.to_base_dict() for role in roles]
            return jsonify(res)

        if not rid:
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))
            counter = Role.query.count()
            paginations = Role.query.order_by('-create_time').paginate(pn, ps)
            roles = paginations.items
            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            res['data_list'] = [role.to_admins_dict() for role in roles]
            return jsonify(res)

        role = Role.query.filter(Role.id == rid).first()
        if not role:
            return jsonify(status_code.ROLE_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = role.to_auths_dict()
        return jsonify(res)

    def post(self):
        rid = request.form.get('rid')
        name = request.form.get('name')
        description = request.form.get('description')
        aids = request.form.get('aids')

        if not all([name, aids]):
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not rid:
            try:
                role = Role.query.filter(Role.name == name).first()
                if role:
                    return jsonify(status_code.ROLE_ALREADY_EXISTS)

                aid_list = Authority.query.filter(Authority.id.in_(aids))
                role = Role()
                role.name = name
                role.description = description
                role.authorities = aid_list
                role.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)
        else:
            try:
                role = Role.query.filter(Role.id == rid).first()
                if not role:
                    return jsonify(status_code.ROLE_NOT_EXISTS)

                aid_list = Authority.query.filter(Authority.id.in_(aids))
                role.name = name
                role.description = description
                role.authorities = aid_list
                role.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)

    def delete(self, rid):
        if not rid:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)
        try:
            role = Role.query.filter(Role.id == rid).first()
            if not role:
                return jsonify(status_code.ROLE_NOT_EXISTS)
            role.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(RoleApi, '/api/role/', '/api/role/<int:rid>/')


class AdminApi(Resource):
    def get(self, adid=None):
        # if adid == 0:
        #     auths = Authority.query.filter(Authority.parent_id == None).order_by('-create_time')
        #     res = status_code.SUCCESS
        #     res['data_list'] = [auth.to_parent_info_dict() for auth in auths]
        #     return jsonify(res)

        if not adid:
            # sd = request.args.get('sd')
            # ed = request.args.get('ed')
            kw = request.args.get('kw')
            pn = int(request.args.get('pn', 1))
            ps = int(request.args.get('ps', 10))
            if not kw:
                counter = Admin.query.count()
                paginations = Admin.query.order_by('-create_time').paginate(pn, ps)
                admins = paginations.items
                res = status_code.SUCCESS
                res['page_now'] = pn
                res['page_size'] = ps
                res['page_total'] = paginations.pages
                res['rows_count'] = counter
                res['data_list'] = [admin.to_dict() for admin in admins]
                return jsonify(res)
            counter = Admin.query.filter(or_(Admin.username.like('%' + kw + '%'), Admin.name.like('%' + kw + '%'))).count()
            paginations = Admin.query.filter(or_(Admin.username.like('%' + kw + '%'), Admin.name.like('%' + kw + '%'))).order_by('-create_time').paginate(pn, ps)
            admins = paginations.items
            res = status_code.SUCCESS
            res['page_now'] = pn
            res['page_size'] = ps
            res['page_total'] = paginations.pages
            res['rows_count'] = counter
            res['data_list'] = [admin.to_dict() for admin in admins]
            return jsonify(res)

        admin = Admin.query.filter(Admin.id == adid).first()
        if not admin:
            return jsonify(status_code.ADMIN_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = admin.to_dict()
        return jsonify(res)

    def post(self):
        adid = request.form.get('adid')
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        rid = request.form.get('rid')

        if not all([username, password, name, rid]):
            return jsonify(status_code.PARAMS_NOT_COMPLETE)

        if not adid:
            try:
                admin = Admin.query.filter(Admin.username == username).first()
                if admin:
                    return jsonify(status_code.ADMIN_ALREADY_EXISTS)

                admin = Admin(username=username, password=password, name=name)
                admin.role_id = rid
                admin.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)
        else:
            try:
                admin = Admin.query.filter(Admin.id == adid).first()
                if not admin:
                    return jsonify(status_code.ADMIN_NOT_EXISTS)

                admin.username = username
                admin.password = password
                admin.name = name
                admin.role_id = rid
                admin.add_update()
                return jsonify(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return jsonify(status_code.DATABASE_ERROR)

    def delete(self, adid):
        if not adid:
            return jsonify(status_code.PARAMS_NOT_COMPLETE)
        try:
            admin = Admin.query.filter(Admin.id == adid).first()
            if not admin:
                return jsonify(status_code.ADMIN_NOT_EXISTS)
            admin.delete()
            return jsonify(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)


api.add_resource(AdminApi, '/api/admin/', '/api/admin/<int:adid>/')
