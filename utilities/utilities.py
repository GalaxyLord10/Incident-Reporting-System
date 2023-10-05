from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for
import logging

from extensions import db
from models.db_models import User


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


def query_user_by_email(email):
    return User.query.filter_by(email=email).first()


def flash_and_log(message, level, log_message):
    flash(message, level)
    user_activity_logger = configure_logger()
    user_activity_logger.info(log_message)


def db_commit(add_value=None):
    try:
        if add_value is not None:
            db.session.add(add_value)
            db.session.commit()
        else:
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        user_activity_logger = configure_logger()
        user_activity_logger.error(f"Database commit failed: {str(e)}")
        flash("An error occurred. Please try again.", "danger")


