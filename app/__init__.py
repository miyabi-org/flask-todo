from flask import Flask, jsonify, redirect
from .models import db
from config import Config
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    if not app.logger.handlers:
        app.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        app.logger.addHandler(handler)
    
    # Create a root route that returns a simple status message
    @app.route('/')
    def index():
        return jsonify({"message": "Flask Todo API", "status": "online"}), 200
    
    # Initialize extensions - moved after route definitions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Create tables if they don't exist - handle database errors gracefully
    # We do this in a non-blocking way to avoid hanging the application startup
    try:
        with app.app_context():
            db.create_all()
            app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Database initialization error: {str(e)}")
        app.logger.info("Application will continue to run with limited functionality")
    
    return app