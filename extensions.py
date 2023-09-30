from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Initialize LoginManager object
login_manager = LoginManager()

# Initialize SQLAlchemy object
db = SQLAlchemy()
