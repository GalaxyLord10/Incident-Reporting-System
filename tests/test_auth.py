from app import app
from models.db_models import db, User
from flask_login import current_user
from flask import url_for

from tests.test_basic import BasicTests


class AuthTests(BasicTests):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        # Data for a new test user
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        # Use the test client to send a post request to the registration route
        response = self.client.post(url_for('auth.register'), data=data, follow_redirects=True)
        self.assert200(response)
        # Verify that the user was added to the database
        user = User.query.filter_by(email='testuser@example.com').first()
        self.assertIsNotNone(user)

    def test_registration_exisiting_email(self):
        user = User(email='existinguser@example.com')
        user.set_password('existingpassword')
        db.session.add(user)
        db.session.commit()

        data = {
            'email': 'existinguser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post(url_for('auth.register'), data=data, follow_redirects=True)
        self.assertIn(b'Email already exists', response.data)

    def test_login(self):
        # First, add a test user to the database
        user = User(email='loginuser@example.com')
        user.set_password('loginpassword')
        db.session.add(user)
        db.session.commit()

        # Data for the login post request
        data = {
            'email': 'loginuser@example.com',
            'password': 'loginpassword'
        }

        # Use the test client to send a post request to the login route with the test user's credentials
        response = self.client.post(url_for('auth.login'), data=data, follow_redirects=True)
        self.assert200(response)
        # Verify that the login was successful and user is authenticated
        self.assertTrue(current_user.is_authenticated)

    def test_login_incorrect_password(self):
        user = User(email="testuser@example.com")
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(url_for('auth.login'), data=data, follow_redirects=True)
        self.assertIn(b'Incorrect password', response.data)

    def test_login_unregistered_email(self):
        data = {
            'email': 'unregistered@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(url_for('auth.login'), data=data, follow_redirects=True)
        self.assertIn(b'Login Unsuccessful. Please check email and password', response.data)

    def test_logout(self):
        user = User(email='loginuser@example.com')
        user.set_password('loginpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(url_for('auth.login'), data={'email': 'loginuser@example.com', 'password': 'loginpassword'},
                         follow_redirects=True)

        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assert200(response)
        self.assertFalse(current_user.is_authenticated)
