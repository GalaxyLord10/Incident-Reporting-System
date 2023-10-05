import unittest
from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash
from app import app
from extensions import db
from models.db_models import User


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_register(self):
        response = self.client.post('/register', data={
            'email': 'test@email.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.data, 'html.parser')
        flash_message_element = soup.find(class_='alert-success')
        self.assertIsNotNone(flash_message_element)
        self.assertIn('Registration successful!', flash_message_element.text)

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        hashed_password = generate_password_hash('password123')
        user = User(email='test@email.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        response = self.login('test@email.com', 'password123')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        flash_message_element = soup.find(class_='alert-success')
        self.assertIsNotNone(flash_message_element)
        self.assertIn('Login successful!', flash_message_element.text)

    def test_logout(self):
        self.login('test@email.com', 'password123')
        response = self.logout()
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.data, 'html.parser')
        flash_message_element = soup.find(class_='alert-success')
        self.assertIsNotNone(flash_message_element)
        self.assertIn('You have been logged out.', flash_message_element.text)

    def test_dashboard_access_without_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        login_element = soup.find(string='Login')
        self.assertIsNotNone(login_element)

    def test_dashboard_access_with_login(self):
        self.login('test@email.com', 'password123')
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        login_element = soup.find(string='Login')
        self.assertIsNotNone(login_element)

    def test_incidents_overview(self):
        self.login('test@email.com', 'password123')
        response = self.client.get('/incidents_overview', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_incident(self):
        hashed_password = generate_password_hash('password123')
        user = User(email='test@email.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        self.login('test@email.com', 'password123')
        response = self.client.post('/create_incident', data={
            'system': 'System1',
            'product': 'Product1',
            'issue': 'Issue1',
            'time_of_occurrence': '2023-01-01 12:34:56',
            'status': 'Ongoing'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        flash_message_element = soup.find(class_='alert-success')
        self.assertIsNotNone(flash_message_element)
        self.assertIn('Incident created successfully!', flash_message_element.text)


if __name__ == '__main__':
    unittest.main()
