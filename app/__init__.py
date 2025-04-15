from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from app.config import Config

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bootstrap = Bootstrap()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Register the login view (to redirect if user is not logged in)
    login_manager.login_view = 'auth.login'

    # Register Blueprints (routes)
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
