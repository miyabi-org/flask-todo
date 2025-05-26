import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'todo')
    
    # Set a default SQLite database URI if PostgreSQL connection parameters are not provided
    if DB_HOST and DB_USER and DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Use in-memory SQLite as fallback (will not persist data)
        SQLALCHEMY_DATABASE_URI = "sqlite:///memory"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Cloud Storage configuration
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'todo-app-images')
    
    # Secret key for session
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')