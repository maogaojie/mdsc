from flask import redirect,url_for,session
from functools import wraps


def outer(func):
    @wraps(func)
    def inner():
        if not session.get('admin_id'):
            return redirect(url_for('admin.login'))
        return func()
    return inner