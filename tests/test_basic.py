from flask_testing import TestCase
from app import app
from flask import url_for


class BasicTests(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def test_index(self):
        response = self.client.get(url_for('home.index'))
        self.assert200(response)


