from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    """装饰器，用于验证是否登录"""
    @wraps(func)
    def is_login(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return is_login
