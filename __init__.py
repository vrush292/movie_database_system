# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import session
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
      # This should create the User table if it doesn't exist

    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change to your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'  # Change to a secure key

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes import api  # Import your routes
    app.register_blueprint(api)

    return app