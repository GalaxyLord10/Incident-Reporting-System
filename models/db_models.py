from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), default='IncidentReportView')  # Default role
    account_type = db.Column(db.String(80), default='general_user')  # Default to general user
    incidents = db.relationship('Incident', foreign_keys='Incident.user_id', backref='user', lazy=True)

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    system = db.Column(db.String(120))
    product = db.Column(db.String(120))
    issue = db.Column(db.Text)
    time_of_occurrence = db.Column(db.DateTime)
    status = db.Column(db.String(80), default='Ongoing')  # Default status


class IncidentUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    description = db.Column(db.Text)
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Permission(db.Model):
    # This table can be used if not using AAD for permissions
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

