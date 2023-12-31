from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.db_models import User
from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm
from extensions import login_manager
from utilities.utilities import configure_logger, db_commit, query_user_by_email, flash_and_log

auth = Blueprint('auth', __name__)


# register the general user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already exists', 'warning')
                return redirect(url_for('auth.register'))

            new_user = User(email=form.email.data)
            new_user.password = form.password.data
            db_commit(new_user) # add new user to database
            flash_and_log('Registration successful!', 'success', f"{form.email.data} has registered.")
            return redirect(url_for('auth.login'))
    except AssertionError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash_and_log('An unexpected error occurred. Please try again.', 'danger', f"An error occurred during registration: {str(e)}")
    return render_template('authentication/register.html', form=form)


# register an admin
@auth.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already exists', 'warning')
                return redirect(url_for('auth.register'))

            new_user = User(email=form.email.data)
            new_user.password = form.password.data
            new_user.account_type = "admin" # set the account_type to admin
            db_commit(new_user)
            flash_and_log('Registration successful!', 'success', f"{form.email.data} has registered.")
            return redirect(url_for('auth.login'))
    except AssertionError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash_and_log('An unexpected error occurred. Please try again.', 'danger', f"An error occurred during registration: {str(e)}")
    return render_template('authentication/register.html', form=form)


# login the user
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = query_user_by_email(form.email.data)
            if user: # check if user exists
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
        flash_and_log('An unexpected error occurred during login. Please try again.', 'danger', f"An error occurred during login: {str(e)}")
    return render_template('authentication/login.html', form=form)


# logout the user
@auth.route('/logout')
def logout():
    try:
        logout_user()
        flash_and_log('You have been logged out.', 'success', "User has logged out.")
    except Exception as e:
        flash('An unexpected error occurred during logout. Please try again.', 'danger', f"An error occurred during logout: {str(e)}")
    return redirect(url_for('dash.dashboard'))


# load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
