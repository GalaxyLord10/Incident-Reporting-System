from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

home = Blueprint('home', __name__)


@home.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dash.dashboard'))
        else:
            return redirect(url_for('dash.dashboard'))
    return render_template('home/home.html')