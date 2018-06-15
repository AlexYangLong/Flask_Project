from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if not session.get('admin_id'):
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return check_login
