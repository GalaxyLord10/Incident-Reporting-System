from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.account_type != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home.index'))  # Redirect to home or login page
        return f(*args, **kwargs)
    return decorated_function