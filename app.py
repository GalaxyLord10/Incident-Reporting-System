from flask import Flask
from flask_login import current_user
from models.db_models import Incident
from controllers.home import home
from controllers.authentication import auth
from controllers.dashboard import dash
from controllers.incidents import incident
from extensions import login_manager, db
from controllers.admin_dashboard import admin_dashboard
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config.DefaultConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning
db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(incident)
app.register_blueprint(admin_dashboard, url_prefix='/admin')


if __name__ == '__main__':
    app.run(debug=True)


@app.context_processor
def add_notifications():
    if current_user.is_authenticated:
        incidents = Incident.query.filter((Incident.notification_status == 'Unread')
                                          | (Incident.notification_status == 'Updated')).all()
        return {'incidents': incidents}
    return {}
  