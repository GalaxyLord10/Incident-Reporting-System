from flask import Flask
from controllers.home import home
from controllers.authentication import auth
from controllers.dashboard import dash
from controllers.incidents import incident
from extensions import login_manager, db
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


if __name__ == '__main__':
    app.run(debug=True)





