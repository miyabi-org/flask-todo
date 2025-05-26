from flask import Flask, jsonify, redirect
from .models import db
from config import Config
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Create a root route that returns a simple status message
    @app.route('/')
    def index():
        return jsonify({"message": "Flask Todo API", "status": "online"}), 200
    
    # Create tables if they don't exist - handle database errors gracefully
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Database initialization error: {str(e)}")
            app.logger.info("Application will continue to run with limited functionality")
    
    return app