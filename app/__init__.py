from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    """Application factory for the Flask app."""
    app = Flask(__name__)

    # Set up database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<USER>:<PASSWORD>@<HOST>/<DB_NAME>' # TODO env vars?
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    from .models import db
    db.init_app(app)

    # Import and register blueprints
    from .routes import routes
    app.register_blueprint(routes)

    return app
