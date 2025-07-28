# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # App specific config
    YFINANCE_TICKERS = os.environ.get('YFINANCE_TICKERS', "SPY QQQ").split()


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'optionforge_dev.db')
    

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    CELERY_TASK_ALWAYS_EAGER = True # Run tasks synchronously for tests


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure DATABASE_URL is set in production environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for production")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
