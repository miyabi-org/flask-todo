from flask import Flask, jsonify, redirect, render_template
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
        return render_template('index.html', message="Flask Todo API", status="online")
        
    # Add health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200
    
    # Initialize extensions - moved after route definitions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Create tables if they don't exist - handle database errors gracefully
    # This is now executed in a separate function to ensure it doesn't block startup
    def initialize_database():
        try:
            with app.app_context():
                db.create_all()
                app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Database initialization error: {str(e)}")
            app.logger.info("Application will continue to run with limited functionality")
    
    # Start database initialization in a non-blocking way
    import threading
    db_thread = threading.Thread(target=initialize_database)
    db_thread.daemon = True  # Make thread a daemon so it doesn't block app shutdown
    db_thread.start()
    
    return app