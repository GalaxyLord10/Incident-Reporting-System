from app import app
from models.db_models import db, Incident, User, IncidentUpdate
from flask import url_for
from flask_login import current_user

from tests.test_basic import BasicTests


class IncidentManagementTests(BasicTests):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the context
        self.client = self.app.test_client()
        db.create_all()
        user = User(email='test@example.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_incident(self):
        # Login the user
        response_login = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'test_password'
        })

        # Check if user is authenticated after login
        self.assertTrue(current_user.is_authenticated)

        with self.client.session_transaction() as session:
            response = self.client.post('/create_incident', data={
                'system': 'Test System',
                'product': 'Test Product',
                'issue': 'Test issue description',
                'time_of_occurrence': '2023-08-31 12:00:00'
            }, follow_redirects=True)

            self.assertIn(b'Incident created successfully!', response.data)

    def test_post_update(self):
        # Assuming an incident and a test user are already created and logged in
        incident = Incident(system='Test System', product='Test Product', issue='Test issue description')
        db.session.add(incident)
        db.session.commit()

        data = {
            'description': 'This is a test update for the incident.'
        }

        response = self.client.post(f'/incident/{incident.id}/update', data=data, follow_redirects=True)
        self.assertIn(b'Update posted successfully!', response.data)

        update = IncidentUpdate.query.filter_by(description='This is a test update for the incident.').first()
        self.assertIsNotNone(update)

