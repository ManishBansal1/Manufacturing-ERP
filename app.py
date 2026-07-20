from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db, User

from flask_login import LoginManager

from blueprints.auth.routes import auth_bp

from blueprints.dashboard.routes import dashboard_bp

from blueprints.masters.routes import masters_bp

from blueprints.sales import sales_bp

from blueprints.jobwork.routes import jobwork_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"


app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(masters_bp)
app.register_blueprint(jobwork_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#with app.app_context():
#    db.create_all()


@app.route("/")
def home():
    return "Manufacturing ERP Running Successfully"

if __name__ == "__main__":
    app.run(debug=True)


app.register_blueprint(
    sales_bp,
    url_prefix="/sales"
)