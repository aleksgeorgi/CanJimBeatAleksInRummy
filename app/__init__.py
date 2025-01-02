from flask import Flask

def create_app():
    """Application factory for the Flask app."""
    app = Flask(__name__)

    # Import and register blueprints
    from .routes import routes
    app.register_blueprint(routes)

    return app

# TODO what are blueprints???