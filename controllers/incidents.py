from flask import Blueprint, flash, url_for, redirect, render_template, abort, request
from flask_login import login_required, current_user
from forms.incident_form import IncidentForm
from forms.incident_update_form import IncidentUpdateForm
from models.db_models import Incident, db, IncidentUpdate

incident = Blueprint('incident', __name__)


@incident.route('/incidents_overview')
@login_required
def incidents_overview():
    incidents = Incident.query.all()
    return render_template('incidents/overview.html', title="Incident Overview", incidents=incidents)


@incident.route('/view_incident/<int:incident_id>')
@login_required
def view_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return render_template('incidents/view_incident.html', incident=incident)


@incident.route('/create_incident', methods=['GET', 'POST'])
@login_required
def create_incident():
    form = IncidentForm()
    if form.validate_on_submit():
        new_incident = Incident(user_id=current_user.id, system=form.system.data, product=form.product.data, issue=form.issue.data,
                                time_of_occurrence=form.time_of_occurrence.data, status=form.status.data)
        db.session.add(new_incident)
        # Set the notification_status to 'Unread'
        new_incident.notification_status = 'Unread'

        db.session.commit()
        flash('Incident created successfully!', 'success')
        return redirect(url_for('incident.incidents_overview'))
    return render_template('incidents/create_incident.html', title='Create Incident', form=form)


@incident.route('/update_incident/<int:incident_id>', methods=['GET', 'POST'])
@login_required
def update_incident(incident_id):
    edit_incident = Incident.query.get_or_404(incident_id)
    if edit_incident.user != current_user:
        abort(403)
    form = IncidentUpdateForm()
    if form.validate_on_submit():
        edit_incident.system = form.system.data
        edit_incident.product = form.product.data
        edit_incident.issue = form.issue.data
        edit_incident.time_of_occurrence = form.time_of_occurrence.data
        edit_incident.status = form.status.data
        db.session.commit()
        flash('Incident updated!', 'success')
        return redirect(url_for('incident.incidents_overview'))
    elif request.method == 'GET':
        form.system.data = edit_incident.system
        form.product.data = edit_incident.product
        form.issue.data = edit_incident.issue
        form.time_of_occurrence.data = edit_incident.time_of_occurrence
        form.status.data = edit_incident.status
    return render_template('incidents/update_incident.html', form=form)


@incident.route('/delete_incident/<int:incident_id>', methods=['POST'])
@login_required
def delete_incident(incident_id):
    incident_to_delete = Incident.query.get_or_404(incident_id)
    db.session.delete(incident_to_delete)
    db.session.commit()
    flash('Incident deleted successfully!', 'success')
    return redirect(url_for('incident.incidents_overview'))

