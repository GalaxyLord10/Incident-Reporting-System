from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms.admin_user_creation_form import AdminUserCreationForm
from models.db_models import User, db
from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm
from extensions import login_manager

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        User.create_user(email=form.email.data, password=form.password.data)
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('authentication/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('dash.dashboard'))
            else:
                flash('Incorrect password', 'warning')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('authentication/login.html', form=form)


@auth.route('/create_admin_user', methods=['GET', 'POST'])
@login_required
def create_admin_user():
    if current_user.account_type != 'admin':
        return redirect(url_for('dash.dashboard'))

    form = AdminUserCreationForm()

    if form.validate_on_submit():
        user = User.create_user(email=form.email.data,
                                password=form.password.data,
                                account_type=form.account_type.data,
                                role=form.account_type.data)
        return redirect(url_for('dash.admin_dashboard'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dash.dashboard'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
