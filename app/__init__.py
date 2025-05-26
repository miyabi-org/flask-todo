from flask import Flask
from .models import db
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app