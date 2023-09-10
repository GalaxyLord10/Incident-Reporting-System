from models.db_models import db, User
from app import app
from test_basic import BasicTests


class DatabaseTests(BasicTests):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        import time
        unique_email = f"test{int(time.time())}@example.com"

        new_user = User(email=unique_email, password="testpass")
        db.session.add(new_user)
        db.session.commit()

        added_user = User.query.filter_by(email=unique_email).first()
        assert added_user is not None




