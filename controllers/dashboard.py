from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_required, current_user
from forms.incident_form import IncidentForm
from models.db_models import Incident, db

dash = Blueprint('dash', __name__)


@dash.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')


@dash.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.account_type != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return 'Welcome to the Admin Dashboard!'
