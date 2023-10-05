from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.db_models import User
from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm
from extensions import login_manager
from utilities.utilities import configure_logger

auth = Blueprint('auth', __name__)
user_activity_logger = configure_logger()


def query_user_by_email(email):
    return User.query.filter_by(email=email).first()


def flash_and_log(message, level, log_message):
    flash(message, level)
    user_activity_logger.info(log_message)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = query_user_by_email(form.email.data)
            if user:
                flash_and_log('Email already exists', 'warning', f"Registration failed. Email {form.email.data} already exists.")
                return redirect(url_for('auth.register'))
            User.create_user(email=form.email.data, password=form.password.data)
            flash_and_log('Registration successful!', 'success', f"{form.email.data} has registered.")
            return redirect(url_for('auth.login'))
    except Exception as e:
        user_activity_logger.error(f"An error occurred during registration: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'danger')
    return render_template('authentication/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = query_user_by_email(form.email.data)
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    flash_and_log('Login successful!', 'success', f"{user.email} has logged in.")
                    if user.account_type == 'admin':
                        return redirect(url_for('dash.admin_dashboard'))
                    else:
                        return redirect(url_for('dash.dashboard'))
                else:
                    flash_and_log('Incorrect password', 'warning', f"Incorrect password attempted for {form.email.data}.")
            else:
                flash_and_log('Login Unsuccessful. Please check email and password', 'danger', f"Failed login attempt for {form.email.data}.")
    except Exception as e:
        user_activity_logger.error(f"An error occurred during login: {str(e)}")
        flash('An unexpected error occurred during login. Please try again.', 'danger')
    return render_template('authentication/login.html', form=form)


@auth.route('/logout')
def logout():
    try:
        logout_user()
        flash_and_log('You have been logged out.', 'success', "User has logged out.")
    except Exception as e:
        user_activity_logger.error(f"An error occurred during logout: {str(e)}")
        flash('An unexpected error occurred during logout. Please try again.', 'danger')
    return redirect(url_for('dash.dashboard'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
