from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.db_models import User
from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm
from extensions import login_manager
from utilities.utilities import configure_logger

auth = Blueprint('auth', __name__)
user_activity_logger = configure_logger()


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
        user_activity_logger.info(f"{form.email.data} has registered.")
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
                user_activity_logger.info(f"{user.email} has logged in.")
                if user.account_type == 'admin':
                    return redirect(url_for('dash.admin_dashboard'))
                else:
                    return redirect(url_for('dash.dashboard'))
            else:
                flash('Incorrect password', 'warning')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            user_activity_logger.info(f"{user.email} was unable to log in.")
    return render_template('authentication/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    user_activity_logger.info(f"User has logged out.")
    return redirect(url_for('dash.dashboard'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

  
