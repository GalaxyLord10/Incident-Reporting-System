from app import db, app
from models.db_models import User


def create_default_admin():
    with app.app_context():
        admin_email = "admin@example.com"
        user = User.query.filter_by(email=admin_email).first()

        if user:
            print("Default admin user already exists!")
            return

        admin = User(email=admin_email)
        admin.set_password("defaultpassword")  # Set a default password
        admin.account_type = "admin"

        db.session.add(admin)
        db.session.commit()
        print(f"Default admin user created with email: {admin_email} and password: defaultpassword")


if __name__ == "__main__":
    create_default_admin()