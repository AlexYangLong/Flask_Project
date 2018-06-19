from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def is_login(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return is_login
