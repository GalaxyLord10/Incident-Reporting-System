from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_required, current_user

from extensions import db
from models.db_models import Incident, User
from utilities.utilities import admin_required

dash = Blueprint('dash', __name__)


@dash.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('dashboard/admin_dashboard.html')
    else:
        return render_template('dashboard/dashboard.html')


@dash.route('/admin_dashboard', methods=['GET'])
@admin_required
@login_required
def admin_dashboard():
    all_incidents = Incident.query.all()
    all_users = User.query.all()

    if len(all_incidents) == 0:
        flash('No incidents to display', 'info')

    return render_template('dashboard/admin_dashboard.html')


@dash.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = User(obj=user)

    if form.validate_on_submit():
        user.account_type = form.account_type.data
        db.session.commit()

    flash(f"User {user.email} updated successfully!", 'success')

    return redirect(url_for('admin_dashboard.dashboard'))


@dash.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.email} deleted successfully!", 'success')

    return redirect(url_for('admin_dashboard.dashboard'))


@dash.route('/resolve_incident/<int:incident_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def resolve_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    incident.status = 'Resolved'
    db.session.commit()

    flash(f"Incident {incident.id} marked as Resolved.", 'success')

    return redirect(url_for('admin_dashboard.dashboard'))


@dash.route('/mark_pending/<int:incident_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def mark_pending(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    incident.status = 'Pending'
    db.session.commit()

    flash(f"Incident {incident.id} marked as Pending.", 'success')

    return redirect(url_for('admin_dashboard.dashboard'))

