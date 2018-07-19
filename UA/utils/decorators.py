import functools

from flask import session, jsonify, redirect, url_for

from utils import status_code


def login_required(func):
    @functools.wraps(func)
    def check_login(*args, **kwargs):
        if not session.get('adid'):
            # return jsonify(status_code.ADMIN_NOT_LOGINED)
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return check_login
