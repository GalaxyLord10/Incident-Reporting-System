from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for
import logging


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.account_type != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home.index'))  # Redirect to home or login page
        return f(*args, **kwargs)
    return decorated_function


def configure_logger():
    user_activity_logger = logging.getLogger('user_activity')
    handler = logging.FileHandler('user_activity.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    user_activity_logger.addHandler(handler)
    user_activity_logger.setLevel(logging.INFO)
    return user_activity_logger
