from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from sqlalchemy.orm import validates


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), default='IncidentReportView')  # Default role
    account_type = db.Column(db.String(80), default='general_user')  # Default to general user
    incidents = db.relationship('Incident', foreign_keys='Incident.user_id', backref='user', lazy=True)

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise AssertionError("Invalid email address")
        return email

    @validates('role')
    def validate_role(self, key, role):
        valid_roles = ['IncidentReportView', 'Admin', 'AnotherRole']
        if role not in valid_roles:
            raise AssertionError("Invalid role")
        return role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, email, password, role="general_user"):
        user = cls(email=email, role=role, account_type=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    system = db.Column(db.String(120))
    product = db.Column(db.String(120))
    issue = db.Column(db.Text)
    time_of_occurrence = db.Column(db.DateTime)
    status = db.Column(db.String(80), default='Ongoing')

    @validates('system')
    def validate_system(self, key, system):
        if len(system) < 3:
            raise AssertionError("System name should be at least 3 characters long")
        return system

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['Ongoing', 'Resolved', 'Pending']
        if status not in valid_statuses:
            raise AssertionError("Invalid status")
        return status


class IncidentUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False, index=True)
    description = db.Column(db.Text)
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 10:
            raise AssertionError("Description should be at least 10 characters long")
        return description

