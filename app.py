from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize the Flask app
app = Flask(__name__)

# Set secret key for session management (used for protecting user sessions)
app.config['SECRET_KEY'] = 'root'  # Use your actual secret key here

# Configure the database URI (use your own MySQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/chemical_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirects to login if not logged in
migrate = Migrate(app, db)

# Import your routes, models, and forms
from app import routes, models

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
