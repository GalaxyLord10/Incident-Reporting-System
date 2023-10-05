from flask import Blueprint, flash, url_for, redirect, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from forms.admin_user_edit_form import AdminUserEditForm
from forms.change_password_form import ChangePasswordForm
from forms.incident_update_form import IncidentUpdateForm
from models.db_models import Incident, User
from utilities.utilities import admin_required, db_commit, flash_and_log

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
    return render_template('dashboard/admin_dashboard.html',
                           total_users=len(all_users),
                           total_incidents=len(all_incidents))


@dash.route('/admin_manage_users', methods=['GET'])
@admin_required
@login_required
def admin_manage_users():
    all_incidents = Incident.query.all()
    all_users = User.query.all()
    if len(all_incidents) == 0:
        flash('No users to display', 'info')
    return render_template('dashboard/admin_manage_users.html',  users=all_users, incidents=all_incidents)


@dash.route('/admin_incident_overview', methods=['GET', 'POST'])
@admin_required
@login_required
def admin_incident_overview():
    selected_user_id = request.args.get('user_id')
    all_users = User.query.all()
    if selected_user_id:
        all_incidents = Incident.query.filter_by(user_id=selected_user_id).all() # get all incidents
    else:
        all_incidents = Incident.query.all()
    return render_template('incidents/admin_incident_overview.html', incidents=all_incidents, users=all_users)


@dash.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        user.account_type = form.account_type.data
        db_commit()
        flash_and_log(f"User {user.email} updated successfully!", 'success', f"User {user.email} was updated.")
        return redirect(url_for('dash.admin_dashboard'))
    return render_template('dashboard/admin_user_edit_form.html', form=form, user=user)


@dash.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db_commit()
    flash_and_log(f"User {user.email} deleted successfully!", 'success', f"User {user.email} deleted!")
    return redirect(url_for('dash.admin_dashboard'))


@dash.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.new_password.data == form.confirm_password.data:
            current_user.password = generate_password_hash(form.new_password.data)
            db_commit()
            flash_and_log('Password changed successfully', 'success', f"{current_user.email} password was changed.")
            return redirect(url_for('dash.user_profile'))
        else:
            flash('Passwords do not match', 'danger')
    return render_template('user_profile/profile.html', form=form, email=current_user.email)


@dash.route('/admin_edit_incident/<int:incident_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def admin_edit_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    form = IncidentUpdateForm(obj=incident)

    if form.validate_on_submit():
        incident.system = form.system.data
        incident.product = form.product.data
        incident.issue = form.issue.data
        incident.time_of_occurrence = form.time_of_occurrence.data
        incident.status = form.status.data
        db_commit()
        flash('Incident updated successfully', 'success')
        return redirect(url_for('dash.admin_incident_overview'))

    return render_template('incidents/admin_edit_incident.html', form=form)


@dash.route('/delete_incident/<int:incident_id>', methods=['POST'])
@admin_required
@login_required
def admin_delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db_commit()
    flash('Incident deleted successfully', 'success')
    return redirect(url_for('admin_dashboard.incident_overview'))


@dash.route('/admin_view_incident/<int:incident_id>', methods=['POST'])
@admin_required
@login_required
def admin_view_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db_commit()
    flash('Incident deleted successfully', 'success')
    return redirect(url_for('admin_dashboard.incident_overview'))


@dash.route('/logs', methods=['GET'])
@login_required
@admin_required
def logs():
    with open('user_activity.log', 'r') as f:
        log_data = f.readlines()
    return render_template('logs.html', log_data=log_data)
