import unittest
from models.db_models import User, IncidentUpdate, Incident
from extensions import db
from app import app
from test_basic import BasicTests


class DatabaseTests(BasicTests):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User(email='test@email.com', password='password123', role='Admin')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.email, 'test@email.com')
        self.assertEqual(user.role, 'Admin')
        self.assertTrue(user.check_password('password123'))

    def test_incident_creation(self):
        user = User(email='test2@email.com', password='password123', role='Admin')
        db.session.add(user)
        db.session.commit()

        incident = Incident(user_id=user.id, system='System1', product='Product1', issue='Issue1')
        db.session.add(incident)
        db.session.commit()

        self.assertEqual(incident.system, 'System1')
        self.assertEqual(incident.user_id, user.id)

    def test_incident_update_creation(self):
        user = User(email='test3@email.com', password='password123', role='Admin')
        db.session.add(user)
        db.session.commit()

        incident = Incident(user_id=user.id, system='System1', product='Product1', issue='Issue1')
        db.session.add(incident)
        db.session.commit()

        incident_update = IncidentUpdate(incident_id=incident.id, description='Description1', user_id=user.id)
        db.session.add(incident_update)
        db.session.commit()

        self.assertEqual(incident_update.description, 'Description1')
        self.assertEqual(incident_update.incident_id, incident.id)
        self.assertEqual(incident_update.user_id, user.id)


if __name__ == '__main__':
    unittest.main()




