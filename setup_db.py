from app import app, db


def create_tables():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    create_tables()
